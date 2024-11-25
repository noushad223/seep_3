import sqlite3


def insert_coursework_data(student_uuid, module_id, coursework_id, coursework_content):

    try:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO Courseworks (student_uuid, module_id, coursework_id, coursework_content) VALUES (?, ?, ?, ?)""", (student_uuid, module_id, coursework_id, coursework_content))

        conn.commit()
        conn.close()

        print("Coursework data inserted succesfully")

    except sqlite3.Error as e:
        print(f"Couldn't insert coursework data: {e}")
