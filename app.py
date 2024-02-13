import streamlit as st
import pandas as pd
import plots

typing = pd.read_csv('data/results.csv', delimiter="|")

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

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
# col1, col2, col3 = st.columns(3)
# col1.metric("Temperature", "70 °F", "1.2 °F")
# col2.metric("Wind", "9 mph", "-8%")
# col3.metric("Humidity", "86%", "4%")

# Row B
c1, c2 = st.columns((5, 5))
with c1:
    st.markdown('### Language Distribution')
    lang_pie = plots.lang_pie(typing, height=400, width=400)
    st.plotly_chart(lang_pie, use_container_width=True)

with c2:
    st.markdown('### Typing Test Modes')
    pie = plots.pie(typing, lang=lang, height=400, width=400)
    st.plotly_chart(pie, use_container_width=True)

# Row C
st.markdown('### Box Plot')
box = plots.box(typing, col=choose_column, lang=lang)
st.plotly_chart(box, use_container_width=True)
