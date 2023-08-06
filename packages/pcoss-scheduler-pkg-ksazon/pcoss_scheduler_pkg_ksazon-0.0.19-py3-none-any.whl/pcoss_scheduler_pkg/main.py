import argparse
import asyncio
import time
from typing import List, Set, Tuple

import constants as c
import helpers as h
import output
import scheduler as s
from problem_input import ProblemInput


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("toml_file", help="Path to the TOML file to be used", type=str)
    args = ap.parse_args()

    pi = ProblemInput.from_toml(args.toml_file)
    c.PRINT_METHOD_TIMES = pi.print_method_times
    
    sc = s.Scheduler.from_ProblemInput(pi)

    sc.prepare()
    
    if pi.show_gantt_plot:
        h.plot_gantt_chart(sc.schedule)

    ts = time.perf_counter()
    await sc.run()
    te = time.perf_counter()

    if pi.print_method_times:
        print(f'Function "run" execution time: {te-ts:.3f}s')

    # print(output.output_dict)


if __name__ == '__main__':
    (asyncio
        .get_event_loop()
        .run_until_complete(
            main()
        )
    )
