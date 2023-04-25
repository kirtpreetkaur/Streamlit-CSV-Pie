import pickle
from pathlib import Path
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
import yaml
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import altair as alt
from time import strftime
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url_search = "https://assets7.lottiefiles.com/packages/lf20_yJ8wNO.json"
# lottie_url_search = "https://assets3.lottiefiles.com/packages/lf20_1PD1tpvlop.json"
lottie_url_hello = "https://assets3.lottiefiles.com/packages/lf20_nOfkZot060.json"
lottie_url_welcome= "https://assets1.lottiefiles.com/packages/lf20_llbjwp92qL.json"
lottie_hello = load_lottieurl(lottie_url_hello)
lottie_search = load_lottieurl(lottie_url_search)
lottie_welcome=load_lottieurl(lottie_url_welcome)
# --- USER AUTHENTICATION ---
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=yaml.SafeLoader)
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# name, authentication_status, username = authenticator.login('Login', 'main')

def firewall():
    # Upload CSV
    # uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    df = pd.read_csv("firewall_status.csv")
    # Add a new column with tick or cross marks based on the value in the "Enabled" column
    df["Status"] = df["Enabled"].apply(lambda x: "✅" if x else "❌")
    # color of tick and cross marks based on the value in the "Enabled" column
    df["Status"] = df["Enabled"].apply(lambda x: "✅" if x else "❌")

    col1, col2 = st.columns(2)
    enabled_count = df["Enabled"].value_counts()
    colors = ["green", "red"]
    with col1:
        # Display the CSV file as a table with tick or cross
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.table(df[["Name", "Status"]].style.hide_index())

    with col2:
# Create a pie chart showing the frequency of True and False values in the "Enabled" column
        fig2 = px.pie(values=enabled_count.values, names=enabled_count.index, title="Status of Firewall Across Domains",
              color=enabled_count.index, color_discrete_sequence=colors)
        st.plotly_chart(fig2)

 # comparative bar chart for True and False values in the "Enabled" column

    fig1 = px.bar(x=enabled_count.index, y=enabled_count.values,
                      title="Comparative analysis of Active & Inactive Firewall on Domains", color=enabled_count.index,
                      color_discrete_sequence=colors)
    fig1.update_xaxes(title_text="Firewall Value")
    fig1.update_yaxes(title_text="Number of Domains", tickmode='linear', dtick=1)
    st.plotly_chart(fig1)

def os_version():
    csv_file_path = "osversion8.csv"
    dataframe = pd.read_csv(csv_file_path)
    # st.header("OS Version and Properties")
    st.image("image.png")
    st.table(dataframe)
    

def netstats():
    # file = st.file_uploader("Upload CSV file", type=["csv"])
    file = "network-stats.csv"
    if file:
        df = pd.read_csv(file)

        # Create a bar chart of InterfaceAlias and Source
        chart = alt.Chart(df).mark_bar().encode(
            x='InterfaceAlias',
            y='count()',
            color='Source'
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart)

        # Create a table of statistics for each InterfaceAlias
        interfaces = df['InterfaceAlias'].unique()
        for interface in interfaces:
            st.write('## ' + interface)
            subset = df[df['InterfaceAlias'] == interface]
            subset = subset.drop(columns=['ifAlias', 'ifDesc', 'Caption', 'Description', 'ElementName', 'InstanceID',
                                          'InterfaceDescription', 'Name', 'Source', 'SystemName'])
            st.write(subset)

def peripheral():
    #st.title("Peripherals Status")

    filename = "PeripheralsAndAdaptersReport.csv"
    df = pd.read_csv(filename)
    status_dict = {"OK": "✅", "ERROR": "❌"}
    df["Status"] = df["Status"].map(status_dict)

    st.markdown(
        '<style>div.row-widget.stRadio > div{background-color: #f4f4f4}</style>',
        unsafe_allow_html=True,
    )
    st.write(df)

    total_class = len(df)
    system_adap = len(df[df['Class'] == 'System'])
    net_adap = total_class - system_adap
    System_percentage = round(system_adap/ total_class * 100, 2)
    Net_percentage = round( net_adap / total_class* 100, 2)

    data = {'Class': ['System', 'Net'], 'Percentage': [System_percentage, Net_percentage]}
    fig1 = px.pie(data, values='Percentage', names='Class', color_discrete_sequence=['yellow', 'teal'])

    st.plotly_chart(fig1)

def portList():
    df = pd.read_csv("output.csv")
    # st.set_page_config(page_title="Listening Port Stats")
    # Bold Bold headings dekhlo
    # st.markdown("<h1 style='text-align: center; font-weight: bold;'>Listening Port Stats 👂🏻</h1>",
    #             unsafe_allow_html=True)
    # Gol Gol Pie Dekho
    process_count = df["Process"].value_counts()
    fig1 = px.pie(values=process_count, names=process_count.index, title="Process Frequency")
    st.plotly_chart(fig1)

    # Bar Chart 🌚
    address_count = df["LocalAddress"].value_counts()
    fig2 = px.bar(x=address_count.index, y=address_count.values, title="Local Address Frequency")
    st.plotly_chart(fig2)

    # Table m sab dekhlo
    st.write(df.style.set_properties(**{'font-weight': 'bold'}))


with st.sidebar:
    st_lottie(lottie_hello,width=300, height=200, loop=True, quality='high', key="hello")
st.sidebar.title(f"Welcome AISH !")

with st.sidebar:
        selected = option_menu(
            menu_title= "Dashboard",
            options=["Home", "Notifications","Network Audit", "OS Audit", "Vulnerability Assessment", "Malware Logs"],
            icons=["house","bell fill","ethernet","motherboard","braces asterisk","text-paragraph"],
            menu_icon="cast",
            default_index=0,
        )
if selected=="Home":
    st.title(f"{selected}")
#     with st_lottie_spinner(lottie_welcome,width=600,height=400,loop=False,quality='high'):
#         time.sleep(9)
    with st_lottie_spinner(lottie_search, width=700, height=550, loop=True, quality='high'):
        time.sleep(10)

if selected== "Notifications":
        st.title(f"{selected}")
        #st.subheader('Notifications 🗒')
        with st.spinner("Listening..."):
            time.sleep(3)
        st.error(' Firewall are not enabled for one or more Domains 🧱❌')
        with st.spinner("Listening..."):
            time.sleep(2)
        st.error(' Ports [21] & [22] are open ⚠️')
        with st.spinner("Listening..."):
            time.sleep(1)
        st.error(' No active backup present ❓')
        with st.spinner("Listening..."):
            time.sleep(2)
        st.success(' System is Up-to Date 🆙')
        with st.spinner("Listening..."):
            time.sleep(3)
        st.success(' 2 Active Users Found 👥')
        
        
        
        

if selected == "Network Audit":
        select = option_menu(
            menu_title="Network Audit",
            options=["Listening Ports", "Network Stats","Firewall Stats"],
            icons=["bricks", "displayport", "fire"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )
        # st.title(f"{selected}")
        if select == "Listening Ports":
            st.title(f"{select}")
            portList()
        if select == "Firewall Stats":
            st.title(f"{select}")
            firewall()
        if select == "Network Stats":
            st.title(f"{select}")
            netstats()



if selected == "OS Audit":
        select = option_menu(
            menu_title="OS Audit",
            options=["OS Details and System Version", "Peripheral Devices"],
            icons=["bricks", "displayport", "fire"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )
        if select == "OS Details and System Version":
            tab_titles={
              "Host Details",
              "OS Properties",
              "Hardware Properties",
              "Logical Properties",
              "Locale Properties",
              "Memory Properties",
              "Network and Adapter Properties",
              "Hypervisor Properties",
              "Hotfixes"
            }
            tabs = st.tabs(tab_titles)
            
            with tabs[0]:
#                 st.subheader("Host Details")
                df = pd.read_csv('systeminfo.csv', names=['Name', 'Value'])

            # create sections
                sections = {
                'Logical Properties': ['Windows Directory', 'System Directory', 'BIOS Version']
            }

            # create dictionary to store values for each section
                section_values = {}
                for section in sections:
                    section_values[section] = {}

            # loop through rows of dataframe and populate section values dictionary
                for index, row in df.iterrows():
                    for section, section_names in sections.items():
                        if row['Name'] in section_names:
                            section_values[section][row['Name']] = row['Value']

            # display sections
                for section, section_names in sections.items():
                    st.header(section)
                    section_df = pd.DataFrame(section_values[section].items(), columns=['Name', 'Value'])
                    section_df = section_df.loc[section_df['Name'].isin(section_names)]
                    section_df['Value'] = section_df['Value'].apply(lambda x: '✔️' if x == 'True' else (
                        '❌' if x == 'False' else x))  # add tick or cross for True/False values
                    st.dataframe(section_df.style.set_properties(**{'width': '100px'}), width=800)

            with tabs[1]:
                st.subheader("OS Properties")
            with tabs[2]:
                st.subheader("Hardware Properties")
            with tabs[3]:
                st.subheader("Locale Properties")
            with tabs[4]:
                st.subheader("Memory Properties")
            with tabs[5]:
                st.subheader("Network and Adapter Properties")
            with tabs[6]:
                st.subheader("Hypervisor Properties")
            with tabs[7]:
                st.subheader("Hypervisor Properties")
            with tabs[8]:
                st.subheader("Logical Properties")

            
        if select == "Peripheral Devices":
            st.title(f"{select}")
            peripheral()


if selected == "Vulnerability Assessment":
        select = option_menu(
            menu_title="Vulnerability Assessment",
            options=["Assessment 1", "Assessment 2", "Assessment 3"],
            icons=["file-bar-graph", "file-bar-graph", "file-bar-graph"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )
        if select == "Assessment 1":
            st.title(f"{select}")
        if select == "Assessment 2":
            st.title(f"{select}")
        if select == "Assessment 3":
            st.title(f"{select}")

if selected == "Malware Logs":
        st.title(f"{selected}")


