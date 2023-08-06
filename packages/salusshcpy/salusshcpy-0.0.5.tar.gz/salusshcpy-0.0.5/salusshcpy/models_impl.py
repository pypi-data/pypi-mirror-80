from .device import SALUSDevice
from .api import SHCAPI

from .const import (
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    TEMP_CELSIUS,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    PRESET_FOLLOW_SCHEDULE,
    PRESET_OFF,
    PRESET_PERMANENT_HOLD,
)


class SALUSThermostat(SALUSDevice):

    def __init__(self, api: SHCAPI, raw_device):
        super().__init__(api, raw_device)

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def precision(self):
        return 0.5

    @property
    def current_temperature(self):
        return self.sit_600th["LocalTemperature_x100"] / 100

    @property
    def target_temperature(self):
        return self.sit_600th["HeatingSetpoint_x100"] / 100

    @property
    def max_temp(self):
        return self.sit_600th.get("MaxHeatSetpoint_x100", 3500) / 100

    @property
    def min_temp(self):
        return self.sit_600th.get("MinHeatSetpoint_x100", 500) / 100

    @property
    def hvac_mode(self):
        return HVAC_MODE_OFF if self.sit_600th["HoldType"] == 7 else HVAC_MODE_HEAT

    @property
    def hvac_action(self):
        return CURRENT_HVAC_OFF if self.sit_600th["HoldType"] == 7 else CURRENT_HVAC_IDLE \
            if self.sit_600th["RunningState"] % 2 == 0 else CURRENT_HVAC_HEAT

    @property
    def hvac_modes(self):
        return [HVAC_MODE_OFF, HVAC_MODE_HEAT]

    @property
    def preset_mode(self):
        return PRESET_OFF if self.sit_600th["HoldType"] == 7 else PRESET_PERMANENT_HOLD if self.sit_600th["HoldType"] == 2 \
            else PRESET_FOLLOW_SCHEDULE

    @property
    def preset_modes(self):
        return [PRESET_FOLLOW_SCHEDULE, PRESET_PERMANENT_HOLD, PRESET_OFF]

    @property
    def mac_address(self):
        return self.s_zdo.get("MACAddress", None)

    @property
    def firmware_version(self):
        return self.s_zdo.get("FirmwareVersion", None)

    def update(self):
        print(f"Update Thermostat")

    def summary(self):
        print(f"TRV Thermostat:")
        super().summary()
        print(f"  Current temperature:" + str(self.current_temperature))
        print(f"  Target temperature:" + str(self.target_temperature))

    def process_long_polling_poll_result(self, raw_result):
        super().process_long_polling_poll_result(raw_result)
        self.summary()

    async def set_temperature(self, celsius: float):
        await self.api.set_temperature(self, celsius)

    async def set_climate_device_mode(self, mode: str):
        await self.api.set_climate_device_mode(self, mode)

    async def set_climate_device_preset(self, preset: str):
        await self.api.set_climate_device_preset(self, preset)


MODEL_MAPPING = {
    "SQ610RF": SALUSThermostat
}

SUPPORTED_MODELS = MODEL_MAPPING.keys()


def build(api, raw_device):
    device_model = raw_device["DeviceL"]["ModelIdentifier_i"]
    assert device_model in SUPPORTED_MODELS, "Device model is supported"
    return MODEL_MAPPING[device_model](api=api, raw_device=raw_device)
