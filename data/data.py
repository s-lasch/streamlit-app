import pandas as pd

df = pd.read_csv("data/results.csv", delimiter="|")
df_pie = df.groupby('language')['language'].count().to_frame().rename(columns={'language':'count'}).reset_index().sort_values('count', ascending=False)
data = [{"value": count, "name": language.replace("_", " ").capitalize() if not language.endswith('1k') else language.split('_')[0].capitalize()} for language, count in zip(df_pie['language'], df_pie['count'])]


lang_pie = {
  "tooltip": {
    "trigger": 'item'
  },
  "legend": {
    "orient": "vertical",
    "right": 20,
    "bottom": "center"
  },
  "series": [
    {
      "name": 'Tests Taken',
      "type": 'pie',
      "radius": ['40%', '70%'],
      "avoidLabelOverlap": True,
      "itemStyle": {
        "borderRadius": 10,
        "borderColor": '#fff',
        "borderWidth": 1
      },
      "label": {
        "show": False,
        "position": 'center'
      },
      "labelLine": {
        "show": False
      },
      "data": data
    }
  ]
}
