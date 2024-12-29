import altair as alt
import pandas as pd
#from vega_datasets import data as vega_data
import numpy as np
from sklearn.covariance import EllipticEnvelope
import streamlit as st
#from google.colab import files

st.set_page_config(
    layout="wide"
)
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 2.5em;  /* Ajusta el tamaño de la fuente si es necesario */
        margin-top: 0;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="centered-title">Mass Shooting Incidents Analysis Dashboard</h1>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .centered-subtitle {
        text-align: center;
        font-size: 1.5em;  /* Ajusta el tamaño de la fuente si es necesario */
        margin-top: 0;
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="centered-subtitle">Evolution of Mass Shootings Across US Regions  and  county-level detailed</h1>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 6, 1])  # Adjust column widths for centering




# Heatmap for year selection
year_interval = alt.selection_interval(name="year_interval", encodings=['x'])


# Region selection
region_selection = alt.selection_single(
    fields=['Region'],
    bind='legend',
    name='region_select'
)
# State selection
state_selection = alt.selection_single(
    fields=['State'],
    bind='legend',
    name='state_select'
)


with open("Q1Q3final.html",'r', encoding='utf-8') as f:
    chart_html=f.read()

with col2:
    st.components.v1.html(chart_html,height=1200,width=1200)


# Question2

#read
grouped_data = pd.read_csv('Q2dataset.csv')

year_slider = alt.binding_range(min=2019, max=grouped_data['Year'].max(), step=1, name="Select Year: ")
year_selection = alt.param(name="YearSelect", bind=year_slider, value=2019)

# colorblind-friendly
CB_color_cycle = ['#DC267F', '#FE6100', '#FFB000', '#785EF0', '#648FFF']

lines = alt.Chart(grouped_data).mark_line(point=True).encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Shootings_Per_Citizen:Q', title='Mass Shootings per Citizen'),
    color=alt.Color('Region:N', title='Region', scale=alt.Scale(range=CB_color_cycle)),
    detail='Region:N'
).transform_filter(
    (alt.datum.Year == 2018) | (alt.datum.Year == year_selection)
).add_params(
    year_selection
).properties(
    width=500,
    height=300,
    title='Interactive Slope Chart of Mass Shootings per Citizen by Region'
)

heatmap = alt.Chart(grouped_data).mark_rect().encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Region:N', title='Region'),
    color=alt.Color('Pct_Change:Q', scale=alt.Scale(scheme='redblue', domainMid=0), title='% Change'),
    tooltip=['Region', 'Year', 'Pct_Change']
).transform_filter(
    alt.datum.Year <= year_selection
).add_params(
    year_selection
).properties(
    title="Heatmap of % Change in Shootings per Citizen Compared to 2018",
    width=500,
    height=300
)


combined_chart = alt.hconcat(lines,  heatmap)

st.markdown('<h1 class="centered-subtitle">Change in Mass Shootings Per Capita Across US Regions</h1>', unsafe_allow_html=True)

st.altair_chart(combined_chart, use_container_width=True)




