"""Support for Xiaomi Aqara binary sensors."""
import logging

from homeassistant.components.switch import SwitchDevice

from . import PY_XIAOMI_GATEWAY, XiaomiDevice

_LOGGER = logging.getLogger(__name__)

# Load power in watts (W)
ATTR_LOAD_POWER = "load_power"

# Total (lifetime) power consumption in watts
ATTR_POWER_CONSUMED = "power_consumed"
ATTR_IN_USE = "in_use"

LOAD_POWER = "load_power"
POWER_CONSUMED = "power_consumed"
ENERGY_CONSUMED = "energy_consumed"
IN_USE = "inuse"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Perform the setup for Xiaomi devices."""
    devices = []
    for (_, gateway) in hass.data[PY_XIAOMI_GATEWAY].gateways.items():
        for device in gateway.devices["switch"]:
            model = device["model"]
            if model == "plug":
                if "proto" not in device or int(device["proto"][0:1]) == 1:
                    data_key = "status"
                else:
                    data_key = "channel_0"
                devices.append(
                    XiaomiGenericSwitch(device, "Plug", data_key, True, gateway)
                )
            elif model in ["ctrl_neutral1", "ctrl_neutral1.aq1"]:
                devices.append(
                    XiaomiGenericSwitch(
                        device, "Wall Switch", "channel_0", False, gateway
                    )
                )
            elif model in ["ctrl_ln1", "ctrl_ln1.aq1"]:
                devices.append(
                    XiaomiGenericSwitch(
                        device, "Wall Switch LN", "channel_0", False, gateway
                    )
                )
            elif model in ["ctrl_neutral2", "ctrl_neutral2.aq1"]:
                devices.append(
                    XiaomiGenericSwitch(
                        device, "Wall Switch Left", "channel_0", False, gateway
                    )
                )
                devices.append(
                    XiaomiGenericSwitch(
                        device, "Wall Switch Right", "channel_1", False, gateway
                    )
                )
            elif model in ["ctrl_ln2", "ctrl_ln2.aq1"]:
                devices.append(
                    XiaomiGenericSwitch(
                        device, "Wall Switch LN Left", "channel_0", False, gateway
                    )
                )
                devices.append(
                    XiaomiGenericSwitch(
                        device, "Wall Switch LN Right", "channel_1", False, gateway
                    )
                )
            elif model in ["86plug", "ctrl_86plug", "ctrl_86plug.aq1"]:
                if "proto" not in device or int(device["proto"][0:1]) == 1:
                    data_key = "status"
                else:
                    data_key = "channel_0"
                devices.append(
                    XiaomiGenericSwitch(device, "Wall Plug", data_key, True, gateway)
                )

    # add gateway internal switches
    devices.append(
        XiaomiGatewayRadioSwitch(gateway)
    )
    _LOGGER.debug("Add test switch to entities")
    add_entities(devices)


class XiaomiGenericSwitch(XiaomiDevice, SwitchDevice):
    """Representation of a XiaomiPlug."""

    def __init__(self, device, name, data_key, supports_power_consumption, xiaomi_hub):
        """Initialize the XiaomiPlug."""
        self._data_key = data_key
        self._in_use = None
        self._load_power = None
        self._power_consumed = None
        self._supports_power_consumption = supports_power_consumption
        XiaomiDevice.__init__(self, device, name, xiaomi_hub)

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        if self._data_key == "status":
            return "mdi:power-plug"
        return "mdi:power-socket"

    @property
    def is_on(self):
        """Return true if it is on."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self._supports_power_consumption:
            attrs = {
                ATTR_IN_USE: self._in_use,
                ATTR_LOAD_POWER: self._load_power,
                ATTR_POWER_CONSUMED: self._power_consumed,
            }
        else:
            attrs = {}
        attrs.update(super().device_state_attributes)
        return attrs

    @property
    def should_poll(self):
        """Return the polling state. Polling needed for Zigbee plug only."""
        return self._supports_power_consumption

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        if self._write_to_hub(self._sid, **{self._data_key: "on"}):
            self._state = True
            self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        if self._write_to_hub(self._sid, **{self._data_key: "off"}):
            self._state = False
            self.schedule_update_ha_state()

    def parse_data(self, data, raw_data):
        """Parse data sent by gateway."""
        if IN_USE in data:
            self._in_use = int(data[IN_USE])
            if not self._in_use:
                self._load_power = 0

        for key in [POWER_CONSUMED, ENERGY_CONSUMED]:
            if key in data:
                self._power_consumed = round(float(data[key]), 2)
                break

        if LOAD_POWER in data:
            self._load_power = round(float(data[LOAD_POWER]), 2)

        value = data.get(self._data_key)
        if value not in ["on", "off"]:
            return False

        state = value == "on"
        if self._state == state:
            return False
        self._state = state
        return True

    def update(self):
        """Get data from hub."""
        _LOGGER.debug("Update data from hub: %s", self._name)
        self._get_from_hub(self._sid)


class XiaomiGatewayGenericSwitch(SwitchDevice):
    """Internal gateway services switch representation"""

    def __init__(self, xiaomi_hub):
        """init switch"""
        self._state = None
        self._name = None
        self.miio = xiaomi_hub.miio

        """Return the gateway attributes."""
        miio_info = self.miio.info()
        self._gw_attrs = {
            "model": miio_info.data.get("model"),
            "miio_token": miio_info.data.get("token"),
            "ip": miio_info.network_interface.get("localIp")
        }

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def is_on(self):
        """Return true if it is on."""
        return self._state

    @property
    def should_poll(self):
        """Return the polling state. """
        return True


class XiaomiGatewayRadioSwitch(XiaomiGatewayGenericSwitch):
    """Xiaomi Gateway Radio Switch"""

    def __init__(self, xiaomi_hub):
        super().__init__(xiaomi_hub)
        self._name = f"gateway_radio_{xiaomi_hub.sid}"
        self._volume = None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return "mdi:radio"

    @property
    def device_state_attributes(self):
        """Add Radio Volume to the state attributes."""
        return {
            "volume": self._volume,
            **self._gw_attrs
            }

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        if 'ok' in self.miio.raw_command('play_fm', ["on"]):
            self._state = True
        _LOGGER.debug(f"{self._name} Radio ON")

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        if 'ok' in self.miio.raw_command('play_fm', ["off"]):
            self._state = False
        _LOGGER.debug(f"{self._name} Radio OFF")

    def update(self):
        """Get data from hub."""
        _LOGGER.debug("Update data from hub: %s", self._name)
        resp = self.miio.raw_command("get_prop_fm", [])
        self._volume = resp.get("current_volume")
        self._state = resp.get("current_status") == 'run'


