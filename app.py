# import joblib
# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Load trained model
# model = joblib.load("game_sales_model.pkl")

# # Load label encoders
# encoders = joblib.load("label_encoders.pkl")


# # Home Page
# @app.route("/")
# def home():
#     return render_template("index.html")


# # Prediction
# @app.route("/predict", methods=["POST"])
# def predict():

#     platform = request.form["platform"]
#     year = int(request.form["year"])
#     genre = request.form["genre"]
#     publisher = request.form["publisher"]

#     # Convert text into numbers
#     platform = encoders["Platform"].transform([platform])[0]
#     genre = encoders["Genre"].transform([genre])[0]
#     publisher = encoders["Publisher"].transform([publisher])[0]

#     # Predict
#     prediction = model.predict([[platform, year, genre, publisher]])

#     return render_template(
#         "result.html",
#         prediction=round(prediction[0], 2)
#     )


# if __name__ == "__main__":
#     app.run(debug=True)

import joblib
from flask import Flask, render_template, request, redirect, url_for, flash

from database import (
    init_db, save_prediction, get_all_predictions,
    delete_prediction, clear_history,
)

app = Flask(__name__)
app.secret_key = "change-this-secret-key"   # needed for flash messages

# Load trained model
model = joblib.load("game_sales_model.pkl")

# Load label encoders
encoders = joblib.load("label_encoders.pkl")

# Create the history table when the app starts
init_db()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Prediction
@app.route("/predict", methods=["POST"])
def predict():
    # Keep the original readable values (these get stored in history)
    platform_name = request.form["platform"]
    year = int(request.form["year"])
    genre_name = request.form["genre"]
    publisher_name = request.form["publisher"]

    # Convert text into numbers
    platform = encoders["Platform"].transform([platform_name])[0]
    genre = encoders["Genre"].transform([genre_name])[0]
    publisher = encoders["Publisher"].transform([publisher_name])[0]

    # Predict
    prediction = model.predict([[platform, year, genre, publisher]])
    predicted_sales = round(float(prediction[0]), 2)

    # Save to history (NEW)
    save_prediction(platform_name, year, genre_name, publisher_name, predicted_sales)

    return render_template("result.html", prediction=predicted_sales)


# Prediction History page (NEW)
@app.route("/history")
def history():
    records = get_all_predictions()
    return render_template("history.html", records=records)


# Delete a single record (NEW)
@app.route("/history/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    delete_prediction(record_id)
    flash("Prediction record deleted.")
    return redirect(url_for("history"))


# Clear all history (NEW)
@app.route("/history/clear", methods=["POST"])
def clear_all():
    clear_history()
    flash("All prediction history cleared.")
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)