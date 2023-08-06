"""Describe objects for cozytouch."""
import logging

from ..constant import DeviceCommand as dc
from ..constant import DeviceState as ds
from ..constant import DeviceType as dt
from ..constant import ModeState, OnOffState, ThermalState
from ..exception import CozytouchException
from .device import CozytouchDevice

logger = logging.getLogger(__name__)


class CozytouchClimate(CozytouchDevice):
    """APC Heating And Cooling Zone."""

    @property
    def name(self):
        """Name."""
        return self.data["label"]

    @property
    def is_on(self):
        """Climate is on."""
        return self.operating_mode != ModeState.STOP

    @property
    def is_away(self):
        """Heater is away."""
        return self.operating_mode == ModeState.AWAY

    @property
    def is_heating(self):
        """Climate is heating."""
        return self.get_state(ds.PASS_APC_HEATING_MODE_STATE) == OnOffState.ON

    @property
    def is_cooling(self):
        """Climate is cooling."""
        return self.get_state(ds.PASS_APC_COOLING_MODE_STATE) == OnOffState.ON

    @property
    def temperature(self):
        """Return temperature."""
        sensor = self.get_sensors(dt.PASS_APC_ZONE_TEMP, {})
        if hasattr(sensor, "temperature"):
            return sensor.temperature
        return None

    @property
    def target_temperature(self):
        """Return target temperature."""
        return self.get_state(ds.TARGET_TEMPERATURE_STATE)

    @property
    def target_comfort_temperature(self):
        """Return comfort temperature."""
        return self.get_state(ds.COMFORT_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def target_comfort_cooling_temperature(self):
        """Return cooling comfort temperature."""
        return self.get_state(ds.COMFORT_COOLING_TARGET_TEMPERATURE_STATE)

    @property
    def target_eco_temperature(self):
        """Return economic temperature."""
        return self.get_state(ds.ECO_HEATING_TARGET_TEMPERATURE_STATE)

    @property
    def target_eco_cooling_temperature(self):
        """Return cooling economic temperature."""
        return self.get_state(ds.ECO_COOLING_TARGET_TEMPERATURE_STATE)

    @property
    def operating_mode(self):
        """Return operating mode."""
        return self.get_state(ds.THERMAL_CONFIGURATION_STATE)

    @property
    def operating_mode_list(self):
        """Return Operating mode list."""
        return self.get_definition(ds.THERMAL_CONFIGURATION_STATE)

    @property
    def preset_mode(self):
        """Return operation mode."""
        return self.get_state(ds.PASS_APC_HEATING_MODE_STATE)

    @property
    def preset_cooling_mode(self):
        """Return operation mode."""
        return self.get_state(ds.PASS_APC_COOLING_MODE_STATE)

    @property
    def preset_mode_list(self):
        """Return preset mode list."""
        return self.get_definition(ds.PASS_APC_HEATING_MODE_STATE)

    @property
    def preset_cooling_mode_list(self):
        """Return operating mode list."""
        return self.get_definition(ds.PASS_APC_COOLING_MODE_STATE)

    @property
    def supported_states(self) -> dict:
        """Supported states."""
        supported_states = [state["name"] for state in self.states]
        for sensor in self.sensors:
            sensor_states = [state["name"] for state in sensor.states]
            supported_states = list(set(supported_states + sensor_states))
        return supported_states

    def is_state_supported(self, state):
        """Is supported ."""
        return state in self.supported_states

    async def set_operating_mode(self, thermal_mode):
        """Set thermal state (HVAC Mode Heat/Cool/HeatAndCool)."""
        mode_state = ds.HEATING_ON_OFF_STATE
        thermal_state = ds.THERMAL_CONFIGURATION_STATE
        if thermal_mode == ThermalState.HEAT:
            actions = [
                (dc.SET_HEATING_ON_OFF_STATE, OnOffState.ON),
                (dc.SET_COOLING_ON_OFF_STATE, OnOffState.OFF),
                (dc.REFRESH_PASS_APC_HEATING_MODE, None),
                (dc.REFRESH_PASS_APC_COOLING_MODE, None),
            ]
        elif thermal_mode == ThermalState.COOL:
            actions = [
                (dc.SET_HEATING_ON_OFF_STATE, OnOffState.OFF),
                (dc.SET_COOLING_ON_OFF_STATE, OnOffState.ON),
                (dc.REFRESH_PASS_APC_HEATING_MODE, None),
                (dc.REFRESH_PASS_APC_COOLING_MODE, None),
            ]
        elif thermal_mode == ThermalState.HEATCOOL:
            actions = [
                (dc.SET_HEATING_ON_OFF_STATE, OnOffState.ON),
                (dc.SET_COOLING_ON_OFF_STATE, OnOffState.ON),
                (dc.REFRESH_PASS_APC_HEATING_MODE, None),
                (dc.REFRESH_PASS_APC_COOLING_MODE, None),
            ]
        elif self.widget == dt.APC_HEATING_ZONE:
            mode_state = ds.PASS_APC_HEATING_MODE_STATE
            actions = [
                (dc.SET_PASS_APC_HEATING_MODE, thermal_mode),
                (dc.REFRESH_PASS_APC_HEATING_MODE, None),
            ]
        await self.set_mode(mode_state, actions)
        self.set_state(thermal_state, thermal_mode)

    async def set_preset_mode(self, mode, thermal_mode=ThermalState.HEAT):
        """Set operating mode (Preset Mode)."""
        if thermal_mode in [ThermalState.HEAT, ThermalState.HEATCOOL]:
            mode_state = ds.PASS_APC_HEATING_MODE_STATE
            actions = [
                (dc.SET_PASS_APC_HEATING_MODE, mode),
                (dc.REFRESH_PASS_APC_HEATING_MODE, None),
            ]
            await self.set_mode(mode_state, actions)
            self.set_state(mode_state, mode)

        if thermal_mode in [ThermalState.COOL, ThermalState.HEATCOOL]:
            mode_state = ds.PASS_APC_COOLING_MODE_STATE
            actions = [
                (dc.SET_PASS_APC_COOLING_MODE, mode),
                (dc.REFRESH_PASS_APC_COOLING_MODE, None),
            ]
            await self.set_mode(mode_state, actions)
            self.set_state(mode_state, mode)

    async def set_eco_temperature(self, temperature, thermal_mode=ThermalState.HEAT):
        """Set eco temperature."""
        if thermal_mode == ThermalState.HEAT:
            mode_state = ds.ECO_HEATING_TARGET_TEMPERATURE_STATE
            actions = [
                (dc.SET_ECO_HEATING_TARGET_TEMPERATURE, temperature),
                (dc.REFRESH_ECO_HEATING_TARGET_TEMPERATURE, None),
            ]
        elif thermal_mode == ThermalState.COOL:
            mode_state = ds.ECO_COOLING_TARGET_TEMPERATURE_STATE
            actions = [
                (dc.SET_ECO_COOLING_TARGET_TEMPERATURE, temperature),
                (dc.REFRESH_ECO_COOLING_TARGET_TEMPERATURE, None),
            ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_comfort_temperature(
        self, temperature, thermal_mode=ThermalState.HEAT
    ):
        """Set comfort temperature."""
        if thermal_mode == ThermalState.HEAT:
            mode_state = ds.COMFORT_HEATING_TARGET_TEMPERATURE_STATE
            actions = [
                (dc.SET_COMFORT_HEATING_TARGET_TEMPERATURE, temperature),
                (dc.REFRESH_COMFORT_HEATING_TARGET_TEMPERATURE, None),
            ]
        elif thermal_mode == ThermalState.COOL:
            mode_state = ds.COMFORT_COOLING_TARGET_TEMPERATURE_STATE
            actions = [
                (dc.SET_COMFORT_COOLING_TARGET_TEMPERATURE, temperature),
                (dc.REFRESH_COMFORT_COOLING_TARGET_TEMPERATURE, None),
            ]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_derogated_temperature(self, temperature: float):
        """Set derogate temp."""
        mode_state = ds.DEROGATION_ON_OFF_STATE
        actions = [(dc.SET_DEROGATED_TARGET_TEMP, temperature)]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, temperature)

    async def set_derogated_mode(self, mode: OnOffState):
        """Set away mode off."""
        mode_state = ds.DEROGATION_ON_OFF_STATE
        actions = [(dc.SET_DEROGATION_ON_OFF_STATE, mode)]
        await self.set_mode(mode_state, actions)
        self.set_state(mode_state, mode)

    async def turn_derogated_on(self):
        """Turn derogated on."""
        await self.set_derogated_mode(OnOffState.ON)

    async def turn_derogated_off(self):
        """Turn derogated on."""
        await self.set_derogated_mode(OnOffState.OFF)

    async def turn_away_mode_on(self):
        """Turn on away mode."""
        self.set_operating_mode(ModeState.AWAY)

    async def turn_away_mode_off(self):
        """Turn off away mode."""
        self.set_operating_mode(ModeState.AUTO)

    async def turn_on(self, thermal_mode=ThermalState.HEAT):
        """Set on."""
        if thermal_mode == ThermalState.HEAT:
            mode_state = ds.HEATING_ON_OFF_STATE
            actions = [(dc.SET_HEATING_ON_OFF_STATE, OnOffState.ON)]
        elif thermal_mode == ThermalState.COOL:
            mode_state = ds.COOLING_ON_OFF_STATE
            actions = [(dc.SET_COOLING_ON_OFF_STATE, OnOffState.ON)]
        await self.set_mode(mode_state, actions)

    async def turn_off(self, thermal_mode=ThermalState.HEAT):
        """Set off."""
        if thermal_mode == ThermalState.HEAT:
            mode_state = ds.HEATING_ON_OFF_STATE
            actions = [(dc.SET_HEATING_ON_OFF_STATE, OnOffState.OFF)]
        elif thermal_mode == ThermalState.COOL:
            mode_state = ds.COOLING_ON_OFF_STATE
            actions = [(dc.SET_COOLING_ON_OFF_STATE, OnOffState.OFF)]
        await self.set_mode(mode_state, actions)

    async def update(self):
        """Update heater device."""
        if self.client is None:
            raise CozytouchException("Unable to update climate")
        for sensor in self.sensors:
            logger.debug("Climate : Update sensor")
            await sensor.update()
        await super(CozytouchClimate, self).update()
