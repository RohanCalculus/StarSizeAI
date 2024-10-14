import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Set the page configuration with a title and star emoji
st.set_page_config(
    page_title="Star Size Predictor 🌠",
    page_icon="🌟"
)

st.markdown("""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 1);
            color: rgba(0, 0, 0, 1);
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            z-index: 1000;
        }

        /* Add padding at the bottom to avoid overlap with the footer */
        .stApp {
            padding-bottom: 50px;
        }
    </style>
    <div class="footer">
        <p>This is a demo project built as a part of the ML for Astronomy Training Program at Spartificial.</p>
    </div>
""", unsafe_allow_html=True)

# Custom CSS to set the background image and style the containers
background_image_url = "https://4kwallpapers.com/images/walls/thumbs_3t/10307.jpg"  # Replace with your image URL

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.7);
}}

.black-container {{
    background-color: black;
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 16px;
    line-height: 1.6;
}}

.yellow-container {{
    background-color: #FFD700;  /* Golden yellow */
    color: black;
    padding: 10px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
}}

.green-container {{
    background-color: #006400;  /* Dark Green */
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-top: 20px;
    font-size: 18px;
    line-height: 1.6;
}}
</style>
"""

# Inject the CSS to the app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and description of the app
st.title("Star Size Predictor ✨")

# Updated "yellow-container" for app description
st.markdown("""
<div class="yellow-container">
    <p>This app will predict the Star Size based on its Brightness Value!</p>
</div>
""", unsafe_allow_html=True)

# New blue container for step-by-step instructions on how to use the app
st.markdown("""
<div class="green-container">
    <h4>How to use this app:</h4>
    <ol>
        <li><b><a href="https://drive.google.com/uc?id=1Rp8JATmZGsTv-mlYz9KzTgYJDB4DlC5c" target="_blank">Download</a> a sample CSV or <a href="https://github.com/SpartificialUdemy/project_1/blob/main/create_data.py" target="_blank">create your own</a> in case you don't have the dataset</b></li>
        <li><b>Upload a CSV file (instructions given below)</b></li>
        <li><b>Wait for predictions to be displayed</b></li>
        <li><b>Plot the Linear Regression Results</b></li>
        <li><b>You can download the prediction.csv and plot.png files if needed</b></li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Add a black-colored container with white text to explain the CSV format
st.markdown("""
<div class="black-container">
    <h4>How your CSV file should look:</h4>
    <p>The CSV file you upload should contain exactly two columns:</p>
    <ul>
        <li><b>First column:</b> Brightness of the stars (numerical values).</li>
        <li><b>Second column:</b> Size of the stars (numerical values).</li>
    </ul>
    <p>Ensure there are no extra columns or missing values for accurate predictions.</p>
</div>
""", unsafe_allow_html=True)

# Define the FastAPI endpoints
PREDICT_ENDPOINT = "https://star-size-predictor.onrender.com/predict/"
PLOT_ENDPOINT = "https://star-size-predictor.onrender.com/plot/"

# Initialize session state to track the last uploaded file
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# Initialize session state for predictions
if 'predicted_df' not in st.session_state:
    st.session_state.predicted_df = None

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# Check if a new file is uploaded (different from the last one)
if uploaded_file is not None:
    # If a new file is uploaded, clear session state and reinitialize
    if uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.clear()  # Clear session state to restart the app
        st.session_state.last_uploaded_file = uploaded_file  # Store the new file
        st.session_state.predicted_df = None  # Reset predictions

    # Read the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Check if predictions are already stored in the session state
    if st.session_state.predicted_df is None:
        # Send the file to the FastAPI predict endpoint
        with st.spinner("Generating predictions... (it may take a few mins if the app was idle for more than 15 minutes)."):
            response = requests.post(PREDICT_ENDPOINT, files={"file": uploaded_file.getvalue()})

        # Check if the request was successful
        if response.status_code == 200:
            # Read the prediction results from the response
            st.session_state.predicted_df = pd.read_csv(BytesIO(response.content))  # Store predictions in session state
        else:
            st.error("Failed to generate predictions. Please try again.")
    
    # Display the original and predicted CSV files side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Original CSV")
        st.dataframe(df)
    
    with col2:
        st.write("#### Predicted CSV")
        st.dataframe(st.session_state.predicted_df)

    # Button to trigger plot generation
    if st.button("Plot the Linear Regression"):
        # Ensure the spinner is shown for the plot generation process
        with st.spinner("Generating plot..."):
            # Convert the predicted dataframe to a CSV to send to the plot endpoint
            predicted_csv_bytes = st.session_state.predicted_df.to_csv(index=False).encode('utf-8')
            
            # Send the predicted CSV to the plot endpoint
            plot_response = requests.post(PLOT_ENDPOINT, files={"file": predicted_csv_bytes})
        
        if plot_response.status_code == 200:
            # Display the plot
            st.image(BytesIO(plot_response.content))
        else:
            st.error("Failed to generate the plot. Please try again.")