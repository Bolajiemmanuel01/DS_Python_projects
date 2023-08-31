import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
from streamlit_extras.add_vertical_space import add_vertical_space

map_trans = st.session_state['map_trans_df']
top_trans_dist = dist_trans = st.session_state["top_trans_dist_df"]
pin_trans = st.session_state['top_trans_pin_df']


def filter_func(dataframe: pd.DataFrame, year: str, quarter: str):
    if year != 'All':
        dataframe_filtered = dataframe[dataframe['Year'] == year]
    else:
        dataframe_filtered = dataframe
    if quarter != 'All':
        dataframe_filtered = dataframe_filtered[dataframe_filtered['Quarter'] == int(quarter)]
    else:
        dataframe_filtered = dataframe_filtered
    return dataframe_filtered


st.set_page_config(page_title='Trend Analysis', layout='wide', page_icon='Images_and_logo/Logo.png')
st.title('📈 Trend Analysis 📉')
add_vertical_space(3)

state_options = ['All'] + [state for state in st.session_state['states']]
year_options = ['All'] + [state for state in st.session_state['years']]
quarter_options = ['All'] + list(st.session_state['quarters'])

with st.container():
    st.subheader('Transaction Count and Amount - Trend over the years')
    add_vertical_space(1)

    col1, col2, col3, col4 = st.columns([3, 4, 4, 2])

    with col1:
        region1 = st.selectbox('Region', map_trans['Region'].unique(), key='region1')
        df = map_trans[map_trans['Region'] == region1]
    with col2:
        state1 = st.selectbox('State', df['State'].unique(), key='state1')
        df = df[df['State'] == state1]
    with col3:
        district1 = st.selectbox('District', df['District'].unique(), key='district1')
        df = df[df['District'] == district1]
    with col4:
        year1 = st.selectbox('Year', year_options, key='year1')

    if year1 == 'All':
        df = df
        title1 = f'Transaction count trend for {district1} district in {state1} across {str(year1).lower()} years'
        title2 = f'Transaction amount trend for {district1} district in {state1} across {str(year1).lower()} years'
    else:
        df = df[df['Year'] == year1]
        title1 = f'Transaction count trend for {district1} district in {state1} during {year1}'
        title2 = f'Transaction amount trend for {district1} district in {state1} during {year1}'

    tab1, tab2 = st.tabs(['🫰Transaction Count Trend', '💰Transaction Amount Trend'])

    with tab1:
        fig1 = px.line(df, x='Quarter', y='Total_Transaction', color='Year', title=title1)

        fig1.update_xaxes(tickmode='array', tickvals=list(range(1, 5)))

        fig1.update_layout(
            height=500, width=900,
            yaxis_title='Transaction Count',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.9,
                'yanchor': 'bottom'
            }
        )
        st.plotly_chart(fig1, use_container_width=True)
        expander1 = tab1.expander('Detailed view')
        expander1.write(
            df.loc[:, ['Region', 'District', 'Year', 'Quarter', 'Total_Transaction']].reset_index(drop=True))

    with tab2:
        fig2 = px.line(df, x='Quarter', y='Transaction_Value', color='Year', title=title2)

        fig2.update_xaxes(tickmode='array', tickvals=list(range(1, 5)))

        fig2.update_layout(
            height=500, width=900,
            yaxis_title='Transaction Value',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.9,
                'yanchor': 'bottom'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)
        expander2 = tab2.expander('Detailed view')
        expander2.write(
            df.loc[:, ['Region', 'District', 'Year', 'Quarter', 'Transaction_Value']].reset_index(drop=True))

    add_vertical_space(3)

with st.container():
    st.subheader('Transaction Count and Amount - Top Districts')
    add_vertical_space(1)

    col5, col6, col7 = st.columns([5, 3, 1])

    with col5:
        state2 = st.selectbox('State', state_options, key='state2')
        if state2 != 'All':
            top_trans_dist1 = top_trans_dist[top_trans_dist["State"] == state2]
        else:
            top_trans_dist1 = top_trans_dist
    with col6:
        year2 = st.selectbox('Year', year_options, key='year2')
        if year2 != 'All':
            top_trans_dist1 = top_trans_dist1[top_trans_dist1["Year"] == year2]
        else:
            top_trans_dist1 = top_trans_dist1
    with col7:
        quarter2 = st.selectbox('Quarter', quarter_options, key='quarter2')
        quarter2 = str(quarter2)
        if quarter2 != 'All':
            top_trans_dist1 = top_trans_dist1[top_trans_dist1["Quarter"] == int(quarter2)]
        else:
            top_trans_dist1 = top_trans_dist1

    suffix2 = " quarters" if quarter2 == 'All' else 'st' if quarter2 == '1' else 'nd' if quarter2 == '2' else 'rd' if quarter2 == '3' else 'th'
    title2 = f"Top 10 Districts in {'India' if state2 == 'All' else state2} for {quarter2.lower()}{suffix2} {'' if quarter2 == 'All' else 'quarter'} of {'2018 - 2022' if year2 == 'All' else year2}"

    tab3, tab4 = st.tabs(['🫰Transaction Count - Top Districts', '💰Transaction Amount - Top Districts'])

    with tab3:
        aggregation_functions = {'Total_Transaction': 'sum',  # Sum the 'Registered_Users' column
                                 'Latitude': 'first',  # Keep the first value of 'Latitude'
                                 'Longitude': 'first'}  # Keep the first value of 'Longitude'
        top_trans_dist_top10 = top_trans_dist1.groupby('District').agg(aggregation_functions).reset_index()
        top_trans_dist_top10 = top_trans_dist_top10.sort_values(by='Total_Transaction', ascending=False).head(10)
        # top_trans_dist_top10 = top_trans_dist_top10.iloc[::-1]

        fig3 = px.bar(
            top_trans_dist_top10,
            x='Total_Transaction',
            y='District',
            color='District',
            category_orders={'District': top_trans_dist_top10['District']},
            orientation='h', labels={'Total_Transaction': 'Transaction Count'},
            hover_name='District',
            hover_data=['Total_Transaction']
        )

        fig3.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Count: %{x:,}<br>')

        fig3.update_layout(
            height=500, width=950,
            # yaxis=dict(autorange="reversed"),
            title={
                'text': title2,
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.007,
                'yanchor': 'bottom'
            }
        )

        st.plotly_chart(fig3, use_container_width=True)
        expander3 = st.expander('Detailed View')
        expander3.write(top_trans_dist_top10.loc[:, ['District', 'Total_Transaction']].reset_index(drop=True))

    with tab4:
        aggregation_functions = {'Transaction_Value': 'sum',  # Sum the 'Transaction_Value' column
                                 'Latitude': 'first',  # Keep the first value of 'Latitude'
                                 'Longitude': 'first'}  # Keep the first value of 'Longitude'
        top_trans_dist_top10 = top_trans_dist1.groupby('District').agg(aggregation_functions).reset_index()
        top_trans_dist_top10 = top_trans_dist_top10.sort_values(by='Transaction_Value', ascending=False).head(10)

        fig4 = px.bar(
            top_trans_dist_top10,
            x='Transaction_Value',
            y='District',
            color='District',
            category_orders={'District': top_trans_dist_top10['District']},
            orientation='h', labels={'Transaction_Value': 'Transaction Amount'},
            hover_name='District',
            hover_data=['Transaction_Value']
        )

        fig4.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Amount: %{x:,}<br>')

        fig4.update_layout(
            height=500, width=950,
            # yaxis=dict(autorange="reversed"),
            title={
                'text': title2,
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.007,
                'yanchor': 'bottom'
            }
        )

        st.plotly_chart(fig4, use_container_width=True)
        expander4 = st.expander('Detailed View')
        expander4.write(top_trans_dist_top10.loc[:, ['District', 'Transaction_Value']].reset_index(drop=True))
    add_vertical_space(3)

with st.container():
    st.subheader('Other Key Trends over the years')

    col8, col9, col10 = st.columns([5, 3, 1])

    with col8:
        trend3 = st.selectbox('Trend',
                              ('Top 10 States by Transaction Volume',
                               'Top 10 Districts by Transaction Volume',
                               'Top 10 Pincodes by Transaction Volume'),
                              key='trend3'
                              )
    with col9:
        year3 = st.selectbox('Year', year_options, key='year3')
    with col10:
        quarter3 = st.selectbox('Quarter', quarter_options, key='quarter3')

    filtered_dist_trans = filter_func(top_trans_dist, year3, quarter3)
    filtered_pin_trans = filter_func(pin_trans, year3, quarter3)
    filtered_pin_trans['Pincode'] = filtered_pin_trans['Pincode'].astype(str)

    filtered_top_states = filtered_dist_trans.groupby('State')[
        'Transaction_Value'
    ].sum().reset_index().sort_values(
        'Transaction_Value',
        ascending=False
    ).head(10)

    filtered_top_district = filtered_dist_trans.groupby('District')[
        'Transaction_Value'
    ].sum().reset_index().sort_values(
        'Transaction_Value',
        ascending=False
    ).head(10)

    filtered_top_pincodes = filtered_pin_trans.groupby('Pincode')[
        'Transaction_Value'
    ].sum().reset_index().sort_values(
        'Transaction_Value',
        ascending=False
    ).head(10)
    filtered_top_pincodes['Pincode'] = filtered_top_pincodes['Pincode'].astype(str)

    suffix2 = " quarters" if quarter3 == 'All' else "st" if quarter3 == 1 else "nd" if quarter3 == 2 else "rd" if quarter3 == 3 else "th"
    axis_format = '~s'

    if trend3 == 'Top 10 States by Transaction Volume':
        title5 = f"Top 10 states by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {'2018 - 2022' if year3 == 'All' else year3}"
        fig5 = px.bar(
            filtered_top_states,
            x='Transaction_Value',
            y='State',
            color='State',
            category_orders={'State': filtered_top_states['State']},
            orientation='h', labels={'Transaction_Value': 'Transaction Amount'},
            hover_name='State',
            hover_data=['Transaction_Value']
        )

        fig5.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Amount: %{x:,}<br>')

        fig5.update_layout(
            height=500, width=950,
            title={
                'text': title5,
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.007,
                'yanchor': 'bottom'
            }
        )

        st.plotly_chart(fig5, use_container_width=True)
        expander5 = st.expander('Detailed View')
        expander5.write(filtered_top_states.loc[:, ['State', 'Transaction_Value']].reset_index(drop=True))
        add_vertical_space(3)
    elif trend3 == 'Top 10 Districts by Transaction Volume':
        title5 = f"Top 10 Districts by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {'2018 - 2022' if year3 == 'All' else year3}"
        fig5 = px.bar(
            filtered_top_district,
            x='Transaction_Value',
            y='District',
            color='District',
            category_orders={'District': filtered_top_district['District']},
            orientation='h', labels={'Transaction_Value': 'Transaction Amount'},
            hover_name='District',
            hover_data=['Transaction_Value']
        )

        fig5.update_traces(hovertemplate='<b>%{hovertext}</b><br>Transaction Amount: %{x:,}<br>')

        fig5.update_layout(
            height=500, width=950,
            title={
                'text': title5,
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.007,
                'yanchor': 'bottom'
            }
        )

        st.plotly_chart(fig5, use_container_width=True)
        expander5 = st.expander('Detailed View')
        expander5.write(filtered_top_district.loc[:, ['District', 'Transaction_Value']].reset_index(drop=True))
        add_vertical_space(3)
    else:
        title5 = f"Top 10 Pincodes by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {'2018 - 2022' if year3 == 'All' else year3}"
        fig5 = alt.Chart(
            filtered_top_pincodes,
            height=500, width=900
        ).mark_bar(size=18).encode(
            x=alt.X(
                'Transaction_Value',
                axis=alt.Axis(format=axis_format),
                title="Transaction Amount"
            ),
            y=alt.Y('Pincode', sort='-x'),
            tooltip=[
                'Pincode', alt.Tooltip('Transaction_Value', format='.2f')
            ]
        ).properties(
            title=alt.TitleParams(
                text=title5,
                align="center",
                anchor='middle'
            )
        )
        st.altair_chart(fig5, use_container_width=True)
        expander5 = st.expander('Detailed View')
        expander5.write(filtered_top_pincodes.loc[:, ['Pincode', 'Transaction_Value']].reset_index(drop=True))
        add_vertical_space(3)
