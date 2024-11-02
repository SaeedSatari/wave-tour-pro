import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA

# Set up the page
st.set_page_config(page_title="WaveTour Pro - Tourism Predictor", layout="wide")
header_image = 'images/wavetour-header.png'  # Replace with your image file path or URL
st.image(header_image, use_column_width=True)


# Load Data
@st.cache_data
def load_data():
    file_path = 'data/new_tourism_data_2010_2015_fixed.xlsx'
    visitors_df = pd.read_excel(file_path, sheet_name='Visitor Arrivals')
    expenditure_df = pd.read_excel(file_path, sheet_name='Tourist Expenditure')
    weather_df = pd.read_excel(file_path, sheet_name='Weather Patterns')
    economic_df = pd.read_excel(file_path, sheet_name='Economic Indicators')
    overall_df = pd.read_excel(file_path, sheet_name='Overall Data')
    return visitors_df, expenditure_df, weather_df, economic_df, overall_df


# Display Data
st.sidebar.header("Data Preview")

visitors_df, expenditure_df, weather_df, economic_df, overall_df = load_data()

data_choice = st.sidebar.selectbox("Choose dataset to view",
                                   ["Visitor Arrivals", "Tourist Expenditure", "Weather Patterns",
                                    "Economic Indicators"])

st.header("Overall Data - 2010 to 2015")
st.dataframe(overall_df, use_container_width=True, hide_index=True)

# Create a Plotly figure for visitor arrivals and expenditure
fig = go.Figure()

# Add bar trace for the number of visitors
fig.add_trace(go.Bar(
    x=overall_df['Year'],
    y=overall_df['Number of Visitors (in millions)'],
    name='Number of Visitors',
    marker_color='skyblue',
    yaxis='y1'  # Use the first y-axis
))

# Add line trace for the expenditure
fig.add_trace(go.Scatter(
    x=overall_df['Year'],
    y=overall_df['Expenditure (in billion THB)'],
    mode='lines+markers',
    name='Expenditure',
    line=dict(color='orange', width=2),
    marker=dict(size=8),
    yaxis='y2'  # Use the second y-axis
))

# Update layout for dual axes
fig.update_layout(
    title='Overall Visitor Arrivals and Expenditure Over the Years',
    xaxis_title='Year',
    yaxis_title='Number of Visitors (in millions)',
    yaxis=dict(
        title='Number of Visitors (in millions)',
        side='left',
        showgrid=True,
        zeroline=False,
        titlefont=dict(color='skyblue'),
        tickfont=dict(color='skyblue')
    ),
    yaxis2=dict(
        title='Expenditure (in billion THB)',
        overlaying='y',
        side='right',
        showgrid=False,
        zeroline=False,
        titlefont=dict(color='orange'),
        tickfont=dict(color='orange')
    ),
    xaxis=dict(tickvals=overall_df['Year']),  # Ensure all years are shown
    template='plotly_white',  # A clean white background
    hovermode='x unified'  # Show hover info for all traces at the same x-value
)

# Show the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

if data_choice == "Visitor Arrivals":
    st.header("Visitor Arrivals")
    st.dataframe(visitors_df, use_container_width=True, hide_index=True)
elif data_choice == "Tourist Expenditure":
    st.header("Tourist Expenditure")
    st.dataframe(expenditure_df, use_container_width=True, hide_index=True)
elif data_choice == "Weather Patterns":
    st.header("Weather Patterns")
    st.dataframe(weather_df, use_container_width=True, hide_index=True)
    # Create a Plotly figure for visitor arrivals and expenditure
    fig = go.Figure()

    # Add bar trace for the number of visitors
    fig.add_trace(go.Bar(
        x=weather_df['Year'],
        y=weather_df['Average Temperature (°C)'],
        name='Average Temperature',
        marker_color='orange',
        yaxis='y1'  # Use the first y-axis
    ))

    # Add line trace for the expenditure
    fig.add_trace(go.Scatter(
        x=weather_df['Year'],
        y=weather_df['Rainfall (mm)'],
        mode='lines+markers',
        name='Rainfall',
        line=dict(color='skyblue', width=2),
        marker=dict(size=8),
        yaxis='y2'  # Use the second y-axis
    ))

    # Update layout for dual axes
    fig.update_layout(
        title='Weather Patterns Over the Years',
        xaxis_title='Year',
        yaxis_title='Average Temperature (°C)',
        yaxis=dict(
            title='Average Temperature (°C)',
            side='left',
            showgrid=True,
            zeroline=False,
            titlefont=dict(color='orange'),
            tickfont=dict(color='orange')
        ),
        yaxis2=dict(
            title='Rainfall (mm)',
            overlaying='y',
            side='right',
            showgrid=False,
            zeroline=False,
            titlefont=dict(color='skyblue'),
            tickfont=dict(color='skyblue')
        ),
        xaxis=dict(tickvals=weather_df['Year']),  # Ensure all years are shown
        template='plotly_white',  # A clean white background
        hovermode='x unified'  # Show hover info for all traces at the same x-value
    )

    # Show the figure in Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.header("Economic Indicators")
    st.dataframe(economic_df, use_container_width=True, hide_index=True)

# Data Preparation and Visualization
st.header("Data Analysis and Preparation")

# Convert 'Visitors (in thousands)' to numeric, forcing non-numeric values to NaN
visitors_df['Visitors (in thousands)'] = pd.to_numeric(visitors_df['Visitors (in thousands)'], errors='coerce')

# Fill NaNs with 0 (or use .dropna() if you want to exclude those rows)
visitors_df['Visitors (in thousands)'].fillna(0, inplace=True)

# Now proceed with the groupby operation
visitor_totals = visitors_df.groupby('Year')['Visitors (in thousands)'].sum()
expenditure_df.fillna(method='ffill', inplace=True)
# Convert 'Total ($US) / Person per day' to numeric, setting non-numeric values to NaN
expenditure_df['Total ($US) / Person per day'] = pd.to_numeric(expenditure_df['Total ($US) / Person per day'],
                                                               errors='coerce')

# Handle NaNs (fill with 0, drop them, or use other strategies)
expenditure_df['Total ($US) / Person per day'].fillna(0, inplace=True)

# Now perform the groupby operation
avg_expenditure = expenditure_df.groupby('Year')['Total ($US) / Person per day'].mean()

data = pd.DataFrame({
    'Year': visitor_totals.index,
    'Visitor Arrivals': visitor_totals.values,
    'Average Expenditure': avg_expenditure.values,
    'Avg Temp (°C)': weather_df['Average Temperature (°C)'],
    'Rainfall (mm)': weather_df['Rainfall (mm)'],
    'GDP Growth (%)': economic_df['GDP Growth (%)']
})

st.write("Combined Dataset")
st.write(data)

# Model Training
st.header("Visitor Arrivals Prediction")
train = data[data['Year'] < 2015]
test = data[data['Year'] >= 2015]
X_train = train.drop(columns=['Visitor Arrivals', 'Year'])
y_train = train['Visitor Arrivals']
X_test = test.drop(columns=['Visitor Arrivals', 'Year'])
y_test = test['Visitor Arrivals']

rf_model = RandomForestRegressor(n_estimators=100, random_state=0)
rf_model.fit(X_train, y_train)

predictions = rf_model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
st.write("Mean Absolute Error for Visitor Predictions:", mae)

# Plot the predictions
fig, ax = plt.subplots()
ax.plot(data['Year'], data['Visitor Arrivals'], label='Actual Visitors')
ax.plot(test['Year'], predictions, label='Predicted Visitors', linestyle='--')
ax.set_xlabel('Year')
ax.set_ylabel('Visitor Arrivals')
ax.set_title('Visitor Arrivals Prediction')
ax.legend()
st.pyplot(fig)

# Expenditure Forecast using ARIMA
st.header("Expenditure Forecast")
expenditure_model = ARIMA(avg_expenditure, order=(1, 1, 1))
expenditure_fit = expenditure_model.fit()
expenditure_forecast = expenditure_fit.forecast(steps=3)  # Predict for 2016-2018
st.write("Expenditure Forecast for 2016-2018:")
st.write(expenditure_forecast)

# Plot expenditure forecast
forecast_years = [2016, 2017, 2018]
fig, ax = plt.subplots()
ax.plot(data['Year'], data['Average Expenditure'], label='Actual Expenditure')
ax.plot(forecast_years, expenditure_forecast, label='Forecast Expenditure', linestyle='--')
ax.set_xlabel('Year')
ax.set_ylabel('Average Expenditure ($US per day)')
ax.set_title('Expenditure Forecast')
ax.legend()
st.pyplot(fig)

# Footer
st.markdown("---")  # This creates a horizontal line
st.markdown(
    "<footer style='text-align: center; font-size: 12px;'>© 2024 SoftWave Solutions Trade and Services. All rights reserved.</footer>",
    unsafe_allow_html=True)
