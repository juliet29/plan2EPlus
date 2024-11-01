

# df = create_pressure_df(sc)
# df1 = df.filter(pl.col("qoi").str.contains("Pressure"))
# g = sns.relplot(df1,x="time", y="values",  col="qoi", hue="room_names", palette="Set1", kind="line", errorbar=None, style="is_ext", dashes=True,)


# for ax in g.axes.flat:
#     ax.xaxis.set_ticks_position("bottom")
#     ax.xaxis.set_major_locator(ticker.AutoLocator())
# g.add_legend(loc="lower right")