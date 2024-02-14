import streamlit as st
import streamlit_echarts as se
import plots
import pandas as pd

from data.data import get_lang_data, get_mode_data


typing = pd.read_csv('data/results.csv', delimiter="|")

st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_title='Typing Test Analysis')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard `version 2`')

st.sidebar.subheader('Language')
lang = st.sidebar.selectbox('Filter by langauge',
                            options=['All'] + [lang for lang in typing['language'].unique()],
                            format_func=lambda x: (x.replace('_', " ").capitalize() if not x.endswith('1k') else x.split("_")[0].capitalize()))

st.sidebar.markdown('<br/>', unsafe_allow_html=True)
st.sidebar.subheader('Column')
choose_column = st.sidebar.selectbox('Choose column',
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

st.sidebar.markdown('''
---
*Created with [streamlit](https://streamlit.io/) by [Steven Lasch](https://steven-lasch.com)*
''')

# Row A
with open("pages/about.md", "r") as f:
    st.markdown(f.read(), unsafe_allow_html=True)


# Row B
c1, c2 = st.columns((5, 5))
with c1:
    st.markdown("""### <center>Language Distribution</center>""", unsafe_allow_html=True)
    se.st_echarts(get_lang_data(typing), renderer='svg', height=plot_height)

with c2:
    st.markdown("""### <center>Typing Test Modes</center>""", unsafe_allow_html=True)
    se.st_echarts(get_mode_data(typing, lang)[0], renderer='svg', height=plot_height)

st.markdown('<br/>', unsafe_allow_html=True)

# Row C
st.markdown('### Box Plot')
se.st_echarts(get_mode_data(typing, lang)[1], renderer='svg', height=box_height)
