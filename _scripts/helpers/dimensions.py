from fractions import Fraction
from pint import UnitRegistry
from enum import Enum

class UnitTypes(Enum):
    FEET = 0
    METERS = 1


ureg = UnitRegistry()


def dimension_from_str(dim: str) -> float:
    feet, inches = dim.split(",")
    (feet := float(feet))

    try:
        whole, fract = inches.split(" ")
        (whole := float(whole))
        fract = float(Fraction(fract))

        val = (feet * ureg.foot) + (whole * ureg.inches) + (fract * ureg.inches)
        val = val.to(ureg.meters)# type: ignore
        return val.magnitude  # type: ignore
    except:
        pass

    if "/" in inches:
        inches = float(Fraction(inches))
    else:
        (inches := float(inches))

    val = feet * ureg.foot + float(inches) * ureg.inches
    val = val.to(ureg.meters)# type: ignore
    return val.magnitude  # type: ignore


def nice_dim(dim: str, unit_type: UnitTypes = UnitTypes.FEET) -> float:
    if unit_type == UnitTypes.FEET:
        res = dimension_from_str(dim)
        return round(res, 2)
    else:
        raise Exception("Only Feet unit types are implemented!")
