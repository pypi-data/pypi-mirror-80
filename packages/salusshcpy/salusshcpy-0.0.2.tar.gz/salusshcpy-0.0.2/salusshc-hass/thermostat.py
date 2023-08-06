import logging

from salusshcpy import SALUSSession, SALUSThermostat
from homeassistant.components.climate import ClimateEntity
from homeassistant.const import ATTR_TEMPERATURE

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    entities = []
    session: SALUSSession = hass.data[DOMAIN][config_entry.entry_id]

    for device in session.device_helper.thermostats:

        entity = Thermostat(device)
        entities += [entity]

    if entities:
        async_add_entities(entities)


class Thermostat(ClimateEntity):

    def __init__(
        self,
        device: SALUSThermostat
    ):
        self._name = device.name
        self._unique_id = device.unique_id
        self._device = device

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        def on_state_changed():
            self.schedule_update_ha_state()

        self._device.subscribe_callback(self.entity_id, on_state_changed)

    async def async_will_remove_from_hass(self):
        await super().async_will_remove_from_hass()
        self._device.unsubscribe_callback(self.entity_id)

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def temperature_unit(self):
        return self._device.temperature_unit

    @property
    def current_temperature(self):
        return self._device.current_temperature

    @property
    def max_temp(self):
        return self._device.max_temp

    @property
    def min_temp(self):
        return self._device.min_temp

    @property
    def target_temperature(self):
        return self._device.target_temperature

    @property
    def target_temperature_step(self):
        return self._device.precision

    @property
    def hvac_mode(self):
        return self._device.hvac_mode

    @property
    def hvac_modes(self):
        return self._device.hvac_modes

    @property
    def hvac_action(self):
        return self._device.hvac_action

    @property
    def preset_mode(self):
        return self._device.preset_mode

    @property
    def preset_modes(self):
        return self._device.preset_modes

    @property
    def supported_features(self):
        return self._device.supported_features

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        if self.min_temp <= temperature <= self.max_temp:
            self._device.set_temperature(float(temperature))

    async def async_set_hvac_mode(self, hvac_mode: str):
        if hvac_mode not in self.hvac_modes:
            return

        self._device.set_climate_device_mode(hvac_mode)

    async def async_set_preset_mode(self, preset_mode: str):
        if preset_mode not in self.preset_modes:
            return

        self._device.set_climate_device_preset(preset_mode)
