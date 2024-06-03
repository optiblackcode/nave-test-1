import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and display the data
def load_data(file):
    data = pd.read_csv(file)
    return data

# Function to generate Kanban Chart (Cumulative Flow Diagram)
def generate_kanban_chart(data):
    # Process data to create cumulative flow diagram
    data['Date'] = pd.to_datetime(data['To do'], format='%d/%m/%Y')
    data['Done Date'] = pd.to_datetime(data['Done'], format='%d/%m/%Y')
    data = data.sort_values(by='Date')

    # Count tasks in each stage
    stages = ['To do', 'Development', 'Code review', 'Testing', 'Done']
    date_range = pd.date_range(start=data['Date'].min(), end=data['Done Date'].max())
    stage_counts = {stage: [] for stage in stages}

    for date in date_range:
        counts = data[(data['Date'] <= date) & ((data['Done Date'].isna()) | (data['Done Date'] > date))].count()
        for stage in stages:
            stage_counts[stage].append(counts['Id'])

    # Plot cumulative flow diagram
    plt.figure(figsize=(10, 6))
    plt.stackplot(date_range, stage_counts['To do'], stage_counts['Development'],
                  stage_counts['Code review'], stage_counts['Testing'], stage_counts['Done'],
                  labels=stages, alpha=0.8)
    plt.legend(loc='upper left')
    plt.title('Cumulative Flow Diagram')
    plt.xlabel('Date')
    plt.ylabel('Number of Tasks')
    st.pyplot(plt)

# Function to calculate WIP metrics
def calculate_wip_metrics(data):
    wip_items = len(data[(data['Done Date'].isna())])
    wip_age = (pd.Timestamp.now() - data['Date']).mean().days
    st.metric("WIP Items", wip_items)
    st.metric("Average WIP Age (days)", wip_age)

# Streamlit App
st.title("Nave Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)
    st.write("Uploaded Data")
    st.dataframe(data)
    
    if st.button("Create Dashboard"):
        st.subheader("Advanced Kanban Chart")
        generate_kanban_chart(data)
        
        st.subheader("WIP Metrics")
        calculate_wip_metrics(data)
