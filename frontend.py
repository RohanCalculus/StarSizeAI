import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Set the page configuration with a title and star emoji
st.set_page_config(
    page_title="Star Size Predictor 🌠",
    page_icon="🌟"
)

# URL for the background image
background_image_url = "https://4kwallpapers.com/images/walls/thumbs_3t/10307.jpg"

# Custom CSS for styling
st.markdown(f"""
    <style>
        body {{
            background-image: url('{background_image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            color: rgba(0, 0, 0, 1);
            background-color: rgba(255, 255, 255, 0.7);
            text-align: center;
            padding: 10px;
            z-index: 1000;  /* Ensure it's on top of other elements */
        }}

        /* Create space at the bottom of the app for the footer */
        .content {{
            padding-bottom: 60px;  /* Adjust based on footer height */
        }}

        [data-testid="stAppViewContainer"] {{
            padding-bottom: 60px;  /* Adjust this to match the footer height */
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
""", unsafe_allow_html=True)

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

# Initialize session state to track the last uploaded file
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# Add a div with the class 'content' to wrap your main content
st.markdown('<div class="content">', unsafe_allow_html=True)

# File upload section
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

# Define the FastAPI endpoints
PREDICT_ENDPOINT = "https://star-size-predictor.onrender.com/predict/"
PLOT_ENDPOINT = "https://star-size-predictor.onrender.com/plot/"

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
            with st.spinner("Generating plot..."):
                predicted_csv_bytes = predicted_df.to_csv(index=False).encode('utf-8')
                plot_response = requests.post(PLOT_ENDPOINT, files={"file": predicted_csv_bytes})
            
            if plot_response.status_code == 200:
                st.write("### Linear Regression Plot:")
                st.image(BytesIO(plot_response.content))
            else:
                st.error("Failed to generate the plot. Please try again.")
    
    else:
        st.error("Failed to generate predictions. Please try again.")

# Close the content div
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>This is a demo project built as a part of ML4A Training Program</p>
    </div>
""", unsafe_allow_html=True)
