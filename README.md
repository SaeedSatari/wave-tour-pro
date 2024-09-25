# WaveTour Pro

WaveTour Pro is a prediction solution designed to predict tourist behavior based on various input features such as
month, temperature, local events, and holiday season developer by SoftWave Solutions Trade and Services. The application
uses a machine learning model trained on tourism data to provide predictions on visitor numbers.

## Features

- Predict the number of visitors based on input features.
- Visualizations of monthly visitors and their distribution.
- Interactive input fields for user-friendly experience.

## Prerequisites

- Docker installed on your machine.

## Installation

### Using Docker

1. Clone this repository:

   ```bash
   git clone https://github.com/SaeedSatari/wave-tour-pro.git
   cd wavetour-pro
   ```

2. Build the Docker image:

   ```bash
   docker build -t wave_tour_pro .
   ```

3. Run the Docker container:

   ```bash
   docker run -p 8501:8501 wave_tour_pro
   ```

4. Open your web browser and go to `http://localhost:8501` to access the app.

### Without Docker

If you prefer to run the app without Docker, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/SaeedSatari/wave-tour-pro.git
   cd wavetour-pro
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. Open your web browser and go to `http://localhost:8501` to access the app.

## Usage

- Input the features (month, temperature, local events, holiday season) in the provided fields.
- Click the "Predict Visitors" button to see the predicted number of visitors.
- Explore the data visualizations below the prediction results.

## Contact

For inquiries or suggestions, please contact:

**SoftWave Solutions Trade and Services LLC**  
- **Saeed Sattari**  
  CEO, SoftWave Solutions Trade and Services LLC  
  saeed@softwaveco.com