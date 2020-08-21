import logging
from enum import Enum

logger = logging.getLogger(__name__)


class WeatherConditionEnum(Enum):
    STORM = 1
    DRIZZLE = 2
    RAIN = 3
    SNOW = 4
    MIST = 5
    SMOKE = 6
    HAZE = 7
    DUST = 8
    ASH = 9
    SQUALL = 10
    TORNADO = 11
    CLEAR = 12
    CLOUDS = 13
    ATMOSPHERE = 14


class WeatherSubConditionEnum(Enum):
    UNKNOWN = []
    # Storm
    LIGHT_RAIN = [200, 310, 615]
    RAIN = [201, 311, 616]
    HEAVY_RAIN = [202, 312]
    LIGHT = [210, 300, 500, 600]
    NORMAL = [211, 301, 601]
    HEAVY = [212, 302, 502, 602]
    RAGGED = [221]
    LIGHT_DRIZZLE = [230]
    DRIZZLE = [231]
    HEAVY_DRIZZLE = [232]
    # Drizzle
    SHOWER_RAIN = [313]
    HEAVY_SHOWER_RAIN = [314]
    SHOWER = [321, 521, 621]
    # Rain
    MODERATE = [501]
    VERY_HEAVY = [503]
    EXTREME = [504]
    FREEZING = [511]
    LIGHT_SHOWER = [520, 620]
    HEAVY_SHOWER = [522, 622]
    RAGGED_SHOWER = [531]
    # Snow
    SLEET = [611]
    LIGHT_SHOWER_SLEET = [612]
    SHOWER_SLEET = [613]
    # Atmosphere
    MIST = [701]
    SMOKE = [711]
    HAZE = [721]
    WHIRLS = [731]
    FOG = [741]
    SAND = [751]
    DUST = [761]
    ASH = [762]
    SQUALL = [771]
    TORNADO = [781]
    # Clear
    CLEAR = [800]
    # Clouds
    FEW = [801]  # 11-25%
    SCATTERED = [802]  # 25-50%
    BROKEN = [803]  # 51-84%
    OVERCAST = [804]  # 85-100%

    @staticmethod
    def from_code(code: int):
        for _, specific in WeatherSubConditionEnum.__members__.items():
            if code in specific.value:
                return specific
        logger.info('Using fallback enum for code {}'.format(code))
        return WeatherSubConditionEnum.UNKNOWN
