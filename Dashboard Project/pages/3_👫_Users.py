import streamlit as st
import plotly.express as px
from streamlit_extras.add_vertical_space import add_vertical_space

agg_user_df1 = st.session_state['agg_user_df']
map_user_df1 = st.session_state['map_user_df']
top_user_df1 = st.session_state['top_user_dist_df']

states = ['All'] + list(agg_user_df1['State'].unique())
years = ['All'] + list(agg_user_df1['Year'].unique())
quarters = ['All'] + list(agg_user_df1['Quarter'].unique())

st.set_page_config(page_title="Users", page_icon="Images_and_logo/Logo.png", layout="wide")
state_options = states
quarter_option = quarters
year_option = years

with st.container():
    st.title('👫 Users')
    add_vertical_space(2)

with st.container():
    st.subheader('Percentage of Transaction by Phone Brands')

    s_col, y_col, q_col = st.columns([5, 3, 1])

    with s_col:
        state1 = st.selectbox('State', ['All'] + list(agg_user_df1['State'].unique()), key='state1')
        if state1 != 'All':
            agg_user_df1_sorted = agg_user_df1[(agg_user_df1['State'] == state1)]
        else:
            agg_user_df1_sorted = agg_user_df1
    with y_col:
        year1 = st.selectbox('Year', ['All'] + list(agg_user_df1['Year'].unique()), key='year1')
        if year1 != 'All':
            agg_user_df1_sorted = agg_user_df1_sorted[(agg_user_df1_sorted['Year'] == year1)]
        else:
            agg_user_df1_sorted = agg_user_df1_sorted
    with q_col:
        quarter1 = st.selectbox('Quarter', ['All'] + list(agg_user_df1['Quarter'].unique()), key='quarter1')
        if quarter1 != 'All':
            agg_user_df1_sorted = agg_user_df1_sorted[(agg_user_df1_sorted['Quarter'] == int(quarter1))]
        else:
            agg_user_df1_sorted = agg_user_df1_sorted

    suffix1 = " quarters" if quarter1 == 'All' else 'st' if quarter1 == '1' else 'nd' if quarter1 == '2' else 'rd' if quarter1 == '3' else 'th'
    title1 = f"Transaction percentage across {'All States' if state1 == 'All' else state1} for {str(quarter1).lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {'2018 - 2022' if year1 == 'All' else year1}"

    fig1 = px.treemap(
        agg_user_df1_sorted,
        path=['Phone_Brand'],
        values='Registered_user_by_Phone_Brand',
        color='Phone_Brand',
        color_continuous_scale='ylorbr',
        hover_name='Registered_user_by_Phone_Brand'
    )

    fig1.update_layout(
        width=975, height=600,
        margin=dict(l=20, r=20, t=0, b=20),
        title={
            "text": title1,
            'x': 0.45,
            'xanchor': 'center',
            'y': 0.007,
            'yanchor': 'bottom'
        }
    )

    fig1.update_traces(
        hovertemplate=
        '<b>%{label}</b><br>Registered user by Phone Brand: %{value}<extra></extra>'
    )

    st.plotly_chart(fig1, use_container_width=True)

    expander1 = st.expander(label='Detailed View')
    expander1.write(agg_user_df1_sorted.loc[:, ['Year', 'Quarter', 'Phone_Brand', 'Registered_user_by_Phone_Brand']])

    add_vertical_space(2)

with st.container():
    st.subheader('Hotspots of Registered Users - District')

    s_col1, y_col1, q_col1 = st.columns([5, 3, 1])

    with s_col1:
        state2 = st.selectbox('State', ['All'] + list(map_user_df1['State'].unique()), key='state2')
        if state2 != 'All':
            map_user_df1_sorted = map_user_df1[(map_user_df1['State'] == state2)]
        else:
            map_user_df1_sorted = map_user_df1
    with y_col1:
        year2 = st.selectbox('Year', ['All'] + list(map_user_df1['Year'].unique()), key='year2')
        if year2 != 'All':
            map_user_df1_sorted = map_user_df1_sorted[(map_user_df1_sorted['Year'] == year2)]
        else:
            map_user_df1_sorted = map_user_df1_sorted
    with q_col1:
        quarter2 = st.selectbox('Quarter', ['All'] + list(map_user_df1['Quarter'].unique()), key='quarter2')
        if quarter2 != 'All':
            map_user_df1_sorted = map_user_df1_sorted[(map_user_df1_sorted['Quarter'] == int(quarter2))]
        else:
            map_user_df1_sorted = map_user_df1_sorted

    suffix2 = " quarters" if quarter2 == 'All' else 'st' if quarter2 == '1' else 'nd' if quarter2 == '2' else 'rd' if quarter2 == '3' else 'th'
    title2 = f"Registered Users across {'All States' if state2 == 'All' else state2} for {str(quarter2).lower()}{suffix2} {'' if quarter2 == 'All' else 'quarter'} of {'2018 - 2022' if year2 == 'All' else year2}"

    fig2 = px.scatter_mapbox(
        map_user_df1_sorted,
        lat='Latitude',
        lon='Longitude',
        size='Total_Registered_User',
        hover_name='District',
        hover_data={'State': True, 'Quarter': True},
        title=title2,
        color_discrete_sequence=px.colors.sequential.Greens_r
    )

    fig2.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=3.5, mapbox_center={"lat": 20.93684, "lon": 78.96288},
        geo=dict(scope='asia', projection_type='equirectangular'),
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.05,
            'yanchor': 'bottom',
            'font': dict(color='black')
        },
        height=600, width=900,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(fig2, use_container_width=True)

    expander2 = st.expander(label='Detailed View')
    expander2.write(map_user_df1_sorted.loc[:, ['Quarter', 'District', 'Total_Registered_User']].reset_index(drop=True))

    add_vertical_space(2)

with st.container():
    st.subheader('Top District by Registered Users')

    s_col2, y_col3, buff = st.columns([5, 3, 5])

    with s_col2:
        state3 = st.selectbox('State', ['All'] + list(top_user_df1['State'].unique()), key='state3')
        if state3 != 'All':
            top_user_df1_sorted = top_user_df1[(top_user_df1['State'] == state3)]
        else:
            top_user_df1_sorted = top_user_df1
    with y_col3:
        year3 = st.selectbox('Year', ['All'] + list(top_user_df1['Year'].unique()), key='year3')
        if year3 != 'All':
            top_user_df1_sorted = top_user_df1_sorted[(top_user_df1_sorted['Year'] == year3)]
        else:
            top_user_df1_sorted = top_user_df1_sorted

    aggregation_functions = {'Registered_Users': 'sum',  # Sum the 'Registered_Users' column
                             'Latitude': 'first',  # Keep the first value of 'Latitude'
                             'Longitude': 'first'}  # Keep the first value of 'Longitude'

    top_user_df1_sorted = top_user_df1_sorted.groupby('District').agg(aggregation_functions).reset_index()
    top_user_df1_sorted = top_user_df1_sorted.sort_values(by='Registered_Users', ascending=False).head(10)

    title3 = f"Top 10 districts across {'All States' if state3 == 'All' else state3} by registered users {'between 2018 - 2022' if year3 == 'All' else f'in {year3}'}"

    fig3 = px.bar(
        top_user_df1_sorted,
        x='Registered_Users',
        y='District',
        color='Registered_Users',
        color_continuous_scale='Greens',
        orientation='h', labels={'Registered_Users': 'Registered Users'},
        hover_name='District',
        hover_data=['Registered_Users']
    )

    fig3.update_traces(hovertemplate='<b>%{hovertext}</b><br>Registered Users: %{x:,}<br>')

    fig3.update_layout(
        height=500, width=950,
        yaxis=dict(autorange="reversed"),
        title={
            'text': title3,
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.007,
            'yanchor': 'bottom'
        }
    )

    st.plotly_chart(fig3, use_container_width=True)

    expander3 = st.expander(label='Detailed View')
    expander3.write(top_user_df1_sorted.loc[:, ['District', 'Registered_Users']].reset_index(drop=True))

    add_vertical_space(2)

with st.container():
    st.subheader('Total App Open by District')

    y_col4, q_col2, buff = st.columns([2, 2, 7])
    items_to_remove = ['All', '2018']
    year_option_19 = year_option
    for item in items_to_remove:
        year_option.remove(item)

    with y_col4:
        year4 = st.selectbox('Year', year_option_19, key='year4')
    if year4 == '2019':
        quarter_option.remove(1)
    with q_col2:
        quarter3 = st.selectbox('Quarter', quarter_option, key='quarter3')
    map_user_df1_sorted_2 = map_user_df1[map_user_df1['Year'] == year4]

    if quarter3 != 'All':
        map_user_df1_sorted_2 = map_user_df1_sorted_2[map_user_df1_sorted_2['Quarter'] == int(quarter3)]
    else:
        if year4 == '2019':
            map_user_df1_sorted_2 = map_user_df1_sorted_2[map_user_df1_sorted_2['Quarter'] != 1]
        else:
            map_user_df1_sorted_2 = map_user_df1_sorted_2

    map_user_df1_sorted_2 = map_user_df1_sorted_2[map_user_df1_sorted_2['Total_App_open'] != 0]

    fig4 = px.density_mapbox(
        map_user_df1_sorted_2,
        lat='Latitude', lon='Longitude',
        z='Total_App_open', radius=20,
        center=dict(lat=20.5937, lon=78.9629),
        zoom=3, hover_name='District',
        mapbox_style="stamen-watercolor",
        opacity=0.8, labels={'Total_App_open': 'App Opens'},
        hover_data={
            'Latitude': False,
            'Longitude': False,
            'State': True
        },
        color_continuous_scale='Blues'
    )

    fig4.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=3.45, mapbox_center={"lat": 20.93684, "lon": 78.96288},
        geo=dict(scope='asia', projection_type='equirectangular'),
        title={
            'text': 'App Opens Density Map',
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.04,
            'yanchor': 'bottom',
            'font': dict(color='black')
        },
        coloraxis_colorbar=dict(len=0.9),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=900, height=500
    )

    st.plotly_chart(fig4, use_container_width=True)

    expander4 = st.expander(label='Detailed View')
    expander4.write(
        map_user_df1_sorted_2.loc[:, ['District',
                                      'Quarter',
                                      'Total_App_open']].sort_values(by='Total_App_open',
                                                                     ascending=False).reset_index(drop=True)
    )

    add_vertical_space(2)
