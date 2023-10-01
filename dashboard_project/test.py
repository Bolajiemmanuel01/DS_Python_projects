# import mysql.connector
# import streamlit as st
# from getpass import getpass

# ##connection
# password = getpass("Enter your password: ")
# conn = mysql.connector.connect(
#     host='localhost',
#     port='3306',
#     user='root',
#     password=f'{password}',
#     db='phone_pulse'
# )

# cursor = conn.cursor()

# cursor.execute('''
# SELECT column_name
# FROM information_schema.columns
# WHERE table_name = 'agg_trans';
# ''')
# here = []
# smiles = cursor.fetchall()
# for smile in smiles:
#     here.append(smile[0])
# print(here)
#
# import streamlit as st
#
# def home_page():
#     st.title("Home Page")
#     st.write("Welcome to the Home Page!")
#
# def about_page():
#     st.title("About Page")
#     st.write("Welcome to the About Page!")
#
# def contact_page():
#     st.title("Contact Page")
#     st.write("Welcome to the Contact Page!")
#
# def main():
#     st.markdown(
#         """
#         <style>
#         /* Custom sidebar styles */
#         .sidebar {
#             background-color: #0366d6;
#             color: #ffffff;
#             padding: 20px;
#             display: flex;
#             flex-direction: column;
#             justify-content: space-between;
#             height: 100vh;
#         }
#         .sidebar a {
#             color: #ffffff;
#             text-decoration: none;
#             font-size: 18px;
#             font-weight: bold;
#             margin-bottom: 15px;
#         }
#         .sidebar a:hover {
#             color: #f5f5f5;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#
#     # Sidebar layout
#     st.markdown('<div class="sidebar">'
#                 '<a href="#home">Home</a>'
#                 '<a href="#about">About</a>'
#                 '<a href="#contact">Contact</a>'
#                 '</div>',
#                 unsafe_allow_html=True)
#
#     # Create a column layout for the content
#     col1, col2 = st.beta_columns(2)
#
#     # Main content based on the anchor tag clicks
#     if col1.markdown('<h2 id="home">Home</h2>', unsafe_allow_html=True):
#         home_page()
#     elif col1.markdown('<h2 id="about">About</h2>', unsafe_allow_html=True):
#         about_page()
#     elif col1.markdown('<h2 id="contact">Contact</h2>', unsafe_allow_html=True):
#         contact_page()
#
# if __name__ == "__main__":
#     main()

# from pages import 3_Users
# states = 3_Users.agg_user_df1['State'].unique()
# years = Users.agg_user_df1['Year'].unique()
# quarters = Users.agg_user_df1['Quarter'].unique()
#
# print("States:", states)
# print("Years:", years)
# print("Quarters:", quarters)
#
# state_options = ['All'] + [state for state in states]
# quarter_option = ['All'] + [str(quarter) for quarter in quarters]
# year_option = ['All'] + [year for year in years]
#
# print("State Options:", state_options)
# print("Quarter Options:", quarter_option)
# print("Year Options:", year_option)
#



