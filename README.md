# Star Size Prediction App

## Overview

The Star Size Prediction App is a web application that predicts the sizes of stars based on their brightness using a linear regression model. The application is built using FastAPI for the backend and Streamlit for the frontend.

## Notes
1. Training of this linear regression model was done using [this notebook](https://github.com/SpartificialUdemy/StarSizeApp/blob/main/training.ipynb).
2. Input csv can be generated using [data.py](https://github.com/SpartificialUdemy/StarSizeApp/blob/main/data.py).
3. As you can see this was a demo data used to demonstrate linear regression.
4. It creates a dummy linear relationship between brightness and size of stars (dummy variables).

## Features

- Upload a CSV file containing brightness and size data.
- Generate predictions based on the input data.
- Visualize the predictions alongside the actual values in a linear regression plot.

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Deployment**: Render.com (for the FastAPI app)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- pip (Python package manager)

### Clone the Repository

```
git clone <repository-url>  
cd star-size-prediction-app
```

### Create and activate virtual environment
```
python -m venv <name_of_venv>
```
```
.\<name_of_venv>\Scripts\activate
```

### Install Dependencies

You can install all the dependencies for backend and frontend using the following command:-
```
python -m pip install -r requirements.txt
```

### Running the Application on Local Server (for development)

#### Backend

To start the FastAPI backend:-
```
uvicorn main:app --reload
```

#### Frontend

To start the Streamlit frontend (make sure API is hosted before running the frontend):-
```
streamlit run frontend.py
```

### Accessing the Application

Once both the backend and frontend are running, you can access the Streamlit app at:
```
http://localhost:8501
```

## Using the Application

1. **Upload CSV File**: Click on the file uploader to select a CSV file. The file should contain two columns:
   - **Column 1**: Brightness of the stars (numeric values)
   - **Column 2**: Size of the stars (numeric values)

2. **Generate Predictions**: The application will automatically generate predictions based on the uploaded data.

3. **View Results**: The app displays the original data alongside the predicted sizes.

4. **Plotting**: Click on the "Plot Linear Regression" button to visualize the predictions in a scatter plot with a line of best fit.

## API Endpoints

- **GET /**: Check if the API is running.
- **POST /predict/**: Upload a CSV file to receive predictions.
- **POST /plot/**: Upload a CSV file to generate a plot of actual vs predicted values.

## Deployment

The FastAPI backend is deployed on Render.com and streamlit frontend is deployed on Streamlit cloud. 
- **Full App can be accessed using**:- `https://star-size.streamlit.app/`

## Acknowledgments

- Thanks to [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/) for their excellent frameworks.
- Special thanks to the contributors and open-source community for their support.
