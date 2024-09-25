import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from PIL import Image
import streamlit as st

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('data/tourism_data.csv')
    return data

# Train the model
def train_model(data):
    X = data[['month', 'temperature', 'local_events', 'holiday_season']]
    y = data['predicted_visitors']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

# Make prediction
def make_prediction(model, input_data):
    prediction = model.predict([input_data])
    return prediction[0]

# Streamlit app
st.title("WaveTour Pro")

# Load and display image
image = Image.open('images/Royal-Opera-House.jpeg')
st.image(image, use_column_width=True)

# Input fields for the features
st.write("### Input Features for Prediction")
month = st.number_input("Month", min_value=1, max_value=12)
temperature = st.number_input("Temperature")
local_events = st.number_input("Local Events")
holiday_season = st.number_input("Holiday Season (1 for Yes, 0 for No)")

# Load data
data = load_data()

# Train the model
model = train_model(data)

# Button to make predictions
if st.button("Predict Visitors"):
    input_data = [month, temperature, local_events, holiday_season]
    prediction = make_prediction(model, input_data)
    st.write(f"Predicted Visitors: {prediction:.0f}")

# Display data overview
st.write("### Data Overview")
st.write(data.head())

# Charts
st.write("### Monthly Visitors")
monthly_visitors = data.groupby('month')['predicted_visitors'].sum().reset_index()
st.bar_chart(monthly_visitors.set_index('month'))

st.write("### Average Visitors Based on Local Events")
average_visitors_events = data.groupby('local_events')['predicted_visitors'].mean().reset_index()
st.bar_chart(average_visitors_events.set_index('local_events'))

st.write("### Temperature vs. Predicted Visitors")
plt.figure(figsize=(10, 5))
plt.scatter(data['temperature'], data['predicted_visitors'], alpha=0.6)
plt.title("Temperature vs. Predicted Visitors")
plt.xlabel("Temperature")
plt.ylabel("Predicted Visitors")
st.pyplot(plt)

# Show the distribution of visitors
st.write("### Visitor Distribution Box Plot")
plt.figure(figsize=(10, 5))
sns.boxplot(x=data['month'], y=data['predicted_visitors'])
plt.title("Visitor Distribution per Month")
st.pyplot(plt)

# Add company logo and text
st.write("---")  # Add a horizontal line for separation
logo = Image.open('images/fulllogo_transparent.png')  # Update the path to your logo image
st.image(logo, use_column_width=True)
st.write("© 2024 SoftWave Solutions Trade and Services. All rights reserved.")
