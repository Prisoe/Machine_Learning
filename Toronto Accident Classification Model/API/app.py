from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import logging
from joblib import load
from KSI_Group_1_section_402COMP247Project import (
    scale_lat_long,
    bintime_to_timeofday,
    timebin_to_numerical,
)  # Import your functions
import pandas as pd

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Load the trained model
try:
    with open("xgb_model.pkl", "rb") as file:
        loaded_model = pickle.load(file)
    logging.info("Model loaded successfully!")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    loaded_model = None

# Load the scaler (saved during training)
try:
    scaler = load("lat_long_scaler.pkl")
    logging.info("Scaler loaded successfully!")
except Exception as e:
    logging.error(f"Error loading scaler: {e}")
    scaler = None

# Initialize Flask app
app = Flask(__name__)

# Mapping of prediction values to accident labels
prediction_labels = {0: "Non-Fatal Injury", 1: "Fatal", 2: "Property Damage Only"}


# Render the home page
@app.route("/")
def home():
    """
    Render the home page (home.html).
    """
    return render_template("home.html")


# Function to preprocess datetime input
def preprocess_datetime(datetime_str):
    """
    Preprocesses a datetime string from the frontend datetime picker.

    Parameters:
        datetime_str (str): Datetime input in ISO format (e.g., "2025-04-10T14:00").

    Returns:
        dict: Dictionary with extracted features {YEAR, TIME_BIN_NUM, MONTH, DAY_OF_WEEK}.
    """
    try:
        # Convert the datetime string into a Pandas datetime object
        datetime_obj = pd.to_datetime(datetime_str)

        # Extract DATE components
        year = datetime_obj.year
        month = datetime_obj.month
        day_of_week = datetime_obj.weekday()  # 0 = Monday, 6 = Sunday

        # Extract TIME component and use existing functions
        hour = datetime_obj.hour
        time_bin = bintime_to_timeofday(hour)  # Map hour to time-of-day category
        time_bin_num = timebin_to_numerical(time_bin)  # Convert time-of-day category to numerical value

        # Return the extracted features as a dictionary
        return {
            "YEAR": year,
            "MONTH": month,
            "DAY_OF_WEEK": day_of_week,
            "TIME_BIN_NUM": time_bin_num,
        }
    except Exception as e:
        raise ValueError(f"Error processing datetime: {e}")


@app.route("/predict", methods=["POST"])
def predict():
    """
    API endpoint to handle predictions with 24 features.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Preprocess datetime
        if "datetime" not in data:
            return jsonify({"error": "Datetime input is missing"}), 400

        # Call the preprocess_datetime function
        datetime_features = preprocess_datetime(data["datetime"])
        data.update(datetime_features)  # Add extracted features to the data dictionary
        del data["datetime"]  # Remove the original datetime field

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Define expected features
    required_features = [
        "ROAD_CLASS",
        "LATITUDE",
        "LONGITUDE",
        "ACCLOC",
        "VISIBILITY",
        "RDSFCOND",
        "INVTYPE",
        "INJURY",
        "VEHTYPE",
        "DRIVCOND",
        "PEDTYPE",
        "PEDACT",
        "PEDCOND",
        "PEDESTRIAN",
        "MOTORCYCLE",
        "TRUCK",
        "TRSN_CITY_VEH",
        "PASSENGER",
        "SPEEDING",
        "ALCOHOL",
        "YEAR",
        "TIME_BIN_NUM",
        "MONTH",
        "DAY_OF_WEEK",
    ]

    # Validate input data
    if not all(feature in data for feature in required_features):
        missing_features = [f for f in required_features if f not in data]
        return jsonify({"error": f"Missing features: {missing_features}"}), 400

    try:
        # Create a DataFrame for latitude and longitude with feature names
        user_lat_long = pd.DataFrame([[data["LATITUDE"], data["LONGITUDE"]]], columns=["LATITUDE", "LONGITUDE"])
        scaled_lat_long, _ = scale_lat_long(user_lat_long, scaler=scaler)
        data["LATITUDE"], data["LONGITUDE"] = scaled_lat_long[0]  # Update with scaled values

        # Extract features in the correct order
        input_features = np.array([[data[feature] for feature in required_features]])

        # Get prediction from the model
        prediction = int(loaded_model.predict(input_features)[0])

        # Get corresponding label
        prediction_label = prediction_labels.get(prediction, "Unknown Classification")

        return jsonify({"prediction": prediction, "label": prediction_label})
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": "Prediction failed"}), 500

@app.route('/plots')
def visualizations():
    plots = [
        {"filename": "Figure_1.png", "title": "Clustered Accident Locations", "caption": "Geographical clustering of accidents across Toronto regions."},
        {"filename": "Figure_1_.png", "title": "Yearly Trend of Accidents (2006–2023)", "caption": "Annual accident frequency showing post-COVID dips."},
        {"filename": "Figure_2.png", "title": "Accident Concentrations by Category", "caption": "Distribution of pedestrian, cyclist, and vehicle-only accidents."},
        {"filename": "Figure_3.png", "title": "Severity by Cluster", "caption": "Severity distribution across city zones."},
        {"filename": "Figure_4.png", "title": "Severity by Time of Day", "caption": "Injury severity based on the time of the day."},
        {"filename": "Figure_5.png", "title": "Severity by Condition", "caption": "Impact of light, weather, and road conditions on severity."},
        {"filename": "Figure_6.png", "title": "Hourly Accident Distribution", "caption": "Peak periods for accidents across hours."},
        {"filename": "Figure_7.png", "title": "Injury Severity Breakdown", "caption": "Proportion of injuries by type in the dataset."},
        {"filename": "Figure_8.png", "title": "Accident Classifications", "caption": "Number of accidents by classification."},
        {"filename": "Figure_9.png", "title": "Co-occurrence Matrix", "caption": "Correlation between conditions and accident involvement."},
        {"filename": "Figure_11.png", "title": "Entities in Accidents", "caption": "Normalized trend of vehicles/pedestrians involved."},
        {"filename": "Figure_12.png", "title": "Accident Reasons Over Time", "caption": "Reason-based heatmap for yearly trends."},
        {"filename": "Figure_13.png", "title": "Confusion Matrix (XGBoost)", "caption": "Classification accuracy per class."},
        {"filename": "Figure_14.png", "title": "ROC Curve (XGBoost)", "caption": "Model discrimination power visualized with ROC."}
    ]
    return render_template("plots.html", plots=plots)

@app.route('/info')
def prediction_info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
