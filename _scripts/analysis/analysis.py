
import polars as pl
from plan.helpers import create_room_map
from setup.interfaces import CaseData
from helpers.variable_interfaces import all_variables
from setup.data_wrangle import create_dataframe_for_many_cases, join_any_data, create_dataframe_for_case, join_site_data
from helpers.ep_helpers import get_zone_num


def create_zone_vol_df_many(case_data: list[CaseData]):
    vent_vol = all_variables.afn.zone["vent_vol"]
    mix_vol = all_variables.afn.zone["mix_vol"]
    temp = all_variables.zone.temp["zone_mean_air_temp"]

    df = create_dataframe_for_many_cases(case_data, vent_vol)
    df2 = join_any_data(df, case_data, mix_vol)
    return join_any_data(df2, case_data, temp, 1)

def create_zone_rate_df(case: CaseData):
    zq = all_variables.afn.zone
    qois = [zq["vent_heat_gain"], zq["vent_heat_loss"], zq["mix_heat_gain"],zq["mix_heat_loss"]]

    dfs = [create_dataframe_for_case(case.case_name, case.sql, qoi) for qoi in qois]
    return pl.concat(dfs, how="vertical")

    # df = create_dataframe_for_case(case.case_name, case.sql, qois[0])
    # for ix, qoi in enumerate(qois[1:]):
    #     df = join_any_data(df, [case], qoi, ix)
    return df

def create_site_df(case: CaseData):
    sq = all_variables.site
    qois = [sq.temp["db"],sq.solar["direct_rad"],sq.wind["speed"],sq.wind["direction"],]

    dfs = [create_dataframe_for_case(case.case_name, case.sql, qoi) for qoi in qois]
    return pl.concat(dfs, how="vertical")

    df = create_dataframe_for_case(case.case_name, case.sql, qois[0])
    for ix, qoi in enumerate(qois[1:]):
        df = join_site_data(df, case, qoi, ix)
    return df


# df_rate = create_zone_rate_df(sc)
# df_rate.head()

# df_site = create_site_df(sc)
# df_site.head()



def convert_zone_space_name(room_map:dict[int, str], name):
    ix =  get_zone_num(name)
    room_name = room_map[ix]
    label = f"{ix}-{room_name}"
    return label