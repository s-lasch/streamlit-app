import pandas as pd
import plots

pie = {
    "tooltip": {
        "trigger": 'item'
    },
    "legend": {
        "orient": "vertical",
        # "right": 20,
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
            "data": []
        }
    ]
}


def get_lang_data(df):
    # language pie chart data
    df_pie = df.groupby('language')['language'].count().to_frame().rename(
        columns={'language': 'count'}).reset_index().sort_values('count', ascending=False)
    data = [{"value": count,
             "name": language.replace("_", " ").capitalize() if not language.endswith('1k') else language.split('_')[0]
             .capitalize()} for language, count in zip(df_pie['language'], df_pie['count'])]

    pie['series'][0]['data'] = data
    return pie


def get_mode_data(df, lang='All'):
    df_pie = plots.filter_language(df, lang)
    df_pie = df_pie.groupby('mode')['mode'].count().to_frame().rename(
        columns={'mode': 'count'}).reset_index().sort_values('count', ascending=False)

    data = [{"value": count, "name": mode.capitalize()} for mode, count in zip(df_pie['mode'], df_pie['count'])]

    mode_data = pie['series'][0]['data'] = data
    return pie


if __name__ == "__main__":
    dff = pd.read_csv('results.csv', delimiter='|')
    lang_pie = get_mode_data(dff, 'All')
    print(lang_pie)
