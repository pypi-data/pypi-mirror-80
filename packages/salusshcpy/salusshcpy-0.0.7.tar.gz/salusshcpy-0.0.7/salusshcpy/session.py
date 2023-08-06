
import typing
import threading
import time
import logging

from .api import SHCAPI, JSONRPCError
from .device import SALUSDevice
from .information import SALUSInformation
from .device_helper import SALUSDeviceHelper

logger = logging.getLogger("salusshcpy")


class SALUSSession:

    def __init__(self, controller_ip: str, euid: str):
        self._api = SHCAPI(controller_ip=controller_ip, euid=euid)
        self._device_helper = SALUSDeviceHelper(self._api)
        self._information = None
        self._devices_by_id = {}

        self._get_information()

        self._polling_thread = None
        self._stop_polling_thread = False

        self.reset_connection_listener = None

    def _get_information(self):
        raw_information = self._api.get_information()
        self._information = SALUSInformation(api=self.api, raw_information=raw_information)

        for raw_device in self._information.other_devices_raw:
            device_id = raw_device["data"]["UniID"]
            self._devices_by_id[device_id] = self._device_helper.device_init(raw_device)

    def _long_poll(self, wait_seconds=0):
        try:
            raw_results = self.api.long_polling_poll(wait_seconds)
            for raw_result in list(
                    filter(
                        lambda x: not x["data"]["DeviceType"] == 200 and not x["data"]["DeviceType"] == 300,
                        raw_results
                    )
            ):
                self._process_long_polling_poll_result(raw_result)

            return True
        except JSONRPCError as json_rpc_error:
            raise json_rpc_error

    def _process_long_polling_poll_result(self, raw_result):
        device_id = raw_result["data"]["UniID"]
        if device_id in self._devices_by_id.keys():
            device = self._devices_by_id[device_id]
            device.process_long_polling_poll_result(raw_result)
        else:
            logger.debug(f"Skipping polling result with unknown device id {device_id}.")
            print(f"Skipping polling result with unknown device id {device_id}.")
            return

    def start_polling(self):
        if self._polling_thread is None:

            def polling_thread_main():
                while not self._stop_polling_thread:
                    try:
                        if not self._long_poll():
                            logging.warning("_long_poll returned False. Waiting 1 second.")
                            time.sleep(1.0)
                    except RuntimeError as err:
                        self._stop_polling_thread = True
                        logging.info( "Stopping polling thread after expected runtime error.")
                        logging.info(f"Error description: {err}. {err.args}")
                    except Exception as ex:
                        logging.error(f"Error in polling thread: {ex}. Waiting 15 seconds.")
                        time.sleep(15.0)

            self._polling_thread = threading.Thread(target=polling_thread_main, name="SALUSPollingThread")
            self._polling_thread.start()

        else:
            raise ValueError("Already polling!")

    @property
    def devices(self) -> typing.Sequence[SALUSDevice]:
        return list(self._devices_by_id.values())

    def device(self, device_id) -> SALUSDevice:
        return self._devices_by_id[device_id]

    @property
    def information(self) -> SALUSInformation:
        return self._information

    @property
    def api(self):
        return self._api

    @property
    def device_helper(self) -> SALUSDeviceHelper:
        return self._device_helper

