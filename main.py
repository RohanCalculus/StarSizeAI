# Libraries to develop the API
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Libraries to handle the data and visualization
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io

# Create an instance of the FastAPI application
app = FastAPI()

# Set up CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://starsize.streamlit.app/"],  # Only this origin will be allowed to make request to API
    allow_credentials=True, # Allows the server to include cookies in cross-origin requests
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)

# Constants for the linear regression model (taken from training_star_size_predictor.ipynb)
W = 1.982015  # Weight (slope) for the linear model
b = 9.500380  # Bias (intercept) for the linear model

@app.get('/')
def default():
    """
    Default endpoint to check if the application is running.
    
    Returns:
        dict: A simple message indicating the application is running.
    """
    return {'App': 'Running'}

@app.post("/create_data/")
async def create_data(n_samples: int = Query(500, description="Number of samples to generate")):
    """
    Endpoint to generate a dataset for the Star Type Predictor App.

    Args:
        n_samples (int): Number of samples to generate.

    Returns:
        StreamingResponse: CSV file containing the generated dataset.
    """

    # Generate Data
    X_test = 3 * np.random.rand(n_samples, 1)
    y_test = 9 + 2 * X_test + np.random.rand(n_samples, 1)

    # Convert arrays into dict
    dict_info = {
        'Brightness': X_test.flatten(),
        'True Size': y_test.flatten()
    }

    # Convert dict to pandas dataframe
    input_df = pd.DataFrame(dict_info)

    # Convert the DataFrame to CSV format
    output = input_df.to_csv(index=False).encode('utf-8')

    # Return the CSV file as a streaming response
    return StreamingResponse(io.BytesIO(output),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=input_star_data.csv"})

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint to perform predictions based on input data.

    Args:
        file (UploadFile): CSV file containing 'inputs' and 'targets'.

    Returns:
        StreamingResponse: CSV file with predictions attached.
    """
    # Read the contents of the uploaded file
    contents = await file.read()
    
    # Load the CSV data into a DataFrame
    df = pd.read_csv(io.BytesIO(contents))
    
    # Rename columns for clarity
    df.columns = ['inputs', 'targets']
    
    # Calculate predictions using the linear regression formula: y = Wx + b
    df['predictions'] = W * df['inputs'] + b
    
    # Convert the DataFrame with predictions to CSV format
    output = df.to_csv(index=False).encode('utf-8')
    
    # Return the CSV file as a streaming response
    return StreamingResponse(io.BytesIO(output),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=predictions.csv"})

@app.post("/plot/")
async def plot(file: UploadFile = File(...)):
    """
    Endpoint to generate a plot comparing actual targets with predictions.

    Args:
        file (UploadFile): CSV file containing 'inputs' and 'targets'.

    Returns:
        StreamingResponse: Image file of the plot.
    """
    # Read the contents of the uploaded file
    contents = await file.read()
    
    # Load the CSV data into a DataFrame
    df = pd.read_csv(io.BytesIO(contents))
    
    # Set up the plot
    plt.figure(figsize=(10, 6))
    
    # Scatter plot for actual targets
    plt.scatter(df['inputs'], df['targets'], color='royalblue', label='Actual Targets', marker='x')
    
    # Calculate predictions and RMSE
    df['predictions'] = W * df['inputs'] + b
    rmse_score = np.mean(np.square(df['predictions'].values - df['targets'].values))
    
    # Plot the predictions line
    plt.plot(df['inputs'], df['predictions'], color='k', label='Predictions', linewidth=2)
    
    # Title and labels for the plot
    plt.title(f'Linear Regression for Stars Data (RMSE: {round(rmse_score, 3)})', color='maroon', fontsize=15, weight='bold')
    plt.xlabel('Brightness of the Stars', color='m', fontsize=13)
    plt.ylabel('Size of the Stars', color='m', fontsize=13)
    plt.legend()  # Show legend
    
    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Reset buffer position
    plt.close()  # Close the plot to free up memory
    
    # Return the plot as a streaming response
    return StreamingResponse(buf,
                             media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=plot.png"})
