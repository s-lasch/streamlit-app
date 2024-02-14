import pandas as pd
import plots

boxplot = {
    "title": [
        {
            "text": '',
            "left": 'center'
        },
        {
            # "text": 'upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR',
            # "borderColor": '#999',
            # "borderWidth": 1,
            # "textStyle": {
            #     "fontWeight": 'normal',
            #     "fontSize": 14,
            #     "lineHeight": 20
            # },
            # "left": '10%',
            # "top": '90%'
        }
    ],
    "dataset": [
        {
            "source": [
                [850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960,
                 960],
                [960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
                [880, 880, 880, 860, 720, 720, 620, 860, 970, 950, 880, 910, 850, 870, 840, 840, 850, 840, 840, 840],
                [890, 810, 810, 820, 800, 770, 760, 740, 750, 760, 910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
                [890, 840, 780, 810, 760, 810, 790, 810, 820, 850, 870, 870, 810, 740, 810, 940, 950, 800, 810, 870]
            ]
        },
        {
            "transform": {
                "type": 'boxplot',
                "config": {"itemNameFormatter": 'expr {value}'}
            }
        },
        {
            "fromDatasetIndex": 1,
            "fromTransformResult": 1
        }
    ],
    "tooltip": {
        "trigger": 'item',
        "axisPointer": {
            "type": 'shadow'
        }
    },
    "grid": {
        "left": '10%',
        "right": '10%',
        "bottom": '15%'
    },
    "xAxis": {
        "type": 'category',
        "boundaryGap": True,
        "nameGap": 30,
        "splitArea": {
            "show": False
        },
        "splitLine": {
            "show": False
        }
    },
    "yAxis": {
        "type": 'value',
        "name": 'km/s minus 299,000',
        "splitArea": {
            "show": True
        }
    },
    "series": [
        {
            "color": plots.color_discrete_sequence,
            "name": 'boxplot',
            "type": 'boxplot',
            "datasetIndex": 1
        },
        {
            "name": 'outlier',
            "type": 'scatter',
            "datasetIndex": 2
        }
    ]
}

pie = {
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
            "color": plots.color_discrete_sequence,
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
             "name": language.replace("_", " \n").capitalize() if not language.endswith('1k') else language.split('_')[
                 0]
             .capitalize()} for language, count in zip(df_pie['language'], df_pie['count'])]

    pie['series'][0]['data'] = data
    pie['series'][0]['color'] = plots.color_discrete_sequence_r
    return pie


def get_mode_data(df, lang='All'):
    df_pie = plots.filter_language(df, lang)
    df_pie = df_pie.groupby('mode')['mode'].count().to_frame().rename(
        columns={'mode': 'count'}).reset_index().sort_values('count', ascending=False)

    data = [{"value": count, "name": mode.capitalize()} for mode, count in zip(df_pie['mode'], df_pie['count'])]

    pie['series'][0]['data'] = data
    pie['series'][0]['color'] = plots.color_discrete_sequence

    return pie, boxplot


if __name__ == "__main__":
    dff = pd.read_csv('results.csv', delimiter='|')
    lang_pie = get_mode_data(dff, 'All')
    print(plots.color_discrete_sequence)
