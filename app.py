from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import random

app = Flask(__name__)

# 🧠 Sort subjects
def a_star_planner(subjects):
    return sorted(subjects, key=lambda x: x['difficulty'], reverse=True)

# 📊 Graph
def generate_graph(ai, dbms, maths, sml, daa):
    subjects = ['AI', 'DBMS', 'Maths', 'SML', 'DAA']
    values = [ai, dbms, maths, sml, daa]

    if not os.path.exists('static'):
        os.makedirs('static')

    plt.figure(figsize=(4,2))
    plt.bar(subjects, values)
    plt.title("Difficulty Analysis")
    plt.savefig("static/graph.png")
    plt.close()

# 🤖 Prediction
def predict_score(ai, dbms, maths, sml, daa, hours, stress):
    score = 100 - (ai + dbms + maths + sml + daa)*4 + hours*2 - stress*3
    return max(40, min(score, 100))

# 🔥 Motivation
def get_motivation():
    return random.choice([
        "Stay consistent 💪",
        "You got this 🚀",
        "Focus = Success 🎯"
        "Study now, shine later"
        "Small steps every day"
        "Focus beats talent."
        "No pain, no gain."
        "Dream big, work hard"
        "Push yourself daily"
        "Success needs effort"
        "Stay consistent."
        "Do it now."
        "Your future is watching"
        "Discipline = Freedom."
        "Make it happen."
        "One chapter at a time."
        "Don’t quit"
        "Hard work wins."
    ])

@app.route('/')
def home():
    return render_template('index.html')

# 🚀 PLAN
@app.route('/plan', methods=['POST'])
def plan():

    # 🎯 INPUTS
    ai = int(request.form['ai'])
    dbms = int(request.form['dbms'])
    maths = int(request.form['maths'])
    sml = int(request.form['sml'])
    daa = int(request.form['daa'])
    hours = int(request.form['hours'])
    stress = int(request.form['stress'])
    days = int(request.form['days'])

    subjects = [
        {"name": "AI", "difficulty": ai},
        {"name": "DBMS", "difficulty": dbms},
        {"name": "Maths", "difficulty": maths},
        {"name": "SML", "difficulty": sml},
        {"name": "DAA", "difficulty": daa}
    ]

    ordered = a_star_planner(subjects)

    generate_graph(ai, dbms, maths, sml, daa)
    predicted_score = predict_score(ai, dbms, maths, sml, daa, hours, stress)

    # 🔥 PLAN (SIMPLIFIED)
    study_plan = {}
    num_subjects = len(ordered)

    for day in range(1, days + 1):

        day_plan = []
        remaining_hours = hours

        num_today = 2 if day % 3 == 0 else 3

        todays_subjects = []
        for i in range(num_today):
            index = (day * 2 + i) % num_subjects
            todays_subjects.append(ordered[index])

        total_diff = sum(s['difficulty'] for s in todays_subjects)

        for i, sub in enumerate(todays_subjects):

            if i == len(todays_subjects) - 1:
                sub_hours = remaining_hours
            else:
                sub_hours = round((sub['difficulty'] / total_diff) * hours)
                sub_hours = max(1, sub_hours)
                remaining_hours -= sub_hours

            sessions = sub_hours * 2

            day_plan.append(f"{sub['name']} → {sessions} sessions ({sub_hours} hrs)")

        break_time = "45 mins" if stress >= 4 else "15 mins" if stress <= 2 else "30 mins"

        study_plan[f"Day {day}"] = " | ".join(day_plan) + f" | Break: {break_time}"

    return render_template(
        'index.html',
        plan=study_plan,
        motivation=get_motivation(),
        predicted_score=predicted_score
    )

if __name__ == '__main__':
    app.run(debug=True)