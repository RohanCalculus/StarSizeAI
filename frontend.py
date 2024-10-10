import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Set the page configuration with a title and star emoji
st.set_page_config(
    page_title="Star Size Predictor 🌠",
    page_icon="🌟"
)

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
    margin-bottom: 20px;
}}
</style>
"""

# Inject the CSS to the app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and description of the app
st.title("Star Size Predictor ✨")

# Golden yellow container with a message
st.markdown("""
<div class="yellow-container">
    <p>This app will predict the Star Size based on its Brightness Value!</p>
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
    <p>To test this application, you can download a sample CSV file <a href="https://drive.google.com/uc?id=1Rp8JATmZGsTv-mlYz9KzTgYJDB4DlC5c" target="_blank">here</a>.</p>
</div>
""", unsafe_allow_html=True)

# Define the FastAPI endpoints
PREDICT_ENDPOINT = "http://127.0.0.1:8000/predict/"
PLOT_ENDPOINT = "http://127.0.0.1:8000/plot/"

# Initialize session state to track the last uploaded file
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# Check if a new file is uploaded (different from the last one)
if uploaded_file is not None:
    # If a new file is uploaded, clear session state and reinitialize
    if uploaded_file != st.session_state.last_uploaded_file:
        st.session_state.clear()  # Clear session state to restart the app
        st.session_state.last_uploaded_file = uploaded_file  # Store the new file

    # Read the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Send the file to the FastAPI predict endpoint
    with st.spinner("Generating predictions..."):
        response = requests.post(PREDICT_ENDPOINT, files={"file": uploaded_file.getvalue()})

    # Check if the request was successful
    if response.status_code == 200:
        # Read the prediction results from the response
        predicted_df = pd.read_csv(BytesIO(response.content))
        
        # Display the original and predicted CSV files side by side
        st.write("### Predictions:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Original CSV")
            st.dataframe(df)
        
        with col2:
            st.write("#### Predicted CSV")
            st.dataframe(predicted_df)

        # Button to trigger plot generation
        if st.button("Plot the Linear Regression"):
            # Now, ensure the spinner is shown for the plot generation process
            with st.spinner("Generating plot..."):
                # Convert the predicted dataframe to a CSV to send to the plot endpoint
                predicted_csv_bytes = predicted_df.to_csv(index=False).encode('utf-8')
                
                # Send the predicted CSV to the plot endpoint
                plot_response = requests.post(PLOT_ENDPOINT, files={"file": predicted_csv_bytes})
            
            if plot_response.status_code == 200:
                # Display the plot
                st.write("### Linear Regression Plot:")
                st.image(BytesIO(plot_response.content))
            else:
                st.error("Failed to generate the plot. Please try again.")
    
    else:
        st.error("Failed to generate predictions. Please try again.")
