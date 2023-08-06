import asyncio
import time

import aiohttp
import requests
import urllib3

import pcoss_scheduler_pkg.constants as c
import pcoss_scheduler_pkg.output
from pcoss_scheduler_pkg.helpers import Measurement, scheduled_operation

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def operation(so: scheduled_operation, session, ts):
    it0 = time.perf_counter()
    me = Measurement(
        admission_time=it0,
        server_ret=None,
        request_processing_time=None,
        release_time=None,
        )

    url = f'{so.base_url}/{so.endpoint}/{so.machine}/{int(so.item)}/{int(so.operation_duration-1000)}'
    
    await asyncio.sleep(so.start_time/1000.0)

    it1 = time.perf_counter()
    async with session.get(url, ssl=False, timeout=600) as resp:
        it2 = time.perf_counter()
        ret = await resp.text()

    it3 = time.perf_counter()

    me.server_ret = float(ret)
    me.request_processing_time = (it2 - it1) * 1000
    me.release_time = it3

    if me.request_processing_time > so.operation_duration:
        _correct_schedule(so)

    if c.PRINT_RESPONSES:
        print(f'{url=}\t{ret=}')
    
    if c.PRINT_RESPONES_DEBUG_TIMES:
        error_symbol = '***'
        ok_symbol = ''
        print(f'{so.endpoint=}\t{so.machine=}\t{so.start_time=:.2f}\t{so.end_time=:.2f}\t{so.operation_duration=:.2f}')
        print(f'{error_symbol if me.request_processing_time > so.operation_duration else ok_symbol}\tit2-it1={me.request_processing_time:.2f}')
    
    pcoss_scheduler_pkg.output.output_dict.update({(so.job, so.machine): (so, me)})

    return ret


def _correct_schedule(so: scheduled_operation):
    if c.PRINT_SCHEDULE_CORRECTION_MESSAGE:
        print('Schedule needs correction')  
    else:
        pass
