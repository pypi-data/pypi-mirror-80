from typing import Dict, List, Set, Tuple

import pandas as pd
import toml

import pcoss_scheduler_pkg.constants as c
import pcoss_scheduler_pkg.helpers as h


class ProblemInput:
    def __init__(self, init_dict: Dict):

        self.table_in = pd.read_csv(
            init_dict['files']['data'],
            index_col=init_dict['problem_data']['index_cols'],
            usecols=lambda col: col not in init_dict['problem_data']['grouping_cols'],
            )

        self.column_operation_dict = {}
        avaliable_operations_list = ['A', 'B', 'C']

        use_operation_num = 0

        for cm in init_dict['problem_data']['conflicting_machines']:
            self.column_operation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
            self.column_operation_dict[cm[1]] = avaliable_operations_list[use_operation_num]
            use_operation_num = (use_operation_num + 1) % 3

        for col_num in range(len(self.table_in.columns)):
            if col_num not in [cm for te in init_dict['problem_data']['conflicting_machines'] for cm in te]:
                self.column_operation_dict[col_num] = '0'

        job_cnt, machine_cnt = self.table_in.shape

        self.conflict_graph_in = (
            h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
                job_cnt=job_cnt,
                machine_cnt=machine_cnt,
                conflicting_machines=init_dict['problem_data']['conflicting_machines'],
                show=init_dict['display_config']['show_conflict_graph']))

        self.processing_times = pd.read_csv(
            init_dict['files']['processing_times'],
            index_col=init_dict['problem_data']['index_cols'],
            usecols=lambda col: col not in init_dict['problem_data']['grouping_cols'],
            ) * 100 + 1000
        
        self.conflicting_machines_list = init_dict['problem_data']['conflicting_machines']

        self.base_url = init_dict['problem_data']['base_url']

        self.algorithm = init_dict['algorithm_config']['algorithm_name']
        self.objective = init_dict['algorithm_config']['objective']
        self.beam_width = init_dict['algorithm_config']['beam_width']

        self.print_responses = init_dict['display_config']['print_responses']
        self.print_method_times = init_dict['display_config']['print_method_times']
        self.show_conflict_graph = init_dict['display_config']['show_conflict_graph']
        self.show_result_schedule_graph = init_dict['display_config']['show_result_schedule_graph']
        self.show_gantt_plot = init_dict['display_config']['show_gantt_plot']


    @classmethod
    def from_toml(cls, toml_file: str):
        config_dict = toml.load(toml_file)
        
        config_dict['problem_data']['conflicting_machines'] = list(
            map(tuple, config_dict['problem_data']['conflicting_machines'])
            )
        
        return cls(config_dict)
