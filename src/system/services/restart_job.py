import logging
from datetime import datetime, timedelta

import gevent

from src import AppSetting
from src.system.resources.service.utils import create_service_restart_job, get_service_restart_jobs
from src.system.utils.shell import execute_command_with_exception

logger = logging.getLogger(__name__)


class RestartJob:
    def setup(self):
        while True:
            gevent.sleep(60)
            self.restart()

    @classmethod
    def restart(cls):
        logger.info("Service restart has been called")
        service_restart_jobs: dict = get_service_restart_jobs()
        for key, restart_job in service_restart_jobs.items():
            timer: int = restart_job.get("timer", 0)
            cmd: str = restart_job.get("cmd", None)
            next_time: str = restart_job.get("next_time", None)
            time_check: bool = False if next_time is None else \
                datetime.strptime(next_time, '%Y-%m-%d %H:%M:%S.%f') <= datetime.now()
            if timer > 0 and cmd is not None and time_check:
                try:
                    execute_command_with_exception(cmd)
                    restart_job = {**restart_job, "prev_time": str(datetime.now()),
                                   "next_time": str(datetime.now() + timedelta(minutes=timer)), "error": ''}
                except Exception as e:
                    restart_job = {**restart_job, "next_time": str(datetime.now() + timedelta(minutes=timer)),
                                   "error": str(e)}
                    logger.error(str(e))
                create_service_restart_job({key: restart_job})
        logger.info("Service restart has been completed")
