import logging
import json

from .api import SHCAPI

logger = logging.getLogger("salusshcpy")


class SALUSDevice:
    def __init__(self, api: SHCAPI, raw_device):
        self._api = api
        self._raw_device = raw_device
        self._callbacks = {}

    @property
    def is_available(self):
        return True if self._raw_device.get("sZDOInfo", {}).get("OnlineStatus_i", 1) == 1 else False

    @property
    def name(self):
        return json.loads(self.s_zdo.get("DeviceName", '{"deviceName": "Unknown"}'))\
            .get("deviceName", None)

    @property
    def unique_id(self):
        return self.data.get("UniID", None)

    @property
    def supported_features(self):
        return None

    @property
    def device_class(self):
        return ""

    @property
    def data(self):
        return self._raw_device.get("data", None)

    @property
    def sit_600th(self):
        return self._raw_device.get("sIT600TH", {})

    @property
    def device_l(self):
        return self._raw_device.get("DeviceL", {})

    @property
    def s_zdo(self):
        return self._raw_device.get("sZDO", {})

    @property
    def model(self):
        return self.device_l.get("ModelIdentifier_i", None)

    @property
    def device_type(self):
        return self.data.get("DeviceType", None)

    def summary(self):
        print(f"Device: {self.unique_id}")
        print(f"  Name          : {self.name}")
        print(f"  Manufacturer  : Salus")
        print(f"  Unique ID        : {self.unique_id}")

    def process_long_polling_poll_result(self, raw_result):
        self._raw_device = raw_result

        for callback in self._callbacks:
            self._callbacks[callback]()

    def subscribe_callback(self, entity, callback):
        self._callbacks[entity] = callback

    def unsubscribe_callback(self, entity):
        self._callbacks.pop(entity, None)

    def update(self):
        return None
