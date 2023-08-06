import re
from enum import Enum

from enstadtpfaff_platform_mock_api import Event
from enstadtpfaff_platform_mock_api.util import TopicUtil


class Category(Enum):
    INDOOR_CLIMATE = "indoor-climate"
    LIGHTING = "lighting"
    RADIATION = "radiation"
    WINDOW = "window"
    UNIT_DOOR = "unit-door"
    BALCONY_DOOR = "balcony-door"
    ELECTRICITY = "electricity"
    PRESENCE = "presence"
    BLIND = "blind"
    GATE = "gate"
    SOCKET = "socket"
    MISC = "misc"


class ThermostatMode(Enum):
    OFF = 'OFF'
    ON = 'ON'
    HEAT = 'HEAT'
    COOL = 'COOL'
    AUTO = 'AUTO'


# noinspection PyPep8Naming
class IndoorClimate:
    def __init__(
            self,
            currentTemperature: float = None,
            targetTemperature: float = None,
            relativeHumidity: int = None,
            pressure: float = None,
            thermostatMode: ThermostatMode = None,
            currentHeatingPower: float = None,
            currentCoolingPower: float = None
    ):
        self.currentTemperature = currentTemperature
        self.targetTemperature = targetTemperature
        self.relativeHumidity = relativeHumidity
        self.pressure = pressure
        self.thermostatMode = None if thermostatMode is None else thermostatMode.value
        self.currentHeatingPower = currentHeatingPower
        self.currentCoolingPower = currentCoolingPower


class OnOffState(Enum):
    OFF = "OFF"
    ON = "ON"


# noinspection PyPep8Naming
class Lighting:
    def __init__(
            self,
            dimmingLevel: int = None,
            color: tuple = None,
            colorTemperature: float = None,
            state: OnOffState = None
    ):
        if color is not None:
            if len(color) != 4:
                raise ValueError("invalid color")
            if color[0] < 0 or color[0] > 255:
                raise ValueError("invalid color")
            if color[1] < 0 or color[1] > 255:
                raise ValueError("invalid color")
            if color[2] < 0 or color[2] > 255:
                raise ValueError("invalid color")
            if color[3] < 0 or color[3] > 255:
                raise ValueError("invalid color")
        self.dimmingLevel = dimmingLevel
        self.color = color
        self.colorTemperature = colorTemperature
        self.state = None if state is None else state.value


# noinspection PyPep8Naming
class Radiation:
    def __init__(
            self,
            uvIndex: int = None,
            brightness: float = None
    ):
        self.uvIndex = uvIndex
        self.brightness = brightness


class OpeningState(Enum):
    LOCKED = "LOCKED"
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    TILTED = "TILTED"


# noinspection PyPep8Naming
class Window:
    def __init__(
            self,
            openingState: OpeningState = None,
    ):
        self.openingState = None if openingState is None else openingState.value


# noinspection PyPep8Naming
class UnitDoor:
    def __init__(
            self,
            openingState: OpeningState = None
    ):
        self.openingState = None if openingState is None else openingState.value


# noinspection PyPep8Naming
class BalconyDoor:
    def __init__(
            self,
            openingState: OpeningState = None
    ):
        self.openingState = None if openingState is None else openingState.value


# noinspection PyPep8Naming
class Electricity:
    def __init__(
            self,
            currentPower: float = None,
            current: float = None,
            voltage: float = None
    ):
        self.currentPower = currentPower
        self.current = current
        self.voltage = voltage


# noinspection PyPep8Naming
class Presence:
    def __init__(
            self,
            presenceDetected: bool = None,
            presenceAmount: int = None
    ):
        self.presenceDetected = presenceDetected
        self.presenceAmount = presenceAmount


class MovementMode(Enum):
    OPENING = "OPENING"
    CLOSING = "CLOSING"
    IDLE = "IDLE"


# noinspection PyPep8Naming
class Blind:
    def __init__(
            self,
            blindLevel: int = None,
            movementMode: MovementMode = None,
            blindAngle: float = None
    ):
        self.blindLevel = blindLevel
        self.movementMode = None if movementMode is None else movementMode.value
        self.blindAngle = blindAngle


# noinspection PyPep8Naming
class Gate:
    def __init__(
            self,
            openingState: OpeningState = None,
            movementMode: MovementMode = None,
    ):
        self.openingState = None if openingState is None else openingState.value
        self.movementMode = None if movementMode is None else movementMode.value


class Socket:
    def __init__(
            self,
            state: OnOffState = None
    ):
        self.state = None if state is None else state.value


class Misc:
    def __init__(
            self,
            state: OnOffState = None
    ):
        self.state = None if state is None else state.value


class SmartHome:
    # TODO apply some more validation...
    SHARED_TOPIC_ID = "smart-home"
    SMART_HOME_TOPIC_LAYOUT = TopicUtil.shared_topic(
        SHARED_TOPIC_ID,
        "{}",  # house-identifier
        "{}",  # floor-identifier
        "{}",  # unit-identifier
        "{}",  # room-identifier
        "{}",  # category-identifier
        "{}"  # device-identifier
    )
    TOPIC_SEGMENT_PATTERN = re.compile("^[a-z0-9-.]+$")

    @staticmethod
    def indoor_climate(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            indoor_climate: IndoorClimate
    ) -> Event:
        payload = {
            'currentTemperature': indoor_climate.currentTemperature,
            'targetTemperature': indoor_climate.targetTemperature,
            'relativeHumidity': indoor_climate.relativeHumidity,
            'pressure': indoor_climate.pressure,
            'thermostatMode': indoor_climate.thermostatMode,
            'currentHeatingPower': indoor_climate.currentHeatingPower,
            'currentCoolingPower': indoor_climate.currentCoolingPower
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.INDOOR_CLIMATE, payload)

    @staticmethod
    def lighting(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            lighting: Lighting
    ) -> Event:
        payload = {
            'dimmingLevel': lighting.dimmingLevel,
            'color': lighting.color,
            'colorTemperature': lighting.colorTemperature,
            'state': lighting.state
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.LIGHTING, payload)

    @staticmethod
    def radiation(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            radiation: Radiation
    ) -> Event:
        payload = {
            'uvIndex': radiation.uvIndex,
            'brightness': radiation.brightness
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.RADIATION, payload)

    @staticmethod
    def window(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            window: Window
    ) -> Event:
        payload = {
            'openingState': window.openingState
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.WINDOW, payload)

    @staticmethod
    def unit_door(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            unit_door: UnitDoor
    ) -> Event:
        payload = {
            'openingState': unit_door.openingState
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.UNIT_DOOR, payload)

    @staticmethod
    def balcony_door(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            balcony_door: BalconyDoor
    ) -> Event:
        payload = {
            'openingState': balcony_door.openingState
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.BALCONY_DOOR, payload)

    @staticmethod
    def electricity(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            electricity: Electricity
    ) -> Event:
        payload = {
            'currentPower': electricity.currentPower,
            'current': electricity.current,
            'voltage': electricity.voltage
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.ELECTRICITY, payload)

    @staticmethod
    def presence(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            presence: Presence
    ) -> Event:
        payload = {
            'presenceDetected': presence.presenceDetected,
            'presenceAmount': presence.presenceAmount
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.PRESENCE, payload)

    @staticmethod
    def blind(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            blind: Blind
    ) -> Event:
        payload = {
            'blindLevel': blind.blindLevel,
            'movementMode': blind.movementMode,
            'blindAngle': blind.blindAngle
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.BLIND, payload)

    @staticmethod
    def gate(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            gate: Gate
    ) -> Event:
        payload = {
            'openingState': gate.openingState,
            'movementMode': gate.movementMode
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.GATE, payload)

    @staticmethod
    def socket(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            socket: Socket
    ) -> Event:
        payload = {
            'state': socket.state
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.SOCKET, payload)

    @staticmethod
    def misc(
            house_identifier: str,
            floor_identifier: str,
            unit_identifier: str,
            room_identifier: str,
            device_identifier: str,
            misc: Misc
    ) -> Event:
        payload = {
            'state': misc.state
        }
        return SmartHome._build_for_category(house_identifier, floor_identifier, unit_identifier, room_identifier,
                                             device_identifier, Category.MISC, payload)

    @staticmethod
    def _build_for_category(house_identifier: str,
                            floor_identifier: str,
                            unit_identifier: str,
                            room_identifier: str,
                            device_identifier: str,
                            category: Category,
                            payload: dict) -> Event:
        if not SmartHome.TOPIC_SEGMENT_PATTERN.match(house_identifier):
            raise ValueError("invalid house_identifier")
        if not SmartHome.TOPIC_SEGMENT_PATTERN.match(floor_identifier):
            raise ValueError("invalid floor_identifier")
        if not SmartHome.TOPIC_SEGMENT_PATTERN.match(unit_identifier):
            raise ValueError("invalid unit_identifier")
        if not SmartHome.TOPIC_SEGMENT_PATTERN.match(room_identifier):
            raise ValueError("invalid room_identifier")
        if not SmartHome.TOPIC_SEGMENT_PATTERN.match(device_identifier):
            raise ValueError("invalid device_identifier")
        if (
                (category is None) or
                (not isinstance(category, Category)) or
                (not SmartHome.TOPIC_SEGMENT_PATTERN.match(category.value))
        ):
            raise ValueError("invalid category")

        if payload is None:
            raise ValueError("invalid payload")

        payload = SmartHome._del_none(payload)  # get rid of None/nulls

        return Event(
            topic=SmartHome.SMART_HOME_TOPIC_LAYOUT.format(
                house_identifier,
                floor_identifier,
                unit_identifier,
                room_identifier,
                category.value,
                device_identifier
            ),
            payload=payload
        )

    @staticmethod
    def _del_none(d):
        """
        Delete keys with the value ``None`` in a dictionary, recursively.
        """
        if not isinstance(d, dict):
            return d
        return dict((k, SmartHome._del_none(v)) for k, v in d.items() if v is not None)
