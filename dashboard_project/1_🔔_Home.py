import io
import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_player import st_player
from PIL import Image
import requests
from streamlit_lottie import st_lottie

# from streamlit_pandas_profiling import st_profile_report -streamlit-pandas-profiling==0.1.3

agg_trans_df = pd.read_csv(r'csv_files/agg_trans.csv')
agg_user_df = pd.read_csv(r'csv_files/agg_user.csv')
map_trans_df = pd.read_csv(r'csv_files/map_trans.csv')
map_user_df = pd.read_csv(r'csv_files/map_user.csv')
top_trans_dist_df = pd.read_csv(r'csv_files/top_trans_dist.csv')
top_trans_pin_df = pd.read_csv(r'csv_files/top_trans_pin.csv')
top_user_dist_df = pd.read_csv(r'csv_files/top_user_dist.csv')
top_user_pin_df = pd.read_csv(r'csv_files/top_user_pin.csv')

# Session
if 'options' not in st.session_state:
    st.session_state['options'] = {
        'Aggregate Transaction': 'agg_trans_df',
        'Aggregate User': 'agg_user_df',
        'Map Transaction': 'map_trans_df',
        'Map User': 'map_user_df',
        'Top Transaction Districtwise': 'top_trans_dist_df',
        'Top Transaction Pincodewise': 'top_trans_pin_df',
        'Top User Districtwise': 'top_user_dist_df',
        'Top User Pincodewise': 'top_user_pin_df'
    }

# Group Dataframes
df_names = [
    varname for varname in globals()
    if isinstance(globals()[varname], pd.core.frame.DataFrame) and varname.endswith('_df')
]

if 'df_list' not in st.session_state:
    st.session_state['df_list'] = []

    for varname in df_names:
        st.session_state[varname] = globals()[varname]
        st.session_state['df_list'].append(varname)


def year_to_str(df_frame):
    df_frame['Year'] = df_frame['Year'].astype(str)


for df_name in st.session_state['df_list']:
    df = globals()[df_name]
    year_to_str(df)
    globals()[df_name] = df


@st.cache_resource
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


states = agg_trans_df['State'].unique()
years = agg_trans_df['Year'].unique()
quarters = agg_trans_df['Quarter'].unique()

if 'states' not in st.session_state:
    st.session_state['states'] = states
if 'years' not in st.session_state:
    st.session_state['years'] = years
if 'quarters' not in st.session_state:
    st.session_state['quarters'] = quarters
# authenticator.logout('Logout', 'sidebar')


map_of_india = Image.open('Images_and_logo/map_of_india.png')

# ---- Page Configuration ------
st.set_page_config(page_title="Dashboard", page_icon="Images_and_logo/Logo.png", layout="wide")

# --- Load Assets ---
lottie_coding = load_lottie("https://lottie.host/50c32142-e93b-4f48-8a22-8d2f6b853a58/tjOVAhtxK0.json")

with st.container():
    st.title(":purple[🔔 Phone Pulse Analytics Dashboard]")

with st.container():
    description = """PhonePe has launched PhonePe Pulse, a data analytics platform that provides insights into
                        how Indians are using digital payments. With over 3.14 Billion registered users and present in 
                        5600 districts, PhonePe, India's largest digital payments platform with 46% UPI market share,
                        has a unique ring-side view into the Indian digital payments story. Through this app, you 
                        can now easily access and visualize the data provided by PhonePe Pulse, gaining deep 
                        insights and interesting trends into how India transacts with digital payments."""

    add_vertical_space(1)
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(f"<p style='text-align: justify;'><strong>{description}</strong></p>", unsafe_allow_html=True)
    with right_column:
        st_lottie(lottie_coding, key='flag', height=250, width=800)
add_vertical_space(2)
# The YouTube Video
with st.container():
    st_player(url="https://www.youtube.com/watch?v=c_1H6vivsiA", height=480)
    add_vertical_space(2)

with st.container():
    st.image(map_of_india, use_column_width=True,
             caption='Digital Transaction Volume Penetration. Left: 2018 | Right: 2022')
    add_vertical_space(2)

with st.container():
    left_column1, middle_column1, right_column1 = st.columns(3)

    total_reg_user = top_user_dist_df['Registered_Users'].sum()
    left_column1.metric(
        label='Total Registered Users',
        value='{:.2f} Billion'.format(total_reg_user / 1000000000),
        delta='23%'
    )
    total_app_opens = map_user_df['Total_App_open'].sum()
    middle_column1.metric(
        label=':black[Total App Opens]',
        value='{:.2f} Billion'.format(total_app_opens / 1000000000),
        delta='15%'
    )
    total_district = top_trans_dist_df['District'].count()
    right_column1.metric(
        label='District Presence',
        value='{} Districts'.format(total_district),
        delta='11%'
    )

    style_metric_cards(background_color='200329', border_radius_px=9, border_left_color='#7717AF')

    add_vertical_space(2)

with st.container():
    st.image("Images_and_logo/Pulse.gif", use_column_width=True)
    add_vertical_space(2)

with st.container():
    col, buff = st.columns([2, 4])
    option = col.selectbox(
        label='Select Dataset',
        options=list(st.session_state['options'].keys()),
        key='df'
    )

    tab1, tab2 = st.tabs(['Report and Dataset', 'Download Dataset'])

    with tab1:

        column1, column2, buffer = st.columns([2, 2, 4])

        show_profile = column1.button(label='Show Detailed Report', key='show_pf')
        show_dataset = column2.button(label='Show Dataset', key='show_df')

        if show_profile:
            df_name = st.session_state['options'][option]
            df = globals()[df_name]
            pr = ProfileReport(df, explorative=True)
            st.write(pr)

        if show_dataset:
            st.data_editor(
                data=globals()[st.session_state['options'][option]],
                use_container_width=True
            )
    with tab2:
        col1, col2, col3 = st.columns(3)

        df_name = st.session_state['options'][option]
        df = globals()[df_name]

        csv = df.to_csv()
        json = df.to_json(orient='records')
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, engine='xlsxwriter', index=False)
        excel_bytes = excel_buffer.getvalue()

        col1.download_button(
            label='Download as CSV file',
            data=csv,
            file_name=f'{option}.csv',
            mime='text/csv',
            key='csv'
        )

        col2.download_button(
            label='Download as JSON file',
            data=json,
            file_name=f'{option}.json',
            mime='application/json',
            key='json'
        )

        col3.download_button(
            label='Download as EXCEL file',
            data=excel_bytes,
            file_name=f'{option}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            key='excel'
        )
