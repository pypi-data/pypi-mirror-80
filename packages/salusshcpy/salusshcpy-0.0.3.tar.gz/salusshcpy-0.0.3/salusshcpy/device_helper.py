import logging
import typing

from .device import SALUSDevice

from .models_impl import (
    SALUSThermostat,
    SUPPORTED_MODELS,
    build
)

logger = logging.getLogger("salusshcpy")


class SALUSDeviceHelper:
    def __init__(self, api):
        self._api = api
        self._devices_by_model = {}
        for model in SUPPORTED_MODELS:
            self._devices_by_model[model] = {}

    def device_init(self, raw_device):
        device_id = raw_device["data"]["UniID"]
        device_model = raw_device["DeviceL"]["ModelIdentifier_i"]
        print(device_model)
        if device_model in SUPPORTED_MODELS:
            device = build(api=self._api, raw_device=raw_device)
            self._devices_by_model[device_model][device_id] = device
        else:
            device = SALUSDevice(api=self._api, raw_device=raw_device)
        return device

    @property
    def thermostats(self) -> typing.Sequence[SALUSThermostat]:
        if "Thermostat" not in SUPPORTED_MODELS:
            return []
        return list(self._devices_by_model["Thermostat"].values())
