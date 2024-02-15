import pandas as pd

import plots

boxplot = {
    "title": [
        {
            "text": '',
            "left": 'center'
        },
    ],
    "dataset": [
        {
            "source": []  # this will be changed
        },
        {
            "transform": {
                "type": 'boxplot',
                "config": {"itemNameFormatter": 'mode {value}'}  # this will be changed
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
        "name": '',  # this will be changed
        "splitArea": {
            "show": True
        }
    },
    "series": [
        {
            "color": plots.color_discrete_sequence[0],
            "name": 'boxplot',
            "type": 'boxplot',
            "datasetIndex": 1
        },
        # {
        #     "name": 'outlier',
        #     "type": 'scatter',
        #     "datasetIndex": 2
        # }
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
            "color": plots.color_discrete_sequence,  # this will be changed
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
            "data": []  # this will be changed
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


def get_mode_data(df, col=None, lang='All'):
    # get pie chart data
    df_pie = plots.filter_language(df, lang)
    df_pie = df_pie.groupby('mode')['mode'].count().to_frame().rename(
        columns={'mode': 'count'}).reset_index().sort_values('count', ascending=False)

    data = [{"value": count, "name": mode.capitalize()} for mode, count in zip(df_pie['mode'], df_pie['count'])]

    pie['series'][0]['data'] = data
    pie['series'][0]['color'] = plots.color_discrete_sequence

    if col:
        data = [df[col][df['mode'] == 'time'].to_list(),
                df[col][df['mode'] == 'words'].to_list(),
                df[col][df['mode'] == 'quote'].to_list(),
                df[col][df['mode'] == 'custom'].to_list(),
                df[col][df['mode'] == 'zen'].to_list()]

        x_axis = list(['time', 'words', 'quote', 'custom', 'zen'])

        # Create Boxplot instance
        boxplot = (
            Boxplot()
            .set_series_opts(colors=px.colors.sequential.RdBu[0])
            .add_xaxis(x_axis)
            # .add_yaxis(series_name="", y_axis=l)
            .add_yaxis(
                series_name="",
                y_axis=data,
                # Set y-axis label based on column name
                yaxis_index=0,
                # Set custom colors for each boxplot
                itemstyle_opts=opts.ItemStyleOpts(color=px.colors.sequential.RdBu[0]),  # For column 'A'
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(type_="value", name="wpm"),
                title_opts=opts.TitleOpts(is_show=False, title="Shit")
            )
        )

    return pie, boxplot


if __name__ == "__main__":
    dff = pd.read_csv('results.csv', delimiter='|')
    lang_pie = get_mode_data(dff, col='wpm', lang='All')
    print(lang_pie[1])
