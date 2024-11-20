import polars as pl


def split_by_case_type(df):
    return df.with_columns(
        case_type=pl.when(pl.col("case_names").str.contains("amb"))
        .then(pl.lit("amb"))
        .when(pl.col("case_names").str.contains("bol"))
        .then(pl.lit("bol"))
        .otherwise(pl.lit("red"))
    )


def split_by_materials(df):
    return df.with_columns(
        exp_type=pl.when(pl.col("case_names").str.contains("Light"))
        .then(pl.lit("Light"))
        .when(pl.col("case_names").str.contains("Medium"))
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("Heavy"))
    )


def split_by_doors(df):
    return df.with_columns(
        exp_type=pl.when(pl.col("case_names").str.contains("CLOSED"))
        .then(pl.lit("CLOSED"))
        .when(pl.col("case_names").str.contains("DYNAMIC"))
        .then(pl.lit("DYNAMIC"))
        .otherwise(pl.lit("OPEN"))
    )


def split_by_windows(df):
    return df.with_columns(
        exp_type=pl.when(pl.col("case_names").str.contains("1.3"))
        .then(pl.lit("+30%"))
        .when(pl.col("case_names").str.contains("0.7"))
        .then(pl.lit("-30%"))
        .otherwise(pl.lit("Control"))
    )




