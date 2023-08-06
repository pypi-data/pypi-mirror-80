import logging

from salusshcpy import SALUSDevice

from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SALUSEntity(Entity):

    def __init__(self, device: SALUSDevice, controller_ip: str):
        self._device = device
        self._controller_ip = controller_ip

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

    def update(self):
        self._device.update()

    @property
    def unique_id(self):
        return self._device.unique_id

    @property
    def is_available(self):
        return self._device.is_available

    @property
    def name(self):
        return self._device.name

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "manufacturer": "SALUS",
            "model": self._device.model,
            "sw_version": "",
            "via_device": (DOMAIN, self._controller_ip),
        }
