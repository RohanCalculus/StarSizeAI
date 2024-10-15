# Predicting Star Sizes with Artificial Intelligence 🌠

This [web-application](https://starsize.streamlit.app/) allows you to do the following:
1. Generate a synthetic dataset of stars with `n` number of stars provided by the user as input.
2. This dataset includes the synthetic brightness of the stars and respective synthetic true sizes.
3. It then uses artificial intelligence (specifically, linear regression) to predict the star sizes based on the brightness values of the stars.
4. It will then allow you to plot the predictions and see how the model performed on this unseen dataset.

## Why Synthetic Dataset is Being Used?
* This is a tutorial project to help students at Spartificial understand how the linear regression algorithm works using a gradient descent optimizer.
* The aim was to help students first build the dataset using a true output equation and by adding noise, we aimed to generate the equation of prediction.
* This allowed our students to understand how the weight (coefficient) and bias (intercept) in the equation were optimized using gradient descent to get the optimal values.
* These values of weight and bias were then used to build the web application.
* Future projects will allow them to work on real astronomical datasets to test their machine learning skills!

## How to Set Up This Project on Your System
1. Clone this repository using the web URL given below or download the ZIP file.
   ```bash
   git clone https://github.com/SpartificialUdemy/project_1.git
   ```

2. Create the virtual environment in your system:
   - **Windows**
   ```bash
   python -m venv venv
   ```
   - **Linux or Mac**
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**
   ```bash
   venv\Scripts\activate
   ```
   - **Linux or Mac**
   ```bash
   source venv/bin/activate
   ```

4. Install the requirements:
   - **Windows**
   ```bash
   python -m pip install -r requirements.txt
   ```
   - **Linux or Mac**
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend powered by FastAPI using Uvicorn:
   ```bash
   uvicorn main:app 
   ```

6. Run the frontend powered by Streamlit:
   ```bash
   streamlit run frontend.py
   ```

## Tools used in This Project
1. **FastAPI** - To build the API endpoints
2. **Streamlit** - To build and host the frontend of the web application
3. **Render** - To host the backend API built using FastAPI
4. **NumPy** - To create the synthetic dataset for training, validation, testing, and the web application
5. **Matplotlib** - To visualize the cost vs iterations and in the web application to visualize the regression line
6. **Pandas** - To read CSV files, create the dataframe, and save dataframes back to CSV


## Demonstration of the Web Application - Star Size Predictor
<a href="https://youtu.be/2mpu0_Wn1l8" target="_blank">
    <img src="https://github.com/SpartificialUdemy/project_1/blob/main/video-thumbnail.png" alt="Watch the video" width="65%" />
</a>

