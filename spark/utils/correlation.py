plt.figure(figsize=(24,23))
sns.heatmap(df.select([c for c in df_select1]).toPandas().corr(),linewidths=0.1,vmax=1.0, square=True, linecolor=’white’, annot=True)
plt.show()
plt.gcf().clear()
