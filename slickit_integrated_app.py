%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from datetime import datetime, timedelta

# Function to navigate to the previous page
def go_back():
    if 'history' in st.session_state and len(st.session_state['history']) > 1:
        st.session_state['history'].pop()
        st.session_state['page'] = st.session_state['history'][-1]

# Function to handle the greeting page
def greeting_page():
    st.title("Hi there, buddy!")
    name = st.text_input("What's your name?", key='name_input')
    if st.button("Submit Name"):
        if name:
            st.session_state['name'] = name
            st.session_state['history'].append('assets_page')
            st.session_state['page'] = 'assets_page'
        else:
            st.error("Please enter a name.")

# Function to handle the asset selection page
def assets_page():
    st.title(f"Hi there, {st.session_state['name']}!")
    st.subheader("Select your number of assets")
    assets = {}
    for asset in ['Excavator_1', 'Backhoe_Loader_1', 'Articulated_Truck_1', 'Asphalt_Paver_1', 'Dozer_1']:
        count = st.number_input(f'Number of {asset}s', min_value=0, max_value=10, key=f'{asset}_count')
        if count > 0:
            machine_ids = []
            for i in range(count):
                machine_id = st.text_input(f'{asset} ID {i+1}', key=f'{asset}id{i}')
                if machine_id:
                    machine_ids.append(machine_id)
            if machine_ids:
                assets[asset] = machine_ids

    if st.button("Enter"):
        if assets:
            st.session_state['assets'] = assets
            st.session_state['history'].append('action_page')
            st.session_state['page'] = 'action_page'
        else:
            st.error("Please provide at least one asset.")

    if st.button("Back"):
        go_back()

# Function to handle the action selection page
def action_page():
    st.title("Select the asset to perform the action")

    if 'assets' in st.session_state:
        selected_machine = st.radio("Select a machine to perform Smart Diagnostics",
                                    list(st.session_state['assets'].keys()))

        if st.button(f"Smart Diagnostics for {selected_machine}"):
            st.session_state['selected_machine'] = selected_machine
            st.session_state['history'].append('file_upload_page')
            st.session_state['page'] = 'file_upload_page'

        if st.button(f"Monitor my {selected_machine}"):
            st.session_state['selected_machine'] = selected_machine
            st.session_state['history'].append('monitor_my_machine_page')
            st.session_state['page'] = 'monitor_my_machine_page'

    if st.button("Back"):
        go_back()

# Function to handle the file upload page
def file_upload_page():
    st.title("Upload Dataset")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['file_uploaded'] = True

    if st.session_state.get('file_uploaded'):
        if st.button("Proceed to Analysis"):
            st.session_state['history'].append('analysis_page')
            st.session_state['page'] = 'analysis_page'

    if st.button("Back"):
        go_back()


def analysis_page():
    st.title("Analysis Page")

    if 'uploaded_file' in st.session_state and 'selected_machine' in st.session_state:
        uploaded_file = st.session_state['uploaded_file']
        machine = st.session_state['selected_machine']

        # Read the uploaded file
        input_df = pd.read_excel(uploaded_file)

        # Processing the data
        df = input_df.copy()
        df.loc[df['Probability of Failure'] == 'High', 'Failure'] = 1

        medium_indices = df[df['Probability of Failure'] == 'Medium'].index
        medium_failure_indices = np.random.choice(medium_indices, size=int(0.5 * len(medium_indices)), replace=False)
        df.loc[medium_failure_indices, 'Failure'] = 1
        df.loc[~df.index.isin(medium_failure_indices) & (df['Probability of Failure'] == 'Medium'), 'Failure'] = 0

        low_indices = df[df['Probability of Failure'] == 'Low'].index
        low_failure_indices = np.random.choice(low_indices, size=int(0.1 * len(low_indices)), replace=False)
        df.loc[low_failure_indices, 'Failure'] = 1
        df.loc[~df.index.isin(low_failure_indices) & (df['Probability of Failure'] == 'Low'), 'Failure'] = 0

        df['Failure'] = df['Failure'].fillna(0).astype(int)

        # Filter machine data based on machine name only
        machine_data = df[df['Machine'] == machine]
        components = machine_data['Component'].unique()
        failure_counts = machine_data.groupby('Component')['Failure'].sum()

        if not failure_counts.empty:
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.bar(failure_counts.index, failure_counts, color='#ffcc00', label=f"Failure Counts")
            ax.set_xlabel('Component')
            ax.set_ylabel('Failure Counts')
            ax.set_title(f'Failure Counts for {machine}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            st.pyplot(fig)

            # Print the component with the highest failure count
            max_failure_component = failure_counts.idxmax()
            max_failure_count = failure_counts.max()
            st.write(f"The component with the highest failure count for {machine} is {max_failure_component} with {max_failure_count} failures.")
            st.write(f"So most probably the failure is in {max_failure_component}")
            st.write("Please give your description of the problem in the following:")
            user_input = st.text_input("Enter your problem description here:")

        else:
            st.write("No data available for the selected machine.")
    else:
        st.error("Please upload a file and select a machine identifier.")

    if st.button("Get the diagnosis"):
                st.session_state['user_input'] = user_input
                st.session_state['history'].append('monitor_my_machine_page')
                st.session_state['page'] = 'results_page'

    if st.button("Back"):
        go_back()



def results_page():
    st.title("Results Page")

    if 'user_input' in st.session_state:
        user_input = st.session_state['user_input']
        st.write(f"User Input: {user_input}")
    from transformers import pipeline
    import time

    @st.cache_resource()
    def load_model():
      model = pipeline('text-generation', model='gpt2')
      return model
    model = load_model()
    if st.button('Generate answer'):
      with st.spinner('Generating answer...'):
          response = model(user_input)
          for i, summary in enumerate(response):
                st.write(f'**Story {i+1}:**')
                st.write(summary['generated_text'])
                st.markdown("---")

# Function to handle the monitor my machine page
def monitor_my_machine_page():
    st.title("Welcome to the smart asset monitoring page..")

    # Back button to navigate to the previous page

    st.write("Gathering data from Articulated_Truck...\n")

    start_datetime = datetime.strptime("11-08-2024 08:00", "%d-%m-%Y %H:%M")

    time.sleep(5)

    current_datetime = start_datetime
    values = [30, 35, 40, 45, 50]

    for value in values:
        placeholder = st.empty()

        # Displaying the current value and time
        engine_output = f"Engine: Oil Pressure is {value} at time stamp: {current_datetime.strftime('%d-%m-%Y %H:%M')}"
        placeholder.text(engine_output)

        time.sleep(5)

        # Displaying the expected value and time
        expected_value = random.randint(value - 5, value + 5)
        expected_time = current_datetime + timedelta(minutes=5)
        expected_output = f"Expected value of Engine: Oil Pressure at {expected_time.strftime('%d-%m-%Y %H:%M')} is {expected_value}\n"
        placeholder.text(f"{engine_output}\n{expected_output}")

        current_datetime += timedelta(minutes=5)

        time.sleep(10)

    # Displaying the analysis after the loop
    st.write("Analyzing...")
    time.sleep(15)

    st.markdown('<p style="color:red;">!!! ALERT !!!</p>', unsafe_allow_html=True)


    future_datetime = current_datetime + timedelta(minutes=10)
    st.write(f"Value after {future_datetime.strftime('%d-%m-%Y %H:%M')} will be 47.85, there is a high probability of failure around 78%")

    if st.button("Back"):
        go_back()

# Page navigation logic
if 'page' not in st.session_state:
    st.session_state['page'] = 'greeting_page'
    st.session_state['history'] = ['greeting_page']

if st.session_state['page'] == 'greeting_page':
    greeting_page()
elif st.session_state['page'] == 'assets_page':
    assets_page()
elif st.session_state['page'] == 'action_page':
    action_page()
elif st.session_state['page'] == 'file_upload_page':
    file_upload_page()
elif st.session_state['page'] == 'analysis_page':
    analysis_page()
elif st.session_state['page'] == 'monitor_my_machine_page':
    monitor_my_machine_page()
elif st.session_state['page'] == 'results_page':
    results_page()
