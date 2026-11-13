from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "learning_topics.csv")

# Ensure the CSV file exists before running to prevent crashes
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Could not find '{CSV_PATH}' in the application directory. Please make sure learning_topics.csv is in the same folder as app.py.")

df = pd.read_csv(CSV_PATH)
AVAILABLE_CAREERS = df["Career"].dropna().unique().tolist()

@app.route("/", methods=["GET", "POST"])
def home():
    careers = AVAILABLE_CAREERS
    result = []
    selected_career = ""
    current_skills = ""
    submitted = False

    if request.method == "POST":
        submitted = True
        selected_career = request.form.get("career", "")
        current_skills = request.form.get("skills", "")

        known = [s.strip().lower() for s in current_skills.split(",") if s.strip()]

        career_data = df[
            df["Career"].astype(str).str.strip().str.lower()
            == selected_career.strip().lower()
        ]

        missing = career_data[
            ~career_data["Skill Name"].astype(str).str.strip().str.lower().isin(known)
        ]

        result = missing["Skill Name"].dropna().tolist()

    return render_template(
        "index.html",
        careers=careers,
        result=result,
        selected_career=selected_career,
        current_skills=current_skills,
        submitted=submitted
    )


@app.route("/api/careers", methods=["GET"])
def get_careers():
    return jsonify({
        "careers": AVAILABLE_CAREERS,
        "total_careers": len(AVAILABLE_CAREERS)
    })


@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Please send valid JSON"}), 400

    career = data.get("career", "")
    skills = data.get("skills", "")

    if not isinstance(career, str) or not career.strip():
        return jsonify({"error": "Enter a valid career"}), 400

    if not isinstance(skills, str):
        return jsonify({"error": "Skills must be text"}), 400

    career_data = df[
        df["Career"].astype(str).str.strip().str.lower()
        == career.strip().lower()
    ]

    if career_data.empty:
        return jsonify({
            "error": "Career not found",
            "available_careers": AVAILABLE_CAREERS
        }), 404

    known = [s.strip().lower() for s in skills.split(",") if s.strip()]

    missing = career_data[
        ~career_data["Skill Name"].astype(str).str.strip().str.lower().isin(known)
    ]

    recommendations = missing["Skill Name"].dropna().tolist()

    return jsonify({
        "career": career,
        "known_skills": known,
        "recommended_skills": recommendations,
        "total_recommendations": len(recommendations),
        "message": "Recommendations generated successfully"
    })


@app.route("/api/test", methods=["GET"])
def test_api():
    return jsonify({"message": "LearnPath API is working!"})


if __name__ == "__main__":
    app.run(debug=True)