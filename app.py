
import streamlit as st
import pickle
import pandas as pd
import sqlite3
import os
import plotly.express as px
import plotly.graph_objects as go

from database import (
    create_database,
    add_student,
    get_students,
    save_prediction
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Student Performance Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. PROFESSIONAL CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #080f20, #101b35);
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #111b32;
    border-right: 1px solid #293958;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #e0e7ff !important;
}

p, label {
    color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #172554, #312e81);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #4338ca;
    box-shadow: 0 5px 18px rgba(0,0,0,0.2);
}

[data-testid="stMetricLabel"] {
    color: #c7d2fe !important;
}

[data-testid="stMetricValue"] {
    color: #a5b4fc !important;
    font-weight: 800;
}

[data-testid="stForm"] {
    background: #111c35;
    border: 1px solid #293958;
    padding: 22px;
    border-radius: 15px;
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: bold;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(90deg, #4338ca, #7e22ce);
    color: white;
    border: none;
}

[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 12px;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD MODEL AND DATABASE
# ==========================================

create_database()

if not os.path.exists("student_model.pkl"):
    st.error("student_model.pkl not found. Train your model first.")
    st.stop()

if not os.path.exists("model_metrics.pkl"):
    st.error("model_metrics.pkl not found. Run train_model.py first.")
    st.stop()

with open("student_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("model_metrics.pkl", "rb") as file:
    metrics = pickle.load(file)


# ==========================================
# 4. LOAD STUDENTS AND HISTORY
# ==========================================

students = get_students()

conn = sqlite3.connect("students.db")

try:
    history = pd.read_sql_query(
        """
        SELECT * FROM prediction_history
        ORDER BY id DESC
        """,
        conn
    )
finally:
    conn.close()


# ==========================================
# 5. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🎓 Student System")

    st.caption("Machine Learning Dashboard")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Student Registration",
            "Marks Prediction",
            "Student Records",
            "Analytics",
            "Student Report"
        ]
    )

    st.divider()

    st.markdown("### 👨‍💻 Developer")

    st.write("Muhammad Zakaria")

    st.caption("BSCS | Machine Learning Project")

    st.divider()

    st.caption("Version 2.0 | 2026")


# ==========================================
# 6. HEADER
# ==========================================

st.markdown("""
<div style="
background:linear-gradient(110deg,#172554,#312e81,#581c87);
padding:28px;
border-radius:18px;
border:1px solid #4f46e5;
margin-bottom:25px;
">
<h1>🎓 Student Performance Prediction System</h1>
<p>Machine Learning Based Student Analytics Dashboard</p>
<p><b>Developed by Muhammad Zakaria</b></p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. DASHBOARD
# ==========================================

if page == "Dashboard":

    st.header("📊 Dashboard Overview")

    total_students = len(students)
    total_predictions = len(history)

    average_marks = (
        history["predicted_marks"].mean()
        if not history.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", total_students)
    col2.metric("Total Predictions", total_predictions)
    col3.metric("Average Predicted Marks", f"{average_marks:.2f}")
    col4.metric("Model R² Score", f"{metrics['r2']:.2%}")

    st.divider()

    st.subheader("🧠 Machine Learning Evaluation")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("MAE", f"{metrics['mae']:.3f}")
    c2.metric("MSE", f"{metrics['mse']:.3f}")
    c3.metric("RMSE", f"{metrics['rmse']:.3f}")
    c4.metric("R² Score", f"{metrics['r2']:.2%}")

    st.caption(
        "Metrics are calculated on the model's test dataset."
    )

    st.divider()

    st.subheader("📋 Recent Student Predictions")

    if not history.empty:
        st.dataframe(
            history.head(10),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No prediction records available.")

    st.subheader("👨‍🎓 Registered Students")

    if students:

        student_data = []

        for s in students:
            student_data.append({
                "ID": s[0],
                "Name": s[1],
                "Roll Number": s[2],
                "Semester": s[3],
                "Department": s[4]
            })

        st.dataframe(
            pd.DataFrame(student_data),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Register your first student.")


# ==========================================
# 8. STUDENT REGISTRATION
# ==========================================

elif page == "Student Registration":

    st.header("👨‍🎓 Student Registration")

    st.write("Add a new student to the database.")

    with st.form("student_registration"):

        name = st.text_input("Student Name")

        roll_number = st.text_input("Roll Number")

        semester = st.selectbox(
            "Semester",
            [
                "1st", "2nd", "3rd", "4th",
                "5th", "6th", "7th", "8th"
            ]
        )

        department = st.text_input("Department")

        submit = st.form_submit_button("Register Student")

        if submit:

            if name.strip() and roll_number.strip():

                success = add_student(
                    name,
                    roll_number,
                    semester,
                    department
                )

                if success:
                    st.success("Student registered successfully!")
                    st.rerun()
                else:
                    st.error("Roll Number already exists.")

            else:
                st.warning("Please enter Name and Roll Number.")


# ==========================================
# 9. MARKS PREDICTION
# ==========================================

elif page == "Marks Prediction":

    st.header("🤖 Student Marks Prediction")

    if students:

        roll_numbers = [s[2] for s in students]

        selected_roll = st.selectbox(
            "Select Student",
            roll_numbers
        )

        study_hours = st.number_input(
            "Daily Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=5.0
        )

        attendance = st.slider(
            "Attendance (%)",
            0, 100, 85
        )

        previous_marks = st.number_input(
            "Previous Marks",
            min_value=0.0,
            max_value=100.0,
            value=70.0
        )

        sleep_hours = st.slider(
            "Sleep Hours",
            min_value=0.0,
            max_value=24.0,
            value=7.0
        )

        if st.button("🚀 Predict Student Marks"):

            input_data = pd.DataFrame([{
                "study_hours": study_hours,
                "attendance": attendance,
                "previous_marks": previous_marks,
                "sleep_hours": sleep_hours
            }])

            prediction = model.predict(input_data)[0]

            prediction = max(0, min(100, prediction))

            save_prediction(
                selected_roll,
                study_hours,
                attendance,
                previous_marks,
                sleep_hours,
                prediction
            )

            st.success(
                f"Predicted Marks: {prediction:.2f} / 100"
            )

            st.info(
                "This is an estimated result, not a guaranteed final mark."
            )

            st.rerun()

    else:
        st.warning("Register a student before prediction.")


# ==========================================
# 10. STUDENT RECORDS
# ==========================================

elif page == "Student Records":

    st.header("📋 Student Records")

    if students:

        student_data = []

        for s in students:
            student_data.append({
                "ID": s[0],
                "Name": s[1],
                "Roll Number": s[2],
                "Semester": s[3],
                "Department": s[4]
            })

        df = pd.DataFrame(student_data)

        search = st.text_input("🔍 Search by Roll Number")

        if search:
            df = df[
                df["Roll Number"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.metric("Total Registered Students", len(students))

    else:
        st.info("No student records found.")


# ==========================================
# 11. ANALYTICS AND REAL GRAPHS
# ==========================================

elif page == "Analytics":

    st.header("📈 Student Performance Analytics")

    if not history.empty:

        st.subheader("Average Predicted Marks by Student")

        average_marks = history.groupby(
            "roll_number",
            as_index=False
        )["predicted_marks"].mean()

        fig1 = px.bar(
            average_marks,
            x="roll_number",
            y="predicted_marks",
            color="predicted_marks",
            title="Average Predicted Marks",
            labels={
                "roll_number": "Student Roll Number",
                "predicted_marks": "Average Marks"
            },
            template="plotly_dark"
        )

        fig1.update_layout(
            paper_bgcolor="#111c35",
            plot_bgcolor="#111c35"
        )

        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        st.subheader("Prediction History Trend")

        trend = history.sort_values("id")

        fig2 = px.line(
            trend,
            x="id",
            y="predicted_marks",
            markers=True,
            title="Student Prediction History",
            labels={
                "id": "Prediction Number",
                "predicted_marks": "Predicted Marks"
            },
            template="plotly_dark"
        )

        fig2.update_layout(
            paper_bgcolor="#111c35",
            plot_bgcolor="#111c35"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        st.subheader("Study Hours vs Predicted Marks")

        if "study_hours" in history.columns:

            fig3 = px.scatter(
                history,
                x="study_hours",
                y="predicted_marks",
                color="roll_number",
                hover_data=["attendance", "previous_marks"],
                title="Study Hours and Predicted Marks",
                template="plotly_dark"
            )

            fig3.update_layout(
                paper_bgcolor="#111c35",
                plot_bgcolor="#111c35"
            )

            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("Make predictions to generate real analytics.")

    st.divider()

    st.subheader("Actual vs Predicted Marks")

    if os.path.exists("model_predictions.csv"):

        comparison = pd.read_csv("model_predictions.csv")

        if (
            "Actual Marks" in comparison.columns
            and "Predicted Marks" in comparison.columns
        ):

            fig4 = go.Figure()

            fig4.add_trace(
                go.Scatter(
                    x=list(range(1, len(comparison) + 1)),
                    y=comparison["Actual Marks"],
                    mode="lines+markers",
                    name="Actual Marks"
                )
            )

            fig4.add_trace(
                go.Scatter(
                    x=list(range(1, len(comparison) + 1)),
                    y=comparison["Predicted Marks"],
                    mode="lines+markers",
                    name="Predicted Marks"
                )
            )

            fig4.update_layout(
                title="Actual vs Predicted Marks",
                xaxis_title="Test Student",
                yaxis_title="Marks",
                template="plotly_dark",
                paper_bgcolor="#111c35",
                plot_bgcolor="#111c35"
            )

            st.plotly_chart(fig4, use_container_width=True)

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning("Comparison CSV columns do not match.")

    else:
        st.warning("model_predictions.csv not found.")


# ==========================================
# 12. INDIVIDUAL STUDENT REPORT
# ==========================================

elif page == "Student Report":

    st.header("🎓 Individual Student Performance Report")

    if not history.empty:

        student_list = history["roll_number"].unique()

        selected_student = st.selectbox(
            "Select Student",
            student_list
        )

        student_history = history[
            history["roll_number"] == selected_student
        ]

        total_predictions = len(student_history)

        average = student_history["predicted_marks"].mean()

        highest = student_history["predicted_marks"].max()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Predictions", total_predictions)

        col2.metric("Average Marks", f"{average:.2f}")

        col3.metric("Highest Marks", f"{highest:.2f}")

        st.divider()

        st.subheader("Student Prediction Records")

        st.dataframe(
            student_history,
            use_container_width=True,
            hide_index=True
        )

        fig5 = px.line(
            student_history.sort_values("id"),
            x="id",
            y="predicted_marks",
            markers=True,
            title="Individual Student Performance",
            template="plotly_dark"
        )

        fig5.update_layout(
            paper_bgcolor="#111c35",
            plot_bgcolor="#111c35"
        )

        st.plotly_chart(fig5, use_container_width=True)

    else:
        st.info("No prediction history available for reports.")


# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">
    <h3>Student Performance Prediction System</h3>
    <p>Developed by Muhammad Zakaria</p>
    <p>Machine Learning Based Academic Analytics</p>
</div>
""", unsafe_allow_html=True)
