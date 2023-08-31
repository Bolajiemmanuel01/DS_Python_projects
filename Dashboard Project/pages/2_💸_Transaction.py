import streamlit as st
import plotly.express as px
from streamlit_extras.add_vertical_space import add_vertical_space

agg_trans = trans_df = trans_df_2 = st.session_state['agg_trans_df']
map_df = st.session_state['map_trans_df']

states = agg_trans['State'].unique()
years = agg_trans['Year'].unique()
quarters = agg_trans['Quarter'].unique()

if 'states' not in st.session_state:
    st.session_state['states'] = states
if 'years' not in st.session_state:
    st.session_state['years'] = years
if 'quarters' not in st.session_state:
    st.session_state['quarters'] = quarters

# Page Development

st.set_page_config(page_title="Transaction", page_icon="Images_and_logo/Logo.png", layout="wide")

with st.container():
    st.title("💸 Transaction")
    add_vertical_space(2)

with st.container():
    st.subheader('Transaction Value by Payment Type')

    col1, col2, col3 = st.columns([5, 3, 1])

    with col1:
        state1 = st.selectbox('State', states, key='state1')
    with col2:
        year1 = st.selectbox('Year', years, key='year1')
    with col3:
        quarter_options = ["All"] + list(map(str, quarters))
        quarter1 = st.selectbox('Quarter', quarter_options, key='quarter1')

    trans_df = trans_df[(trans_df['State'] == state1) & (trans_df['Year'] == year1)]

    if quarter1 != 'All':
        trans_df = trans_df[(trans_df['Quarter'] == int(quarter1))]

    trans_df = trans_df.sort_values(by='Transaction_Value', ascending=False).reset_index(drop=True)

    suffix1 = " quarters" if quarter1 == 'All' else 'st' if quarter1 == '1' else 'nd' if quarter1 == '2' else 'rd' if quarter1 == '3' else 'th'

    title1 = f"Transaction details for {state1} for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    fig1 = px.bar(
        trans_df, x="Payment_Type", y="Transaction_Value",
        color="Payment_Type",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title=title1,
        labels=dict(Transaction_Value='Transaction Value', Payment_Type='Transaction Type'),
        hover_data={'Quarter': True}
    )

    fig1.update_layout(
        showlegend=False,
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'top'
        },
        width=900, height=500
    )

    st.plotly_chart(fig1, use_container_width=True)

    expander1 = st.expander(label='Detailed View')
    expander1.write(trans_df.loc[:, ['Quarter', 'Payment_Type', 'Transaction_Value']].reset_index(drop=True))
    add_vertical_space(2)

with st.container():
    st.subheader('Transaction Hotspots')

    y_col, q_col, buff = st.columns([2, 1, 4])

    with y_col:
        year2 = st.selectbox('Year', years, key='year2')
    with q_col:
        quarter2 = st.selectbox('Quarter', quarter_options, key='quarter2')

    map_df = map_df[(map_df['Year'] == year2)]

    if quarter2 != 'All':
        map_df = map_df[(map_df['Quarter'] == int(quarter2))]

    suffix2 = " quarters" if quarter2 == 'All' else 'st' if quarter2 == '1' else 'nd' if quarter2 == '2' else 'rd' if quarter2 == '3' else 'th'
    title2 = f"Transaction Hotspot for {quarter2.lower()}{suffix2} {'' if quarter2 == 'All' else 'quarter'} of {year2}"

    fig2 = px.density_mapbox(map_df, lat="Latitude", lon="Longitude",
                             z="Transaction_Value", hover_name="District",
                             hover_data={"Total_Transaction": True, "Transaction_Value": True, 'Quarter': True},
                             title=title2, mapbox_style="open-street-map"
                             # color_discrete_sequence=px.colors.sequential.Plotly3
                             )

    fig2.update_layout(mapbox_style='carto-positron',
                       mapbox_zoom=3.45, mapbox_center={"lat": 20.93684, "lon": 78.96288},
                       geo=dict(scope='asia', projection_type='equirectangular'),
                       title={
                           'x': 0.5,
                           'xanchor': 'center',
                           'y': 0.04,
                           'yanchor': 'bottom',
                           'font': dict(color='black')
                       },
                       margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=900, height=500
                       )

    st.plotly_chart(fig2, use_container_width=True)

    expander2 = st.expander(label='Detailed View')
    expander2.write(map_df.loc[:, ['State', 'District', 'Quarter', 'Transaction_Value']])

    add_vertical_space(2)

with st.container():
    st.subheader('Breakdown For Number of Transaction')

    state_col, year_col, quarter_col = st.columns([5, 3, 1])

    with state_col:
        state3 = st.selectbox('State', states, key='state3')
    with year_col:
        year3 = st.selectbox('Year', years, key='year3')
    with quarter_col:
        quarter3 = st.selectbox('Quarter', quarter_options, key='quarter3')

    trans_df_2 = trans_df_2[(trans_df_2['State'] == state3) & (trans_df_2['Year'] == year3)]

    if quarter3 != 'All':
        trans_df_2 = trans_df_2[(trans_df_2['Quarter'] == int(quarter3))]

    suffix3 = " quarters" if quarter3 == 'All' else 'st' if quarter3 == '1' else 'nd' if quarter3 == '2' else 'rd' if quarter3 == '3' else 'th'
    title3 = f"Number of Transaction in {state3} for {quarter3.lower()}{suffix3} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

    fig3 = px.pie(trans_df_2, names='Payment_Type',
                  values='Total_Transaction', hole=0.65,
                  title=title3)
    fig3.update_layout(width=900, height=500)

    st.plotly_chart(fig3, use_container_width=True)

    expander3 = st.expander(label='Detailed View')
    expander3.write(trans_df_2.loc[:, ['Quarter', 'Payment_Type', 'Total_Transaction']])

    add_vertical_space(2)

# st.data_editor(data=trans_df_2.head(20))
