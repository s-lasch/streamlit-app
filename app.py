import streamlit as st
import streamlit_echarts as se
import pandas as pd
import pyecharts.options as opts
import streamlit_extras.jupyterlite
from pyecharts.charts import Boxplot
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.badges import badge

import plots
from data.data import get_lang_data, get_mode_data

typing = pd.read_csv('data/results.csv', delimiter="|")

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title='Typing Test Analysis')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard `version 2`')

st.sidebar.subheader('Language')
lang = st.sidebar.selectbox('Filter by langauge',
                            options=['All'] + [lang for lang in typing['language'].unique()],
                            format_func=lambda x: (
                                x.replace('_', " ").capitalize() if not x.endswith('1k') else x.split("_")[
                                    0].capitalize()))

st.sidebar.markdown('<br/>', unsafe_allow_html=True)
st.sidebar.subheader('Column')
choose_column = st.sidebar.selectbox('Choose metric',
                                     options=['wpm', 'acc', 'consistency', 'rawWpm'],
                                     format_func=lambda x: 'words per minute' if x == 'wpm'
                                     else 'accuracy' if x == 'acc'
                                     else 'raw words per minute' if x == 'rawWpm'
                                     else x)

st.sidebar.markdown('<br/>', unsafe_allow_html=True)
st.sidebar.subheader('Pie Graph Height')
plot_height = st.sidebar.slider(min_value=200, max_value=600, step=5, value=400, label="Height for the pie charts")

st.sidebar.markdown('<br/>', unsafe_allow_html=True)
st.sidebar.subheader('Box Plot Height')
box_height = st.sidebar.slider(min_value=400, max_value=600, step=5, value=400, label="Height for the box plot")

st.sidebar.markdown(f'''
---
*Created with [streamlit](https://streamlit.io/) by [Steven Lasch](https://steven-lasch.com)*
{badge(type='github', name='s-lasch/streamlit-app')}
''')

# Row A
with open("pages/about.md", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="**`wpm`**: *words per minute*", value=round(typing['wpm'].median(), 1), help='**Median** words typed per minute. Takes `acc` into account.')
col2.metric(label="**`rawWpm`**: *raw words per minute*", value=round(typing['rawWpm'].median(), 1), help='**Median** raw words per minute, without accounting for `acc`.')
col3.metric(label="**`acc`**: *typing accuracy*", value=f"{round(typing['acc'].median(), 1)}%", help='**Median** `acc` (typing accuracy), which is a percentage.')
col4.metric(label="**`consistency`**: *typing speed consistency*", value=f"{round(typing['consistency'].median(),1)}%", help='**Median** `consistency`, which is a percentage.')

style_metric_cards(border_left_color="#FF4B4B")

st.markdown("---")

# Row B
c1, c2 = st.columns((5, 5))
with c1:
    st.markdown("""### <center>Language Distribution</center>""", unsafe_allow_html=True)
    se.st_echarts(get_lang_data(typing), renderer='svg', height=plot_height)

with c2:
    st.markdown("""### <center>Typing Test Modes</center>""", unsafe_allow_html=True)
    se.st_echarts(get_mode_data(typing, lang=lang), renderer='svg', height=plot_height)

st.markdown('<br/>', unsafe_allow_html=True)

# Row C
st.markdown('### <center>Box Plot</center>', unsafe_allow_html=True)
# se.st_echarts(get_mode_data(typing, choose_column, lang)[1], renderer='svg', height=box_height)

box_typing = plots.filter_language(typing, lang)

data = [box_typing[choose_column][box_typing['mode'] == 'time'].to_list(),
        box_typing[choose_column][box_typing['mode'] == 'words'].to_list(),
        box_typing[choose_column][box_typing['mode'] == 'quote'].to_list(),
        box_typing[choose_column][box_typing['mode'] == 'custom'].to_list(),
        box_typing[choose_column][box_typing['mode'] == 'zen'].to_list()]

x_axis = list(['time', 'words', 'quote', 'custom', 'zen'])

# Create Boxplot instance
boxplot = (
    Boxplot()
    .set_series_opts(colors=plots.color_discrete_sequence)
    .add_xaxis(x_axis)
    .add_yaxis(
        series_name="",
        y_axis=data,
        yaxis_index=0,
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(type_="value", name=f'{"accuracy" if choose_column == "acc" else "raw wpm" if choose_column == "rawWpm" else choose_column}')
    )
)
se.st_pyecharts(boxplot, renderer='svg', height=box_height)
