from math import log, sin, cos, pow, radians

# TO DO, read this paper, how did they fit this? 
# inc_rad => indident angle in radians, ~ angle between wind direction and and outward normal of wall under consideration.. 
# side_ratio_fac => log(width of facade / width of adjacent facade)
def calc_cp(inc_angle, side_ratio_fac=log(1)):
    # TODO check that side_ratio_fac falls within bounds.. 
    inc_rad = radians(inc_angle)
    cos_inc_rad_over_2 = cos(inc_rad / 2)
    val = 0.6 * log(
        1.248
        - 0.703 * sin(inc_rad / 2.0)
        - 1.175 * pow(sin(inc_rad), 2)
        + 0.131 * pow(sin(2.0 * inc_rad * side_ratio_fac), 3)
        + 0.769 * cos_inc_rad_over_2
        + 0.07 * pow((side_ratio_fac * sin(inc_rad / 2.0)), 2)
        + 0.717 * pow(cos_inc_rad_over_2, 2)
    )
    return val

# side ratios are capped at a certain value.. 
# how does Cp become pressure? 