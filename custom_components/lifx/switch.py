from __future__ import annotations
from homeassistant.components.switch import ( SwitchEntity, SwitchEntityDescription, SwitchDeviceClass )

from typing import Any

import aiolifx_effects as aiolifx_effects_module
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID, Platform
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_platform
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_point_in_utc_time

from .const import ( DOMAIN )
from .coordinator import LIFXUpdateCoordinator
from .entity import LIFXEntity
from .util import lifx_features

LIFX_SWITCH = SwitchEntityDescription(key="LIFX_SWTICH", name="LIFX Switch", device_class=SwitchDeviceClass.SWITCH)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LIFX from a config entry."""
    domain_data = hass.data[DOMAIN]
    coordinator: LIFXUpdateCoordinator = domain_data[entry.entry_id]
    if lifx_features(coordinator.device)["relays"]:
        async_add_entities([LIFXSwitch(coordinator, LIFX_SWITCH, 1), LIFXSwitch(coordinator, LIFX_SWITCH, 2), LIFXSwitch(coordinator, LIFX_SWITCH, 3), LIFXSwitch(coordinator, LIFX_SWITCH, 4)])


class LIFXSwitch(LIFXEntity, SwitchEntity):
    """Representation of a LIFX Switch"""

    def __init__(self, coordinator: LIFXUpdateCoordinator, description: SwitchEntityDescription, relay_index: int) -> None:
        super().__init__(coordinator)
        self.relay_index = relay_index
        self._attr_unique_id = f"{coordinator.serial_number}_{description.key}_{relay_index}"
        self.entity_description = description
    
    @property
    def is_on(self) -> bool:
        return self.coordinator.async_get_rpower(self.relay_index)

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.async_set_rpower(self.relay_index, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_set_rpower(self.relay_index, False)