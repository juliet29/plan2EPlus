from fractions import Fraction
from pint import UnitRegistry

ureg = UnitRegistry()


def dimension_from_str(dim: str) -> float:
    feet, inches = dim.split(",")
    (feet := float(feet))

    try:
        whole, fract = inches.split(" ")
        (whole := float(whole))
        fract = float(Fraction(fract))

        val = (feet * ureg.foot) + (whole * ureg.inches) + (fract * ureg.inches)
        return val.magnitude  # type: ignore
    except:
        pass

    if "/" in inches:
        inches = float(Fraction(inches))
    else:
        (inches := float(inches))

    val = feet * ureg.foot + float(inches) * ureg.inches
    return val.magnitude  # type: ignore


def nice_dim(dim: str) -> float:
    res = dimension_from_str(dim)
    return round(res, 2)
