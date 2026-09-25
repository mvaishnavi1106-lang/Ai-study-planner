import random

def heuristic(subject, stress):
    return subject["difficulty"] * 2 + stress


def generate_plan(subjects, total_hours, stress):

    subjects_sorted = sorted(subjects, key=lambda x: heuristic(x, stress), reverse=True)

    plan = {}
    remaining = total_hours

    for sub in subjects_sorted:
        if remaining <= 0:
            break

        if sub["difficulty"] == 3:
            time_alloc = 3
        elif sub["difficulty"] == 2:
            time_alloc = 2
        else:
            time_alloc = 1

        # stress adjustment
        if stress >= 4:
            time_alloc -= 1
            if time_alloc < 1:
                time_alloc = 1

        plan[sub["name"]] = time_alloc
        remaining -= time_alloc

    return plan

def generate_ai_advice(plan, stress):
    time = sum(plan.values())

    if time >= 3:
        advice = "You have enough time. Focus on weak subjects."
    else:
        advice = "Limited time. Prioritize important topics."

    if stress >= 4:
        advice += " Take short breaks to reduce stress."

    return advice



def generate_motivation():
    quotes = [
        "Consistency beats intensity.",
        "Small progress is still progress.",
        "Focus today, succeed tomorrow.",
        "You are closer than you think."
    ]
    return random.choice(quotes)


def adjust_for_stress(plan, stress):
    if stress >= 4:
        plan["Break"] = "2 hrs + Relax"
    elif stress == 3:
        plan["Break"] = "1 hr"
    else:
        plan["Break"] = "30 mins"

    return plan