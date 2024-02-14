import streamlit as st
import streamlit_echarts as se
import pandas as pd
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
                            format_func=lambda x: (x.replace('_', " ").split(" ")[0][0].upper()
                                                   + x.replace('_', " ").split(" ")[0][1:]))

st.sidebar.subheader('Column')
choose_column = st.sidebar.selectbox('Choose column',
                                     options=['wpm', 'acc', 'consistency', 'rawWpm'],
                                     format_func=lambda x: 'words per minute' if x == 'wpm'
                                     else 'accuracy' if x == 'acc'
                                     else 'raw words per minute' if x == 'rawWpm'
                                     else x)

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
    se.st_echarts(get_lang_data(typing), renderer='svg', height="400px")

with c2:
    st.markdown("""### <center>Typing Test Modes</center>""", unsafe_allow_html=True)
    se.st_echarts(get_mode_data(typing), renderer='svg', height="400px")

# Row C
st.markdown('### Box Plot')
box = plots.box(typing, col=choose_column, lang=lang)
st.plotly_chart(box, use_container_width=True)
