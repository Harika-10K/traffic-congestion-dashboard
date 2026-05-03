import streamlit as st
import pandas as pd
import plotly.express as px
from model import load_data, process_data

# ✅ Page setup (MUST BE FIRST)
st.set_page_config(page_title="Traffic Dashboard", layout="wide")

# Title
st.title("🚦 Traffic Congestion Dashboard")

# Load data
df = load_data()
df = process_data(df)
from sklearn.linear_model import LinearRegression

# Train model
X = df[['time']]
y = df['vehicle_count']

model = LinearRegression()
model.fit(X, y)

# ✅ FIX: your time is numeric already (8,9,10)
df['hour'] = df['time']

# Dataset view (optional - you can remove later)
st.subheader("📂 Dataset")
st.dataframe(df)

# Area selection
area = st.selectbox("📍 Select Area", df['area'].unique())
filtered = df[df['area'] == area]
st.subheader("🔮 Traffic Prediction")

input_time = st.slider("Select Time", 8, 10, 9)

predicted = model.predict([[input_time]])

st.success(f"🚗 Predicted Vehicles at {input_time}:00 = {int(predicted[0])}")

# 🎨 COLOR FUNCTION
def highlight_traffic(val):
    if val == 'Low':
        return 'background-color: lightgreen'
    elif val == 'Medium':
        return 'background-color: orange'
    elif val == 'High':
        return 'background-color: red; color: white'

# 📊 FILTERED DATA (COLORFUL)
st.subheader("📊 Filtered Data")
st.dataframe(filtered.style.applymap(highlight_traffic, subset=['traffic_level']))

# 📈 KEY INSIGHTS (WITH EMOJIS)
st.subheader("📊 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("🚗 Total Vehicles", filtered['vehicle_count'].sum())
col2.metric("📈 Avg Traffic", round(filtered['vehicle_count'].mean(), 2))

peak_hour = filtered.loc[filtered['vehicle_count'].idxmax(), 'hour']
col3.metric("⏰ Peak Hour", peak_hour)

# 🔥 INTERACTIVE GRAPH (PLOTLY)
st.subheader("📊 Traffic Trend")

fig = px.line(
    filtered,
    x='time',
    y='vehicle_count',
    color='traffic_level',
    markers=True,
    title=f"Traffic in {area}"
)

st.plotly_chart(fig, use_container_width=True)

# 🥧 PIE CHART (VERY IMPRESSIVE)
st.subheader("🚦 Traffic Distribution")

pie = px.pie(
    filtered,
    names='traffic_level',
    title="Traffic Level Distribution"
)

st.plotly_chart(pie, use_container_width=True)
st.dataframe(filtered.style.map(highlight_traffic, subset=['traffic_level']))

st.subheader("📍 Area Comparison")

compare = df.groupby('area')['vehicle_count'].mean().reset_index()

import plotly.express as px

fig_compare = px.bar(
    compare,
    x='area',
    y='vehicle_count',
    color='area',
    title="Average Traffic by Area"
)

st.plotly_chart(fig_compare, use_container_width=True)
import time
import random

st.subheader("📡 Live Traffic Simulation")

placeholder = st.empty()

for i in range(5):   # runs 5 updates
    simulated = random.randint(200, 1000)
    
    placeholder.metric("🚗 Live Vehicle Count", simulated)
    
    time.sleep(1)
