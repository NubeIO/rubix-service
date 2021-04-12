import logging
from threading import Thread

import gevent
from flask import current_app
from mrb.brige import MqttRestBridge

from .setting import AppSetting

logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:
    @staticmethod
    def run():
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        if setting.mqtt_rest_bridge_setting.enabled:
            MqttRestBridge(port=setting.port,
                           mqtt_setting=setting.mqtt_rest_bridge_setting,
                           callback=Background.sync_on_start).start()
            if setting.mqtt_rest_bridge_setting.master:
                from src.discover.remote_device_registry import RemoteDeviceRegistry
                gevent.spawn(RemoteDeviceRegistry().register)

    @staticmethod
    def sync_on_start():
        pass
