
import pandas as pd

df = pd.read_csv("learning_topics.csv")

print("Available Careers:")
print(df["Career"].unique().tolist())

career = input("Enter your career goal: ").strip().lower()
skills = input("Enter your skills (comma separated): ").lower()
known_skills = [s.strip().lower() for s in skills.split(",") if s.strip()]
hours = int(input("Study hours per day: "))
days = int(input("Target days: "))

data = df[df["Career"].str.lower() == career]

if data.empty:
    print("Career not found!")
else:
    missing = data[
        ~data["Skill Name"].str.lower().isin(known_skills)
    ]

    print("\nRecommended Skills:")
    total = 0

    for skill in missing["Skill Name"]:
        print("-", skill)

    total = missing["Estimated Hours"].sum()
    available = hours * days

    print("\nRequired Hours:", total)
    print("Available Hours:", available)

    if total <= available:
        print("Status: Feasible")
    else:

        print("Status: More time needed")
