import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import random

# Set the page configuration with a title and star emoji
st.set_page_config(
    page_title="Star Size Predictor 🌠",
    page_icon="🌟"
)

# Define background image URLs
background_image_urls = [
    "https://i.ytimg.com/vi/tU4aKTz9Ky0/maxresdefault.jpg",
    "https://i.ytimg.com/vi/HMSRTEnV_Hw/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGEsgRihyMA8=&amp;rs=AOn4CLBVO1pirlKMXbkO0WqSMXa0OOOssQ.jpg",
    "https://i.pinimg.com/originals/04/5f/10/045f10b4643df21923387b777f56bcbb.jpg",
    "https://image.winudf.com/v2/image/Y29tLkx3cE1hc3Rlci5TcGExNDdfc2NyZWVuXzBfazg2aXh1ZG0/screen-0.jpg?fakeurl=1&type=.jpg",
    "https://steamuserimages-a.akamaihd.net/ugc/80344884637849543/48DFCE86803381928F8315C96FCF1FDD94118859/?imw=512&amp;imh=320&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true.jpg",
    "https://media.wired.com/photos/5b7f64cbbe2f8d3a624b77b2/4:3/w_2000,h_1500,c_limit/SPoW_82318_01.jpg",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5eae36e3-278f-4731-be00-1440d36eca76/d30idy4-9a4a96ed-33be-4941-99c1-8b77adb23288.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi81ZWFlMzZlMy0yNzhmLTQ3MzEtYmUwMC0xNDQwZDM2ZWNhNzYvZDMwaWR5NC05YTRhOTZlZC0zM2JlLTQ5NDEtOTljMS04Yjc3YWRiMjMyODguanBnIn1dXX0.urB7x7zyDCCRhro0z1HDVMWXZ9HJi9NgdXurlCon43Q"
]

# Check if the background is already set in session state, if not, set a random one
if 'background_image_url' not in st.session_state:
    st.session_state.background_image_url = random.choice(background_image_urls)

# Inject CSS for background image and footer
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{st.session_state.background_image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.7);
}}
.gray-container {{
    background-color: rgba(255, 255, 255, 0.8); 
    color: black;
    padding: 10px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
}}
.footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: white;
    color: black;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    border-top: 1px solid #ccc;
}}
</style>
"""

# Inject the CSS to the app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and description of the app
st.markdown('<h1 style="color: magenta;">Star Size Predictor ✨</h1>', unsafe_allow_html=True)

# Instructions on how to use the app
st.markdown("""
<div class="gray-container">
    <h4 style="color: maroon;"><u>How to use this app:</u></h4>
    <ol>
        <li><b>Enter the number of Stars to generate the dataset with its Brightness and Size Values.</b></li>
        <li><b>Click on Create Dataset and Generate Predictions Button.</b></li>
        <li><b>It will generate the dataset and also predict the star sizes using Linear Regression.</b></li>
        <li><b>Plot the True Sizes and Predicted Sizes by Linear Regression based on the Brightness values.</b></li>
        <li><b>You can now download the generated data, predicted data and the plot if needed.</b></li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Define the API endpoints for making requests using streamlit web-app
PREDICT_ENDPOINT = "https://starsize-predictor.onrender.com/predict/"
PLOT_ENDPOINT = "https://starsize-predictor.onrender.com/plot/"
CREATE_DATA_ENDPOINT = "https://starsize-predictor.onrender.com/create_data/"

### Setting up the session state ###

# Initialize session state for predictions
if 'predicted_df' not in st.session_state:
    st.session_state.predicted_df = None

# Initialize session state for generated dataset
if 'generated_df' not in st.session_state:
    st.session_state.generated_df = None

# Adding an empty line in the app for creating visual gap
st.text("")

### Code for Dataset Creation and Prediction ###

# Helper text container to allow users understand how to generate data
st.markdown("""
<div style='background-color: rgba(230, 230, 250, 0.7); padding: 0px 1px 1px 10px; border-radius: 10px;'>
    <h4 style='color: #000000;'>👇 Generate the Star Dataset with its Brightness and Size Values</h4>
</div>
""", unsafe_allow_html=True)

# Empty line for visual gap
st.text("")

# Ask user for the number of stars to generate (minimum value is 10 and default value on app will be 500)
n_samples = st.number_input("Enter the number of Stars:-", min_value=10, value=500)

# If the button is clicked
if st.button("Create Dataset and Generate Predictions"):
    
    # Ensure footer remains visible
    st.markdown("""<div class="footer">Made with ❤️ by <b>Rohan</b></div>""", unsafe_allow_html=True)
    
    # Show the spinner with a message
    with st.spinner("Generating dataset... (it may take a while if the app was idle for more than 15 minutes)"):
        # Send the post HTTP request to /create_data/ endpoint with n_samples as input parameter
        response = requests.post(CREATE_DATA_ENDPOINT, params={"n_samples": n_samples})
        
        # If the HTTP response is a success (200)
        if response.status_code == 200:
            # Update the session state of the generated dataframe from none to generated_df
            st.session_state.generated_df = pd.read_csv(BytesIO(response.content))
            
            # Use another spinner for generating predictions
            with st.spinner("Generating predictions..."):
                # Send the HTTP post request to /predict/ endpoint
                prediction_response = requests.post(PREDICT_ENDPOINT, files={"file": BytesIO(response.content)})
                
                if prediction_response.status_code == 200:
                    # Update the session state of the predicted dataframe
                    st.session_state.predicted_df = pd.read_csv(BytesIO(prediction_response.content))
                else:
                    error_message = prediction_response.json().get("error", "Unknown error occurred.")
                    st.error(f"Failed to generate predictions. Error: {error_message}.")
        else:
            error_message = response.json().get("error", "Unknown error occurred.")
            st.error(f"Failed to create dataset. Error: {error_message}.")
    



### Display the dataframes (generated and predicted) side by side ###

# Once the predicted and generated df is ready
if 'generated_df' in st.session_state and st.session_state.predicted_df is not None:
    # Get two columns for streamlit app
    col1, col2 = st.columns(2)
    # For col1 (left)
    with col1:
        # Display the Generated Dataframe
        st.write("#### Generated Dataset")
        st.dataframe(st.session_state.generated_df)
    # For col2 (right)
    with col2:
        # Display the Predicted Dataframe
        st.write("#### Predicted CSV")
        st.dataframe(st.session_state.predicted_df)

### Code for Plotting the Linear Regression Line ###

# Display the plot button only if predictions have been generated successfully
if st.session_state.predicted_df is not None:
    # If the plot button is clicked
    if st.button("Plot the Linear Regression"):
        # Ensure footer remains visible
        st.markdown("""<div class="footer">Made with ❤️ by <b>Rohan</b></div>""", unsafe_allow_html=True)

        # Display the spinner with the message
        with st.spinner("Generating plot..."):
            # Convert the predicted DataFrame to CSV format and encode it in UTF-8
            predicted_csv_bytes = st.session_state.predicted_df.to_csv(index=False).encode('utf-8')
            # Pass the predicted file as input to the /plot/ endpoint using the post HTTP request
            plot_response = requests.post(PLOT_ENDPOINT, files={"file": predicted_csv_bytes})
        # If the plot_response is a success (200)
        if plot_response.status_code == 200:
            # Display the image
            st.image(BytesIO(plot_response.content))
        else:
            # Else display the error
            error_message = plot_response.json().get("error", "Unknown error occurred.")
            st.error(f"Failed to generate the plot. Error: {error_message}. Please check if the predictions are correct and try again.")

# Footer Section
st.markdown("""
<div class="footer">
    Made with ❤️ by <b>Rohan</b>
</div>
""", unsafe_allow_html=True)