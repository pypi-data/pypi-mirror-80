import asyncio
import logging

from salusshcpy import SALUSSession

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STOP,
)

from homeassistant.helpers import device_registry as dr

from .const import (
    DOMAIN,
    CONF_EUID
)

PLATFORMS = [
    "thermostat"
]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    conf = config.get(DOMAIN)

    if not conf:
        return True

    configured_hosts = {
        entry.data.get("ip_address")
        for entry in hass.config_entries.async_entries(DOMAIN)
    }

    if conf[CONF_IP_ADDRESS] in configured_hosts:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
        )
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = entry.data

    _LOGGER.cr("Connecting to SALUS Gateway")

    session = await hass.async_add_executor_job(
        SALUSSession,
        data[CONF_IP_ADDRESS],
        data[CONF_EUID]
    )

    information = session.information
    hass.data[DOMAIN][entry.entry_id] = session
    device_registry = await dr.async_get_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, data[CONF_IP_ADDRESS])},
        manufacturer="SALUS",
        name=data[CONF_NAME],
        model="Gateway",
        sw_version=information.version,
    )

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    async def stop_polling(event):
        _LOGGER.debug("Stopping polling service of SALUS")
        await hass.async_add_executor_job(session.stop_polling)

    async def start_polling(event):
        """Start polling service."""
        _LOGGER.debug("Starting polling service of SALUS")
        await hass.async_add_executor_job(session.start_polling)
        session.reset_connection_listener = hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, stop_polling
        )

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_polling)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    session: SALUSSession = hass.data[DOMAIN][entry.entry_id]
    session.reset_connection_listener()
    _LOGGER.debug("Stopping polling service of SALUS")
    await hass.async_add_executor_job(session.stop_polling)

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
