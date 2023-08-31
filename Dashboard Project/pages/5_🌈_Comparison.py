import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px
from streamlit_extras.add_vertical_space import add_vertical_space

# Data prep
trans_df1 = trans_df2 = trans_df3 = st.session_state['agg_trans_df']
user_df = st.session_state['agg_user_df']

trans_df1['Total_Transaction (B)'] = trans_df1['Total_Transaction'] / 1e9
year_order = sorted(trans_df1['Year'].unique())
trans_df1['Year'] = pd.Categorical(values=trans_df1['Year'], categories=year_order, ordered=True)

quarter_options = ['All'] + list(st.session_state['quarters'])
transaction_types = trans_df1['Payment_Type'].unique()

# Page result
st.set_page_config(
    page_title='Comparative Analysis',
    page_icon="Images_and_logo/Logo.png",
    layout="wide"
)
with st.container():
    st.title("🌈 Comparative Analysis")
    add_vertical_space(3)

with st.container():
    st.subheader("Region-wise Transaction Volume Comparison")

    fig1 = sns.catplot(
        x="Year", y="Total_Transaction",
        col="Region", data=trans_df1,
        kind="bar",
        height=5, aspect=1.5, col_wrap=2,
        sharex=False
    )
    for ax in fig1.axes.flat:
        ax.set_yticklabels(['₹. {:,.0f}M'.format(y / 1e6) for y in ax.get_yticks()])
        ax.set_ylabel('Transaction Amount')

    sns.set_style("white")
    st.pyplot(fig1, use_container_width=True)
    add_vertical_space(2)

with st.container():
    st.subheader('Transaction breakdown by Payment Type')

    col1, col2, col3 = st.columns([5, 3, 1])
    with col1:
        selected_states = st.multiselect('Select State(s)', trans_df2['State'].unique(), key='selected_states')
    with col2:
        year1 = st.selectbox("Year", trans_df2['Year'].unique(), key='year1')
        trans_df2 = trans_df2[trans_df2['Year'] == year1]
    with col3:
        quarter1 = st.selectbox("Quarter", quarter_options, key="quarter1")
        if quarter1 != 'All':
            trans_df2 = trans_df2[trans_df2['Quarter'] == int(quarter1)]
        else:
            trans_df2 = trans_df2
    suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == 1 else "nd" if quarter1 == 2 else "rd" if quarter1 == 3 else "th"

    if len(selected_states) == 1:
        state_str = ''.join(selected_states)
        title1 = f"Transaction details of {state_str} for {str(quarter1).lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"
    else:
        title1 = f"Transaction details comparison of the selected states for {str(quarter1).lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    if selected_states:
        trans_df2 = trans_df2[trans_df2["State"].isin(selected_states)]
        trans_df2 = trans_df2.sort_values("Total_Transaction", ascending=False)

        fig2 = px.bar(
            trans_df2, x="Payment_Type", y="Total_Transaction",
            color="State",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            barmode='group',
            title=title1,
            labels=dict(Total_Transaction='Transaction Count', Payment_Type='Payment Type'),
            hover_data={'Quarter': True}
        )

        fig2.update_layout(
            width=900, height=550,
            title={
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.9,
                'yanchor': 'top'
            }
        )

        fig2.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

        st.plotly_chart(fig2, use_container_width=True)
        add_vertical_space(2)
    else:
        column, buffer = st.columns([5, 4])
        with column:
            st.info("🚨 Please select at least one state to display the plot. 🚨")
        add_vertical_space(10)

with st.container():
    st.subheader('Transaction amount comparison - Quarter-wise')

    col4, col5, buff = st.columns([3, 2, 4])

    with col4:
        region1 = st.selectbox('Region', trans_df3['Region'].unique(), key='region1')
        filtered_df = trans_df3[trans_df3['Region'] == region1]
    with col5:
        year2 = st.selectbox("Year", trans_df3['Year'].unique(), key='year2')
        filtered_df = filtered_df[filtered_df['Year'] == year2]

    filtered_df['Quarter'] = 'Quarter ' + filtered_df['Quarter'].astype(str)

    fig3 = px.pie(
        filtered_df, values='Total_Transaction (B)',
        names='Quarter', color='Quarter',
        title=f'Transaction amount Comparison of {region1} for the year {year2}'
    )

    fig3.update_layout(
        width=850, height=550,
        title={
            'x': 0.45,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'top'
        }
    )

    fig3.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig3)

    filtered_df['Year'] = filtered_df["Year"].astype(int)

    expander1 = st.expander('Detailed view')
    expander1.dataframe(
        filtered_df.groupby(
            [
                'Year', 'Quarter'
            ]
        ).agg(
            {
                'Total_Transaction (B)': sum
            }
        ).reset_index().sort_values(
            'Total_Transaction (B)',
            ascending=False
        ).loc[:, ['Quarter', 'Total_Transaction (B)']].reset_index(drop=True)
    )

