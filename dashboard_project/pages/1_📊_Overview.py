import streamlit as st
import plotly.express as px
import json
from streamlit_extras.add_vertical_space import add_vertical_space

agg_trans = st.session_state['agg_trans_df']
map_trans = st.session_state['map_trans_df']
map_user = st.session_state['map_user_df']

# 1
trans_type_count = agg_trans.groupby('Payment_Type')['Total_Transaction'].sum()
total_trans_count = agg_trans['Total_Transaction'].sum()
trans_type_perc = round(trans_type_count / total_trans_count * 100, 2).reset_index()

trans_type_fig = px.pie(
    trans_type_perc, names='Payment_Type',
    values='Total_Transaction', hole=.65,
    hover_data={'Total_Transaction': False}
)

trans_type_fig.update_layout(width=900, height=500)

# 2
trans_state = agg_trans.groupby('State')['Total_Transaction'].sum().reset_index()
trans_state_sorted = trans_state.sort_values(by='Total_Transaction', ascending=False).head(10)

trans_state_fig = px.bar(
    trans_state_sorted, x='Total_Transaction', y='State', orientation='h',
    text='Total_Transaction', text_auto='.1s',
    labels={'Total_Transaction': 'Transaction Count'}
)

trans_state_fig.update_layout(
    yaxis=dict(autorange="reversed"),
    width=900, height=500
)

# 3
trans_district = map_trans.groupby(['State', 'District'])['Total_Transaction'].sum().reset_index()
trans_district_sorted = trans_district.sort_values(by='Total_Transaction', ascending=False).head(10)

trans_district_fig = px.bar(
    trans_district_sorted, x='Total_Transaction', y='District', orientation='h',
    text='Total_Transaction', text_auto='.1s',
    labels={'Total_Transaction': 'Transaction Count'}
)

trans_district_fig.update_layout(
    yaxis=dict(autorange="reversed"),
    width=900, height=500
)

# 4
user_state = map_user.groupby('State')['Total_Registered_User'].sum().reset_index()

with open(r"csv_files/india_states.json") as f:
    geojson = json.load(f)

if 'geojson' not in st.session_state:
    st.session_state["geojson"] = geojson

user_state_fig = px.choropleth(
    user_state, geojson=geojson,
    locations='State',
    featureidkey='properties.ST_NM',
    color='Total_Registered_User', projection='orthographic',
    labels={'Total_Registered_User': "Registered Users"},
    color_continuous_scale='blues'
)

user_state_fig.update_geos(fitbounds='locations', visible=False)
user_state_fig.update_layout(height=600, width=900)


# Page Development

st.set_page_config(page_title="Overview", page_icon="Images_and_logo/Logo.png", layout="wide")


with st.container():
    st.title('📊 Overview')
    add_vertical_space(2)

with st.container():
    st.subheader("Transaction Breakdown by Payment Type")
    st.plotly_chart(trans_type_fig, use_container_width=True)
    add_vertical_space(2)

with st.container():
    st.subheader("Transaction Breakdown by State")
    state_desc = "Here are the Top State with the Highest Transaction Count"
    st.markdown(f"<p style='text-align: center;'><strong>{state_desc}</strong></p>", unsafe_allow_html=True)
    st.plotly_chart(trans_state_fig, use_container_width=True)
    add_vertical_space(2)

with st.container():
    st.subheader("Transaction Breakdown by District")
    district_desc = "Here are the Top District with the Highest Transaction Count"
    st.markdown(f"<p style='text-align: center;'><strong>{district_desc}</strong></p>", unsafe_allow_html=True)
    st.plotly_chart(trans_district_fig, use_container_width=True)
    add_vertical_space(2)

with st.container():
    st.subheader("Total Registered User by State")
    st.plotly_chart(user_state_fig, use_container_width=True)
    add_vertical_space(2)

