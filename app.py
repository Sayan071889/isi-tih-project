import streamlit as st
import numpy as np
import pandas as pd

# --------------------------------------
# 🧮 Mathematical MHS Model Functions
# --------------------------------------

def normalize_positive(x, min_val, max_val):
    """Positive contributor normalization: more = better."""
    return np.clip((x - min_val) / (max_val - min_val), 0, 1)

def normalize_negative(x, min_val, max_val):
    """Negative contributor normalization: more = worse."""
    return np.clip(1 - (x - min_val) / (max_val - min_val), 0, 1)

def normalize_sleep(x):
    """Piecewise normalization for sleep duration."""
    if x < 4 or x > 12:
        return 0
    elif 4 <= x < 7:
        return (x - 4) / 3
    elif 7 <= x <= 9:
        return 1
    elif 9 < x <= 12:
        return 1 - (x - 9) / 3

# Feature weights (sum = 1)
FEATURE_WEIGHTS = {
    "Sleep_Hours": 0.1,
    "Daily_Steps": 0.1,
    "Exercise_Frequency": 0.1,
    "Exercise_Duration": 0.1,
    "Diet_Quality": 0.1,
    "Social_Interaction": 0.1,
    "Happiness_Level": 0.1,
    "Screen_Time_Hours": 0.1,
    "Stress_Level": 0.1,
    "Anxiety_Level": 0.05,
    "Depression_Level": 0.05
}

# --------------------------------------
# 🧭 Streamlit App Layout
# --------------------------------------

st.set_page_config(page_title="MindBalance AI", page_icon="🧘", layout="centered")
st.title("🧘 MindBalance AI — Mental Health Score Calculator")
st.write("Estimate your **Mental Health Score (MHS)** using a mathematical model combining your daily habits, emotions, and lifestyle.")

# --------------------------------------
# 🧩 Input Section
# --------------------------------------

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    occupation = st.selectbox("Occupation", ["Student", "Working Professional", "Other"])
    sleep_hours = st.slider("Average Sleep Hours per night", 0.0, 12.0, 7.0)
    daily_steps = st.number_input("Average Daily Steps", min_value=0, max_value=30000, value=5000)
    diet_quality = st.slider("Diet Quality (1=Poor, 5=Excellent)", 1, 5, 3)
    social_interaction = st.slider("Meaningful Social Interactions per week", 0, 20, 5)

with col2:
    exercise_frequency = st.slider("Exercise Frequency (days/week)", 0, 7, 3)
    exercise_duration = st.number_input("Exercise Duration (minutes/session)", 0, 180, 45)
    exercise_type = st.selectbox("Exercise Type", ["Cardio", "Strength", "Yoga", "Other"])
    screen_time = st.slider("Daily Screen Time (non-work hours)", 0.0, 12.0, 4.0)
    stress_level = st.slider("Stress Level (1–10)", 1, 10, 5)
    anxiety_level = st.slider("Anxiety Level (1–10)", 1, 10, 5)
    depression_level = st.slider("Depression Level (1–10)", 1, 10, 5)
    happiness_level = st.slider("Happiness Level (1–10)", 1, 10, 7)

# --------------------------------------
# 📊 Compute Mental Health Score
# --------------------------------------

if st.button("🔮 Compute My Mental Health Score"):
    # Normalize inputs
    s_sleep = normalize_sleep(sleep_hours)
    s_steps = normalize_positive(daily_steps, 0, 30000)
    s_exfreq = normalize_positive(exercise_frequency, 0, 7)
    s_exdur = normalize_positive(exercise_duration, 0, 180)
    s_diet = normalize_positive(diet_quality, 1, 5)
    s_social = normalize_positive(social_interaction, 0, 20)
    s_happy = normalize_positive(happiness_level, 1, 10)
    s_screen = normalize_negative(screen_time, 0, 12)
    s_stress = normalize_negative(stress_level, 1, 10)
    s_anxiety = normalize_negative(anxiety_level, 1, 10)
    s_depression = normalize_negative(depression_level, 1, 10)

    # Weighted score
    score_norm = (
        s_sleep * FEATURE_WEIGHTS["Sleep_Hours"] +
        s_steps * FEATURE_WEIGHTS["Daily_Steps"] +
        s_exfreq * FEATURE_WEIGHTS["Exercise_Frequency"] +
        s_exdur * FEATURE_WEIGHTS["Exercise_Duration"] +
        s_diet * FEATURE_WEIGHTS["Diet_Quality"] +
        s_social * FEATURE_WEIGHTS["Social_Interaction"] +
        s_happy * FEATURE_WEIGHTS["Happiness_Level"] +
        s_screen * FEATURE_WEIGHTS["Screen_Time_Hours"] +
        s_stress * FEATURE_WEIGHTS["Stress_Level"] +
        s_anxiety * FEATURE_WEIGHTS["Anxiety_Level"] +
        s_depression * FEATURE_WEIGHTS["Depression_Level"]
    )

    mhs_score = 100 * score_norm

    # --------------------------------------
    # 🧠 Display Result
    # --------------------------------------
    st.markdown("---")
    st.subheader(f"🧩 Your Mental Health Score: **{mhs_score:.2f} / 100**")

    if mhs_score >= 75:
        st.success("🌿 Excellent mental well-being! Keep nurturing your balance of rest, work, and joy.")
        st.balloons()
    elif mhs_score >= 50:
        st.info("🙂 Fair well-being. A few lifestyle improvements can significantly lift your mood and energy.")
    else:
        st.warning("⚠️ Your score suggests stress or fatigue. Consider gradual lifestyle adjustments and mindfulness habits.")

    # --------------------------------------
    # 💡 Personalized Recommendations
    # --------------------------------------
    st.markdown("### 💡 Personalized Recommendations")
    recommendations = []

    # Sleep advice
    if sleep_hours < 7:
        recommendations.append("🌙 **Sleep:** Try to get 7–9 hours of sleep regularly to restore energy and focus.")
    elif sleep_hours > 9:
        recommendations.append("🛏️ **Sleep:** Oversleeping may affect alertness — aim for a consistent 7–9 hours.")

    # Screen time
    if screen_time > 5:
        recommendations.append("📵 **Screen Time:** Reduce non-essential screen time below 5 hours/day to ease anxiety.")

    # Exercise
    if exercise_frequency < 3:
        recommendations.append("🏃‍♂️ **Exercise:** Increase exercise frequency to at least 3–4 days per week.")
    elif exercise_duration < 30:
        recommendations.append("⏱️ **Exercise Duration:** Aim for 30–60 minutes per session for maximum benefit.")

    # Diet
    if diet_quality < 3:
        recommendations.append("🥗 **Diet:** Improve diet quality with whole foods, fruits, and lean proteins.")

    # Stress & Anxiety
    if stress_level > 6:
        recommendations.append("🧘‍♀️ **Stress:** Try meditation, yoga, or journaling to relax your mind.")
    if anxiety_level > 6:
        recommendations.append("💭 **Anxiety:** Practice deep-breathing or grounding exercises to stay calm.")
    if depression_level > 6:
        recommendations.append("💬 **Mood:** Engage in hobbies or connect with loved ones to improve mood.")

    # Social
    if social_interaction < 3:
        recommendations.append("🤝 **Social Life:** Regularly interact with friends or join community groups.")
    
    # Happiness
    if happiness_level < 5:
        recommendations.append("🌈 **Happiness:** Focus on gratitude, purpose, and activities that bring joy.")

    # Display personalized tips
    if recommendations:
        for tip in recommendations:
            st.markdown(f"- {tip}")
    else:
        st.success("🎉 Great job! Your lifestyle already supports good mental health. Keep it up!")
