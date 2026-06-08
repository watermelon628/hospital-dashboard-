import streamlit as st
import pandas as pd
import numpy as np

# Set up the Streamlit app
st.set_page_config(layout="wide")
st.title('🏥 Hospital Bed Capacity Dashboard')

# Create dummy data
data = {
    'Ward': ['ICU', 'General', 'Maternity', 'Pediatrics', 'Emergency'],
    'Total Beds': [20, 50, 30, 25, 40],
    'Occupied Beds': [18, 40, 10, 20, 35]
}

df = pd.DataFrame(data)
df['Available Beds'] = df['Total Beds'] - df['Occupied Beds']
df['Occupancy %'] = (df['Occupied Beds'] / df['Total Beds']) * 100

# Sidebar for filtering
st.sidebar.header('Filter Options')
occupancy_trigger = st.sidebar.slider(
    'Highlight Wards with Occupancy Above %:',
    min_value=0,
    max_value=100,
    value=80
)

# Display metrics
st.header('Real-Time Status')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Total Hospital Beds', df['Total Beds'].sum())

with col2:
    st.metric('Total Occupied', df['Occupied Beds'].sum())

with col3:
    # Logic: If occupancy is high, color it red
    total_occ = (df['Occupied Beds'].sum() / df['Total Beds'].sum()) * 100
    st.metric('Overall Occupancy %', f"{total_occ:.1f}%", delta_color="inverse")

# Main Chart
st.subheader(f'Wards above {occupancy_trigger}% Occupancy')
st.bar_chart(
    df.set_index('Ward')[['Occupied Beds', 'Available Beds']],
    stack=True
)

# Raw Data Table
st.subheader('Detailed Ward Data')
st.dataframe(
    df.style.highlight_between(
        left=occupancy_trigger,
        right=100,
        subset=['Occupancy %'],
        color='#ffcccc'
    )
)
