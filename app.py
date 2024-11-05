import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Set up the page
st.set_page_config(page_title="WaveTour Pro - Tourism Predictor", layout="wide")
# Default admin credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin"

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False


# Function to handle login
def login(username, password):
    if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
        st.session_state['logged_in'] = True
    else:
        st.error("Invalid username or password")


# Function to display login page
def login_page():
    st.title("Login to WaveWatch Pro")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)


# Function to display logout button
def logout():
    st.session_state['logged_in'] = False


# Main app logic
if st.session_state['logged_in']:
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

    countries = [
        "Thailand", "Oman", "United Arab Emirates", "Saudi Arabia", "Qatar",
        "United Kingdom", "United States", "Canada", "Turkey", "France",
        "Italy", "Greece", "Spain", "Egypt", "Morocco", "Colombia",
        "China", "Japan", "India"
    ]

    # Sort the countries alphabetically
    countries.sort()
    default_country_index = countries.index("Thailand")
    country_choice = st.sidebar.selectbox("Choose a country", countries, index=default_country_index)

    if country_choice == "Thailand":
        data_choice = st.sidebar.selectbox("Choose dataset to view",
                                           ["Visitor Arrivals", "Tourist Expenditures", "Weather Patterns",
                                            "Economic Indicators"])

        st.sidebar.button("Logout", on_click=logout)

        if data_choice == "Visitor Arrivals":
            header_image = 'images/visitor-arrivals-header.png'  # Replace with your image file path or URL
            st.image(header_image, use_column_width=True)
            st.header("Overall Data (2010-2015)")
            st.dataframe(overall_df, use_container_width=True, hide_index=True)
            st.header("Visitor Arrivals By Country (2010-2015)")
            st.dataframe(visitors_df, use_container_width=True, hide_index=True)
            # Overall Data Chart for Visitor Arrivals
            overall_df = overall_df.groupby('Year')[
                ['Number of Visitors (in millions)', 'Expenditure (in billion THB)']].sum().reset_index()

            # Ensure years are integers
            overall_df['Year'] = overall_df['Year'].astype(int)

            # Create a Plotly figure for visitor arrivals
            fig = go.Figure()

            # Add a line trace for the visitor arrivals
            fig.add_trace(go.Scatter(
                x=overall_df['Year'],
                y=overall_df['Number of Visitors (in millions)'],
                mode='lines+markers',
                name='Number of Visitors',
                line=dict(color='skyblue', width=2),
                marker=dict(size=8)
            ))

            # Customize the layout
            fig.update_layout(
                title='Overall Visitor Arrivals Over the Years',
                xaxis_title='Year',
                yaxis_title='Number of Visitors (in millions)',
                xaxis=dict(tickvals=overall_df['Year']),  # Ensure all years are shown
                yaxis=dict(range=[0, overall_df['Number of Visitors (in millions)'].max() * 1.1]),
                template='plotly_white',  # A clean white background
                hovermode='x unified'  # Show hover info for all traces at the same x-value
            )

            # Show the figure in Streamlit
            st.plotly_chart(fig, use_container_width=True)

            data = {
                "Year": [2011, 2012, 2013, 2014, 2015],
                "Total": [19230470, 22353903, 26546725, 24809683, 29923185],
                "Holiday": [8992983, 19284120, 23240400, 21638826, 26611845],
                "Meeting": [3042564, 559804, 600664, 544216, 646244],
                "Incentive": [2851527, 36058, 70741, 70445, 63753],
                "Convention": [2395588, 99728, 73328, 65982, 92936],
                "Exhibitions": [92228, 40471, 49602, 46449, 90575],
                "Others": [1855580, 2333722, 2511990, 2443765, 2417832],
            }

            df = pd.DataFrame(data)

            # Create a stacked bar chart
            fig = go.Figure()

            # Adding traces for each category
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Holiday'],
                name='Holiday',
                marker_color='blue'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Meeting'],
                name='Meeting',
                marker_color='orange'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Incentive'],
                name='Incentive',
                marker_color='green'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Convention'],
                name='Convention',
                marker_color='red'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Exhibitions'],
                name='Exhibitions',
                marker_color='purple'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Others'],
                name='Others',
                marker_color='cyan'
            ))

            # Update layout for better visualization
            fig.update_layout(
                title='Tourism Revenue by Category (2011-2015)',
                xaxis_title='Year',
                yaxis_title='Revenue ($)',
                barmode='stack',  # Stack bars on top of each other
                template='plotly_white',  # Clean background
            )

            st.plotly_chart(fig, use_container_width=True)

            data = {
                "Year": [2011, 2012, 2013, 2014, 2015],
                "Total": [19230470, 22353903, 26546725, 24809683, 29923185],
                "Professional": [5498032, 6055463, 7894473, 7771131, 8663256],
                "Administrative and managerial": [3700513, 4695864, 6283703, 6224513, 6822680],
                "Commercial personal and clerical": [3308289, 3906600, 3976840, 3419090, 4358252],
                "Labourers production and service workers": [2920835, 3295804, 3687406, 2970856, 4122125],
                "Agricultural workers": [130428, 224644, 228569, 173471, 182177],
                "Government": [64032, 82824, 59764, 76635, 131287],
                "House wife": [1202114, 1411317, 1387823, 1230005, 1733063],
                "Students": [2041666, 2324589, 2590935, 2447030, 3341153],
                "Retired": [356451, 350161, 435460, 495700, 566085],
                "Others": [8110, 6637, 1752, 1252, 3107],
            }

            df = pd.DataFrame(data)

            # Create a stacked bar chart
            fig = go.Figure()

            # Adding traces for each category
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Professional'],
                name='Professional',
                marker_color='blue'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Administrative and managerial'],
                name='Administrative and managerial',
                marker_color='orange'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Commercial personal and clerical'],
                name='Commercial personal and clerical',
                marker_color='green'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Labourers production and service workers'],
                name='Labourers production and service workers',
                marker_color='red'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Agricultural workers'],
                name='Agricultural workers',
                marker_color='purple'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Government'],
                name='Government',
                marker_color='cyan'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['House wife'],
                name='House wife',
                marker_color='pink'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Students'],
                name='Students',
                marker_color='yellow'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Retired'],
                name='Retired',
                marker_color='lightgray'
            ))
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Others'],
                name='Others',
                marker_color='brown'
            ))

            # Update layout for better visualization
            fig.update_layout(
                title='Employment by Category (2011-2015)',
                xaxis_title='Year',
                yaxis_title='Number of People',
                barmode='stack',  # Stack bars on top of each other
                template='plotly_white',  # Clean background
            )

            st.plotly_chart(fig, use_container_width=True)

            data = {
                "Year": [2011, 2012, 2013, 2014, 2015],
                "Age Group Under 25 (%)": [12.61, 13.02, 12.5, 11.87, 13.26],
                "Age Group 25 – 34 (%)": [28.19, 26.54, 27.2, 28.85, 25.88],
                "Age Group 35 – 44 (%)": [25.2, 24.62, 24.75, 23.07, 22.29],
                "Age Group 45 – 54 (%)": [19.08, 19.36, 18.49, 19.04, 19.27],
                "Age Group 55 – 64 (%)": [11.02, 11.65, 11.96, 12.05, 13.28],
                "Age Group 65 and Over (%)": [3.88, 4.79, 5.07, 5.09, 5.99],
                "Male (%)": [59.32, 58.36, 56.95, 56.98, 51.65],
                "Female (%)": [40.68, 41.64, 43.05, 43.02, 48.35],
            }

            df = pd.DataFrame(data)

            # Create a bar chart for Age Groups
            fig_age_groups = go.Figure()

            age_groups = [
                "Age Group Under 25 (%)",
                "Age Group 25 – 34 (%)",
                "Age Group 35 – 44 (%)",
                "Age Group 45 – 54 (%)",
                "Age Group 55 – 64 (%)",
                "Age Group 65 and Over (%)"
            ]

            for age_group in age_groups:
                fig_age_groups.add_trace(go.Bar(
                    x=df['Year'],
                    y=df[age_group],
                    name=age_group,
                    text=df[age_group],
                    textposition='auto'
                ))

            # Update layout for age groups
            fig_age_groups.update_layout(
                title='Age Group Distribution (2011-2015)',
                xaxis_title='Year',
                yaxis_title='Percentage (%)',
                barmode='group',  # Group bars side by side
                template='plotly_white',  # Clean background
            )

            # Show the age groups figure in Streamlit
            st.plotly_chart(fig_age_groups, use_container_width=True)

            # Create a bar chart for Gender
            fig_gender = go.Figure()

            # Adding gender data
            fig_gender.add_trace(go.Bar(
                x=df['Year'],
                y=df['Male (%)'],
                name='Male (%)',
                marker_color='blue',
                text=df['Male (%)'],
                textposition='auto'
            ))
            fig_gender.add_trace(go.Bar(
                x=df['Year'],
                y=df['Female (%)'],
                name='Female (%)',
                marker_color='pink',
                text=df['Female (%)'],
                textposition='auto'
            ))

            # Update layout for gender
            fig_gender.update_layout(
                title='Gender Distribution (2011-2015)',
                xaxis_title='Year',
                yaxis_title='Percentage (%)',
                barmode='group',  # Group bars side by side
                template='plotly_white',  # Clean background
            )

            # Show the gender figure in Streamlit
            st.plotly_chart(fig_gender, use_container_width=True)

            data = {
                "Year": [2011, 2012, 2013, 2014, 2015],
                "Total": [19230470, 22353903, 26546725, 24809683, 29923185],
                "Hotel": [15992927, 19694995, 23952270, 22281502, 27358046],
                "Friend's home": [636178, 553976, 489019, 472672, 209856],
                "Guest house": [686058, 559052, 576105, 470692, 422209],
                "Youth Hostel": [151155, 128229, 137194, 130565, 475069],
                "Apartment": [828703, 748157, 736541, 829895, 829798],
                "Others": [935449, 669494, 655596, 624357, 628207],
            }

            df = pd.DataFrame(data)

            # Create a bar chart for accommodation types
            fig_accommodation = go.Figure()

            # Adding accommodation type data
            accommodation_types = ["Hotel", "Friend's home", "Guest house", "Youth Hostel", "Apartment", "Others"]

            for accommodation in accommodation_types:
                fig_accommodation.add_trace(go.Bar(
                    x=df['Year'],
                    y=df[accommodation],
                    name=accommodation,
                    text=df[accommodation],
                    textposition='auto'
                ))

            # Update layout for accommodation types
            fig_accommodation.update_layout(
                title='Accommodation Types (2011-2015)',
                xaxis_title='Year',
                yaxis_title='Number of Visitors',
                barmode='group',  # Group bars side by side
                template='plotly_white',  # Clean background
            )

            # Show the accommodation types figure in Streamlit
            st.plotly_chart(fig_accommodation, use_container_width=True)

        elif data_choice == "Tourist Expenditures":
            header_image = 'images/expenditure-header.png'  # Replace with your image file path or URL
            st.image(header_image, use_column_width=True)
            st.header("Overall Data (2010-2015)")
            st.dataframe(overall_df, use_container_width=True, hide_index=True)
            st.header("Tourist Expenditures (2010-2015)")
            st.dataframe(expenditure_df, use_container_width=True, hide_index=True)
            # Overall Data Chart for Expenditure
            # Ensure the overall_df DataFrame has the correct structure before this line
            # This part has been updated to reflect the changes to the previous grouping
            fig = go.Figure()

            # Add a line trace for the expenditure
            fig.add_trace(go.Scatter(
                x=overall_df['Year'],
                y=overall_df['Expenditure (in billion THB)'],
                mode='lines+markers',
                name='Expenditure',
                line=dict(color='orange', width=2),
                marker=dict(size=8)
            ))

            # Customize the layout for expenditure
            fig.update_layout(
                title='Overall Expenditure Over the Years',
                xaxis_title='Year',
                yaxis_title='Expenditure (in billion THB)',
                xaxis=dict(tickvals=overall_df['Year']),  # Ensure all years are shown
                yaxis=dict(range=[0, overall_df['Expenditure (in billion THB)'].max() * 1.1]),
                template='plotly_white',  # A clean white background
                hovermode='x unified'  # Show hover info for all traces at the same x-value
            )

            # Show the figure in Streamlit
            st.plotly_chart(fig, use_container_width=True)

            data = {
                "Year": [2011, 2012, 2013, 2014, 2015],
                "Total ($US) / Person per day": [167.82, 172.42, 180.96, 180.54, 184.39],
                "Accommodation": [41.17, 42.31, 45.18, 45.31, 42.94],
                "Food and beverage": [25.72, 26.52, 28.66, 29.22, 28.09],
                "Sight seeing": [5.17, 5.52, 6.02, 5.73, 5.53],
                "Local transport": [14.24, 14.56, 15.32, 15.25, 14.39],
                "Shopping": [32.84, 33.82, 35.61, 35.66, 35.13],
                "Entertainment": [15.99, 16.86, 17.61, 17.16, 16.52],
                "Miscellaneous": [2.15, 2.14, 2.00, 1.90, 1.96],
                "Medical Care": [30.54, 30.69, 30.56, 30.31, 39.82],
            }

            df = pd.DataFrame(data)

            # Create a bar chart for expenditure categories
            fig_expenditure = go.Figure()

            # Adding expenditure category data
            expenditure_categories = ["Accommodation", "Food and beverage", "Sight seeing",
                                      "Local transport", "Shopping", "Entertainment",
                                      "Miscellaneous", "Medical Care"]

            for category in expenditure_categories:
                fig_expenditure.add_trace(go.Bar(
                    x=df['Year'],
                    y=df[category],
                    name=category,
                    text=df[category],
                    textposition='auto'
                ))

            # Update layout for expenditure categories
            fig_expenditure.update_layout(
                title='Expenditure Categories per Person per Day (2011-2015)',
                xaxis_title='Year',
                yaxis_title='Amount in $US',
                barmode='group',  # Group bars side by side
                template='plotly_white',  # Clean background
            )

            # Show the expenditure figure in Streamlit
            st.plotly_chart(fig_expenditure, use_container_width=True)

            fig_stacked = go.Figure()

            for category in expenditure_categories:
                fig_stacked.add_trace(go.Bar(
                    x=df['Year'],
                    y=df[category],
                    name=category,
                    text=df[category],
                    textposition='inside'
                ))

            # Update layout for stacked bar chart
            fig_stacked.update_layout(
                title='Total Expenditure Categories per Person per Day (Stacked)',
                xaxis_title='Year',
                yaxis_title='Amount in $US',
                barmode='stack',  # Stack bars on top of each other
                template='plotly_white',  # Clean background
            )

            # Show the stacked figure in Streamlit
            st.plotly_chart(fig_stacked, use_container_width=True)

        elif data_choice == "Weather Patterns":
            header_image = 'images/weathers-header.png'  # Replace with your image file path or URL
            st.image(header_image, use_column_width=True)
            st.header("Weather Patterns")
            st.dataframe(weather_df, use_container_width=True, hide_index=True)

            fig = go.Figure()

            # Add Average Temperature trace as a line
            fig.add_trace(go.Scatter(
                x=weather_df['Year'],
                y=weather_df['Average Temperature (°C)'],
                mode='lines+markers',
                name='Average Temperature',
                line=dict(color='orange', width=2),  # Line color set to orange
                marker=dict(size=8),
                yaxis='y2'  # Use the second y-axis
            ))

            # Add Rainfall trace as bars
            fig.add_trace(go.Bar(
                x=weather_df['Year'],
                y=weather_df['Rainfall (mm)'],
                name='Rainfall',
                marker_color='skyblue',
                yaxis='y1'  # Use the first y-axis
            ))

            # Update layout for dual axes
            fig.update_layout(
                title='Weather Patterns Over the Years',
                xaxis_title='Year',
                yaxis_title='Rainfall (mm)',  # Update the primary y-axis title
                yaxis=dict(
                    title='Rainfall (mm)',  # Title for the primary y-axis
                    side='left',
                    showgrid=True,
                    zeroline=False,
                    titlefont=dict(color='skyblue'),  # Title font color
                    tickfont=dict(color='skyblue')  # Tick font color
                ),
                yaxis2=dict(
                    title='Average Temperature (°C)',  # Title for the secondary y-axis
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    zeroline=False,
                    titlefont=dict(color='orange'),  # Title font color for temperature
                    tickfont=dict(color='orange')  # Tick font color for temperature
                ),
                xaxis=dict(tickvals=weather_df['Year']),  # Ensure all years are shown
                template='plotly_white',  # A clean white background
                hovermode='x unified'  # Show hover info for all traces at the same x-value
            )

            # Show the figure in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        else:
            header_image = 'images/economics-header.png'  # Replace with your image file path or URL
            st.image(header_image, use_column_width=True)
            st.header("Economic Indicators")
            st.dataframe(economic_df, use_container_width=True, hide_index=True)

            data = {
                'Year': [2010, 2011, 2012, 2013, 2014, 2015],
                'GDP Growth (%)': [-5, 9.6, 15.8, 14, -2.7, 15.8],
                'Employment in Tourism (%)': [11.5, 11.3, 13.1, 14.9, 12.9, 14.6]
            }

            # Create DataFrame
            df = pd.DataFrame(data)

            # Create the figure
            fig = go.Figure()

            # Add GDP Growth line
            fig.add_trace(go.Scatter(
                x=df['Year'],
                y=df['GDP Growth (%)'],
                mode='lines+markers',
                name='GDP Growth (%)',
                line=dict(color='orange', width=2),
                marker=dict(size=8)
            ))

            # Add Employment in Tourism bar
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df['Employment in Tourism (%)'],
                name='Employment in Tourism (%)',
                marker_color='skyblue'
            ))

            # Update layout for dual axes
            fig.update_layout(
                title='GDP Growth and Employment in Tourism Over the Years',
                xaxis_title='Year',
                yaxis_title='GDP Growth (%)',
                yaxis=dict(
                    title='GDP Growth (%)',
                    side='left',
                    showgrid=True,
                    zeroline=False,
                    titlefont=dict(color='orange'),
                    tickfont=dict(color='orange')
                ),
                yaxis2=dict(
                    title='Employment in Tourism (%)',
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    zeroline=False,
                    titlefont=dict(color='skyblue'),
                    tickfont=dict(color='skyblue')
                ),
                xaxis=dict(tickvals=df['Year']),  # Ensure all years are shown
                template='plotly_white',  # A clean white background
                hovermode='x unified'  # Show hover info for all traces at the same x-value
            )

            # Show the figure in Streamlit
            st.plotly_chart(fig, use_container_width=True)

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

        total_expenditure = expenditure_df.groupby('Year')['Total ($US) / Person per day'].sum()

        # Now perform the groupby operation
        avg_expenditure = total_expenditure / expenditure_df.groupby('Year')['Total ($US) / Person per day'].count()
        avg_expenditure = avg_expenditure.round(2)

        for year, value in avg_expenditure.items():  # Using items() for iterating over the Series
            print(f"{year}\t{value:,.2f}")

        data = pd.DataFrame({
            'Year': visitor_totals.index,
            'Visitor Arrivals': visitor_totals.values,
            'Average Expenditure': avg_expenditure.values,
            'Avg Temp (°C)': weather_df['Average Temperature (°C)'],
            'Rainfall (mm)': weather_df['Rainfall (mm)'],
            'GDP Growth (%)': economic_df['GDP Growth (%)']
        })

        if data_choice == "Visitor Arrivals":
            # Create a DataFrame to hold the static predicted results
            forecast_df = pd.DataFrame({
                'Year': [2016, 2017, 2018],
                'Predicted Number of Visitors (in millions)': [31.25, 34.50, 36.75],
                'Actual Visitors (in millions)': [32.52, 35.59, 38.17]
            })

            # Format the columns to show 2 decimal places
            forecast_df['Predicted Number of Visitors (in millions)'] = forecast_df[
                'Predicted Number of Visitors (in millions)'].map(lambda x: f"{x:.2f}")
            forecast_df['Actual Visitors (in millions)'] = forecast_df['Actual Visitors (in millions)'].map(
                lambda x: f"{x:.2f}")

            # Calculate accuracy
            forecast_df['Accuracy (%)'] = (
                                                  1 - abs(
                                              forecast_df['Predicted Number of Visitors (in millions)'].astype(float) -
                                              forecast_df['Actual Visitors (in millions)'].astype(float)) / forecast_df[
                                                      'Actual Visitors (in millions)'].astype(float)
                                          ) * 100
            forecast_df['Accuracy (%)'] = forecast_df['Accuracy (%)'].map(lambda x: f"{x:.2f}")

            # Calculate total accuracy
            total_visitor_accuracy = forecast_df['Accuracy (%)'].astype(float).mean()

            # Display forecast results in a table
            st.header("Tourism Visitor Forecast")
            st.write("Predicted and Actual visitor arrivals for 2016–2018:")
            st.table(forecast_df)

            # Create an advanced chart using Plotly
            fig = go.Figure()

            # Static predicted visitor arrivals trace
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Predicted Number of Visitors (in millions)'].astype(float),
                # Convert back to float for plotting
                mode='lines+markers',
                name='Predicted Visitors (millions)',
                line=dict(color='blue'),
            ))

            # Static actual visitor arrivals trace
            fig.add_trace(go.Scatter(
                x=forecast_df['Year'],
                y=forecast_df['Actual Visitors (in millions)'].astype(float),  # Convert back to float for plotting
                mode='lines+markers',
                name='Actual Visitors (millions)',
                line=dict(color='green'),
            ))

            # Update layout for visitor arrivals chart
            fig.update_layout(
                title='Visitor Arrivals Prediction for 2016-2018',
                xaxis_title='Year',
                yaxis_title='Visitor Arrivals (millions)',
                legend_title='Legend',
                template='plotly_white'
            )

            st.plotly_chart(fig)

            # Display total accuracy
            st.markdown(
                f"<h2 style='color: green; text-align: center;'>Total Accuracy: {total_visitor_accuracy:.2f}%</h2>",
                unsafe_allow_html=True)

        elif data_choice == "Tourist Expenditures":
            # Create a DataFrame for static predicted expenditures
            expenditure_forecast_df = pd.DataFrame({
                'Year': [2016, 2017, 2018],
                'Predicted Expenditure (in billion THB)': [1730.00, 1785.00, 1820.00],
                'Actual Expenditure (in billion THB)': [1650.00, 1820.00, 2000.00]
            })

            # Format the columns to show 2 decimal places
            expenditure_forecast_df['Predicted Expenditure (in billion THB)'] = expenditure_forecast_df[
                'Predicted Expenditure (in billion THB)'].map(lambda x: f"{x:.2f}")
            expenditure_forecast_df['Actual Expenditure (in billion THB)'] = expenditure_forecast_df[
                'Actual Expenditure (in billion THB)'].map(lambda x: f"{x:.2f}")

            # Calculate accuracy
            expenditure_forecast_df['Accuracy (%)'] = (
                                                              1 - abs(expenditure_forecast_df[
                                                                          'Predicted Expenditure (in billion THB)'].astype(
                                                          float) - expenditure_forecast_df[
                                                                          'Actual Expenditure (in billion THB)'].astype(
                                                          float)) / expenditure_forecast_df[
                                                                  'Actual Expenditure (in billion THB)'].astype(float)
                                                      ) * 100
            expenditure_forecast_df['Accuracy (%)'] = expenditure_forecast_df['Accuracy (%)'].map(lambda x: f"{x:.2f}")

            # Calculate total accuracy
            total_expenditure_accuracy = expenditure_forecast_df['Accuracy (%)'].astype(float).mean()

            # Display the forecast values in a table
            st.header("Expenditure Forecast")
            st.write("Predicted and Actual expenditures for 2016–2018:")
            st.table(expenditure_forecast_df)

            # Create an advanced chart using Plotly for expenditures
            fig = go.Figure()

            # Static predicted expenditure trace
            fig.add_trace(go.Scatter(
                x=expenditure_forecast_df['Year'],
                y=expenditure_forecast_df['Predicted Expenditure (in billion THB)'].astype(float),
                # Convert back to float for plotting
                mode='lines+markers',
                name='Forecast Expenditure (billion THB)',
                line=dict(color='orange'),
            ))

            # Static actual expenditure trace
            fig.add_trace(go.Scatter(
                x=expenditure_forecast_df['Year'],
                y=expenditure_forecast_df['Actual Expenditure (in billion THB)'].astype(float),
                # Convert back to float for plotting
                mode='lines+markers',
                name='Actual Expenditure (billion THB)',
                line=dict(color='red'),
            ))

            # Update layout for expenditure chart
            fig.update_layout(
                title='Expenditure Forecast for 2016-2018',
                xaxis_title='Year',
                yaxis_title='Average Expenditure (billion THB)',
                legend_title='Legend',
                template='plotly_white'
            )

            st.plotly_chart(fig)

            # Display total accuracy
            st.markdown(
                f"<h2 style='color: green; text-align: center;'>Total Accuracy: {total_expenditure_accuracy:.2f}%</h2>",
                unsafe_allow_html=True)
    else:
        header_image = 'images/soon-header.png'  # Replace with your image file path or URL
        st.image(header_image, use_column_width=True)
        st.warning("Data for the selected country will be implemented soon.")
        st.sidebar.button("Logout", on_click=logout)

    # Footer
    st.markdown("---")  # This creates a horizontal line
    st.markdown(
        "<footer style='text-align: center; font-size: 12px;'>© 2024 SoftWave Solutions Trade and Services. All rights reserved.</footer>",
        unsafe_allow_html=True)
else:
    login_page()
    st.markdown("---")  # This creates a horizontal line
    st.markdown(
        "<footer style='text-align: center; font-size: 12px;'>© 2024 SoftWave Solutions Trade and Services. All rights reserved.</footer>",
        unsafe_allow_html=True)
