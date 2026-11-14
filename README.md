<div align="center">

# 🎓 Student Performance Prediction System

### A Machine Learning dashboard that predicts a student's final marks and turns the results into clear analytics.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Linear%20Regression-F7931E?logo=scikitlearn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)

</div>

---

## 📌 Overview

Many students do not know how their daily habits affect their final result. Teachers also need a simple way to spot students who may need help **before** the exam.

**Student Performance Prediction System** solves this. It uses a Machine Learning model to estimate a student's final marks from four simple inputs, and it saves every prediction so progress can be tracked over time.

The project is a complete, working system, not only a model. It includes:

- a trained ML model,
- a database for students and prediction history,
- and a modern, dark-themed web dashboard.

---

## ✨ Key Features

| Feature | What it does |
|---|---|
| 🤖 **Marks Prediction** | Predicts final marks (0–100) from study hours, attendance, previous marks and sleep hours. |
| 👨‍🎓 **Student Registration** | Registers students with name, roll number, semester and department. Duplicate roll numbers are blocked. |
| 🗂️ **Prediction History** | Every prediction is saved to a SQLite database with date and time. |
| 📊 **Dashboard** | Shows total students, total predictions, average predicted marks and model quality at a glance. |
| 📈 **Analytics** | Interactive Plotly charts: average marks per student, prediction trend, study hours vs marks, and actual vs predicted marks. |
| 🎓 **Individual Report** | A personal report for each student with average marks, highest marks and a performance line chart. |
| 🔍 **Search** | Find any student quickly by roll number. |
| 🧠 **Model Evaluation** | MAE, MSE, RMSE and R² score are shown inside the app. |

---

## 🧠 How It Works

```
 student_data.csv
        │
        ▼
 train_model.py ──► Linear Regression model ──► student_model.pkl
        │                                       model_metrics.pkl
        ▼
   app.py (Streamlit) ◄──► database.py (SQLite: students.db)
        │
        ▼
 Dashboard • Prediction • Analytics • Reports
```

**Input features**

| Feature | Meaning |
|---|---|
| `study_hours` | Daily study hours |
| `attendance` | Attendance percentage |
| `previous_marks` | Marks in the previous exam |
| `sleep_hours` | Average daily sleep hours |

**Output:** `final_marks` (predicted score out of 100)

**Model:** Linear Regression (scikit-learn), trained with an 80/20 train-test split.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Machine Learning:** scikit-learn, pandas, NumPy
- **Web App:** Streamlit
- **Charts:** Plotly
- **Database:** SQLite
- **Model storage:** Pickle

---

## 📁 Project Structure

```
Student-Performance-Prediction-System/
│
├── app.py               # Streamlit dashboard (main application)
├── database.py          # SQLite database and helper functions
├── train_model.py       # Trains and evaluates the ML model
├── student_data.csv     # Training dataset
├── student_model.pkl    # Trained model
├── model_metrics.pkl    # Saved evaluation metrics
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/zakaria839uw-ctrl/Student-Performance-Prediction-System.git
cd Student-Performance-Prediction-System
```

### 2. Install the requirements

```bash
pip install -r requirements.txt
```

### 3. Train the model (recommended)

```bash
python train_model.py
```

This creates `student_model.pkl`, `model_metrics.pkl` and `model_predictions.csv`. The last file is used by the **Actual vs Predicted** chart in the Analytics page.

### 4. Run the app

```bash
streamlit run app.py
```

Open the link shown in the terminal (usually `http://localhost:8501`).

---

## 🖥️ How to Use

1. Open **Student Registration** and add a student.
2. Open **Marks Prediction**, select the student, enter the four values and click **Predict**.
3. Open **Dashboard** and **Analytics** to see charts and summaries.
4. Open **Student Report** to see one student's full performance.

---

## 📊 Model Performance

Results on the test split:

| Metric | Value |
|---|---|
| MAE | 0.41 |
| RMSE | 0.53 |
| R² Score | 99.8% |

> ⚠️ **Honest note:** The current dataset is small (13 records), so these scores are very high and should be seen as a **proof of concept**. They do not guarantee the same accuracy on real, larger data. The system is built so that a larger dataset can be dropped into `student_data.csv` and the model retrained with one command.

---

## 🔮 Future Improvements

- Train on a larger, real-world student dataset.
- Compare more models (Random Forest, Gradient Boosting) and pick the best one.
- Add more features (assignments, quizzes, health, family support).
- Early-warning alerts for students at risk of failing.
- Export student reports as PDF.
- Login system for teachers and admins.
- Deploy online with Streamlit Community Cloud.

---

## 👨‍💻 Developer

**Muhammad Zakaria**
BS Computer Science Student

GitHub: [@zakaria839uw-ctrl](https://github.com/zakaria839uw-ctrl)

---

<div align="center">

⭐ If you like this project, please give it a star!

</div>
