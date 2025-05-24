
# we use both get and post here as from index.html we get our data and then me pass it to the model
# we again need to send the prediction to the html page, for that we use post

import joblib
import numpy as np
from flask import Flask, render_template, request
from config.paths_config import MODEL_OUTPUT_PATH

app = Flask(__name__)

# Load the trained model
loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None

    if request.method == "POST":
        try:
            # Extract values from the form
            lead_time = int(request.form["lead_time"])
            no_of_special_request = int(request.form["no_of_special_request"])
            avg_price_per_room = float(request.form["avg_price_per_room"])
            arrival_month = int(request.form["arrival_month"])
            arrival_date = int(request.form["arrival_date"])
            market_segment_type = int(request.form["market_segment_type"])
            no_of_week_nights = int(request.form["no_of_week_nights"])
            no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
            type_of_meal_plan = int(request.form["type_of_meal_plan"])
            room_type_reserved = int(request.form["room_type_reserved"])

            # Prepare input array for model
            input_features = np.array([[
                lead_time,
                no_of_special_request,
                avg_price_per_room,
                arrival_month,
                arrival_date,
                market_segment_type,
                no_of_week_nights,
                no_of_weekend_nights,
                type_of_meal_plan,
                room_type_reserved
            ]])

            # Make prediction
            prediction = loaded_model.predict(input_features)[0]

        except Exception as e:
            print(f"Error during prediction: {e}")
            prediction = None

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)