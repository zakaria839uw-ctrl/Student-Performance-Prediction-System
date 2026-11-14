
import sqlite3

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            semester TEXT,
            department TEXT,
            study_hours REAL,
            attendance REAL,
            previous_marks REAL,
            sleep_hours REAL,
            predicted_marks REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number TEXT NOT NULL,
            study_hours REAL,
            attendance REAL,
            previous_marks REAL,
            sleep_hours REAL,
            predicted_marks REAL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()

def add_student(name, roll_number, semester, department):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (name, roll_number, semester, department)
            VALUES (?, ?, ?, ?)
        """, (name, roll_number, semester, department))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def get_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return students

def save_prediction(roll_number, study_hours, attendance,
                    previous_marks, sleep_hours, predicted_marks):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prediction_history
        (roll_number, study_hours, attendance,
         previous_marks, sleep_hours, predicted_marks)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        roll_number, study_hours, attendance,
        previous_marks, sleep_hours, predicted_marks
    ))

    conn.commit()
    conn.close()

def save_prediction(roll_number, study_hours, attendance,
                    previous_marks, sleep_hours, predicted_marks):

    import sqlite3

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prediction_history
        (roll_number, study_hours, attendance,
         previous_marks, sleep_hours, predicted_marks)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        roll_number,
        study_hours,
        attendance,
        previous_marks,
        sleep_hours,
        predicted_marks
    ))

    conn.commit()
    conn.close()
