import random
from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np
import pandas as pd

import pcoss_scheduler_pkg.constants as c
import pcoss_scheduler_pkg.helpers as h
from pcoss_scheduler_pkg.helpers import scheduled_operation as so
from pcoss_scheduler_pkg.problem_input import ProblemInput


class ScheduleAlgorithmBase:
    def __init__(self, processing_times: pd.DataFrame,
            conflict_graph: nx.Graph, problem_input: ProblemInput):

        self.problem_input = problem_input
        self.pt = processing_times
        self.conflict_graph = conflict_graph
        self.candidate_schedules = [np.full(self.pt.shape, np.nan)]
        self.row_conflicts_set = {
            (o0[1], o1[1])
            for (o0, o1) in filter(
                lambda e: e[0][0] == e[1][0],
                conflict_graph.edges())
                }

    def insertion_order(self) -> List[Tuple[int, int]]:
        raise NotImplementedError

    def run(self) -> List[so]:
        raise NotImplementedError

    outcome_graph: nx.DiGraph = None


class Randomized(ScheduleAlgorithmBase):
    def insertion_order(self):
        return np.random.permutation(list(np.ndindex(self.pt.shape)))

    def run(self):
        return [
            (random.random() * 5, (r_idx, c_idx))
            for (r_idx, r) in enumerate(self.pt)
            for (c_idx, c) in enumerate(self.pt)
            ]


class InsertionBeam(ScheduleAlgorithmBase):
    def insertion_order(self) -> List[Tuple[int, int]]:
        first_order = []
        min_shape = min(self.pt.shape)
        pt_trimmed = self.pt[:min_shape, :].copy()
        row_idx = 0

        for row_idx in range(min_shape):
            max_col_idx = np.argmax(pt_trimmed[row_idx, :])
            first_order += [(row_idx, max_col_idx)]
            pt_trimmed = np.delete(pt_trimmed, max_col_idx, axis=1)

        other_order = [(x[0], x[1]) for x in filter(
            lambda e: (e[0], e[1]) not in first_order,
            np.transpose(
                np.unravel_index(
                    np.argsort(self.pt, axis=None)
                    [::-1],
                    shape=self.pt.shape)))]

        return first_order + other_order

    def solve_conflicting_ranks(self, rm: np.ndarray,
            changed_rows: Set[int], changed_cols: Set[int]) -> np.ndarray:

        new_changed_rows = set()
        new_changed_cols = set()

        for cr in changed_rows:
            for cc in changed_cols:
                cv = rm[cr, cc]

                for n in filter(
                        lambda n: rm[n] == cv,
                        self.conflict_graph[(cr, cc)]):

                    new_changed_rows.add(n[0])
                    new_changed_cols.add(n[1])
                    rm[n] += 1

        if new_changed_rows:
            return self.solve_conflicting_ranks(
                rm,
                new_changed_rows,
                new_changed_cols)

        return rm

    def row_conflicts(self, rm: np.ndarray, row: int, col: int
            ) -> List[Tuple[int, int]]:

        ret = []

        for cp in self.row_conflicts_set:
            if col == cp[0] and not np.isnan(rm[row, cp[1]]):
                ret += [(row, cp[1])]
            if col == cp[1] and not np.isnan(rm[row, cp[0]]):
                ret += [(row, cp[0])]

        return ret

    def path_rec(self, rm: np.ndarray, e: Tuple[int, int], asc: bool
            ) -> List[Tuple[int, int]]:

        step = 1 if asc else -1
        next_val = rm[e] + step
        next_e = next(
            filter(lambda n: rm[n] == next_val, self.conflict_graph[e]),
            None)

        if next_e:
            return [next_e] + self.path_rec(rm, next_e, asc)

        return []

    def path_while(self, rm: np.ndarray, e: Tuple[int, int], asc: bool
            ) -> List[Tuple[int, int]]:

        cg = self.conflict_graph
        step = 1 if asc else -1
        ret = []
        next_e = e

        while next_e:
            next_val = rm[next_e]+step
            next_e = next(
                filter(lambda n: rm[n] == next_val, cg[next_e]),
                None)

            if next_e:
                ret += [next_e]

        return ret

    def get_path(self, rm: np.ndarray, added_element_idx: Tuple[int, int]
            ) -> List[Tuple[int, int]]:

        pr = self.path_rec

        return (
            pr(rm, added_element_idx, False)
            + [added_element_idx]
            + pr(rm, added_element_idx, True)
        )

    def beam_search(self, rm_list: List[np.ndarray],
            added_element_idx: Tuple[int, int]) -> List[np.ndarray]:

        rm_costs = {}

        for rm_idx, rm_cur in enumerate(rm_list):
            jobs, machines = np.transpose(
                self.get_path(rm_cur, added_element_idx))
            cost = sum(self.pt[jobs, machines])
            rm_costs[rm_idx] = cost

        return (
            [
                rm_list[k]
                for k, v in
                sorted(rm_costs.items(), key=lambda e: e[1])
            ]
            [:self.problem_input.beam_width]
            )

    def schedule_as_graph(self, rm: np.ndarray):
        max_rank = int(np.max(rm))

        G = nx.DiGraph()

        for from_rank in range(1, max_rank):
            to_rank = from_rank + 1
            to_idxs = np.nonzero(rm == to_rank)

            for to_idx in np.transpose(to_idxs):
                same_job_idxs = [
                    (to_idx[0], machine)
                    for machine in np.nonzero(rm[to_idx[0], :] == from_rank)[0]
                ]
                same_machine_idxs = [
                    (job, to_idx[1])
                    for job in np.nonzero(rm[:, to_idx[1]] == from_rank)[0]
                ]

                for from_idx in same_job_idxs + same_machine_idxs:
                    G.add_edge(from_idx, tuple(to_idx))

        self.outcome_graph = G

        if self.problem_input.show_result_schedule_graph:
            h.plot_schedule_graph(self.outcome_graph)

    def schedule_as_list_of_scheduled_operations(self, rm: np.ndarray
            ) -> List[so]:

        scheduled_operations: List[so] = []
        cur_rank = 1
        st_mx = np.full(rm.shape, np.nan, dtype=object)

        while len(scheduled_operations) < rm.size:
            idxs = np.nonzero(rm == cur_rank)

            for idx in np.transpose(idxs):
                if cur_rank == 1:
                    prev_max_time = 0
                else:
                    prev_max_time = max(
                        [s.end_time
                        for s in st_mx[
                            tuple(np.transpose([e[0]
                            for e in self.outcome_graph.in_edges([tuple(idx)])]))]])

                end_time = prev_max_time + self.pt[idx[0]][idx[1]]

                cur_so = so(
                    base_url=self.problem_input.base_url,
                    rank=cur_rank,
                    start_time=prev_max_time,
                    end_time=end_time,
                    operation_duration=self.pt[idx[0]][idx[1]],
                    job=idx[0],
                    machine=idx[1],
                    endpoint=None,
                    item=None,
                    )
                scheduled_operations.append(cur_so)
                st_mx[idx[0]][idx[1]] = cur_so

            cur_rank += 1

        return scheduled_operations

    def run(self):
        for job, machine in self.insertion_order():
            candidate_schedules_with_children = []
            for cs in self.candidate_schedules:
                potential_rank = set()

                potential_rank.add(1)
                for e in np.argwhere(~np.isnan(cs[:, machine])):
                    potential_rank.add(cs[(e, machine)][0] + 1)
                for cell in self.row_conflicts(cs, job, machine):
                    potential_rank.add(cs[cell] + 1)

                for pr in potential_rank:
                    cs_with_child = cs.copy()
                    cs_with_child[job, machine] = pr
                    cs_with_child = self.solve_conflicting_ranks(
                        cs_with_child, {job,}, {machine,})
                    candidate_schedules_with_children.append(cs_with_child)

            self.candidate_schedules = self.beam_search(
                candidate_schedules_with_children, (job, machine))

        self.schedule_as_graph(self.candidate_schedules[0])

        return self.schedule_as_list_of_scheduled_operations(
            self.candidate_schedules[0])


ALGORITHM_CLASS_DICT = {
    'randomized': Randomized,
    'insertion_beam': InsertionBeam,
}
