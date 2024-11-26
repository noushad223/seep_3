import sqlite3
from pdfscanner import extract_text_from_pdf

def db_conn():
    # Open and return a connection to the database
    return sqlite3.connect("university.db")

def insert_coursework_data(student_uuid, module_id, coursework_id, pdf_path): 
    # Use the database connection and cursor
    connection = db_conn()  # Get the connection
    coursework_content = extract_text_from_pdf(pdf_path) # Get the coursework content via pdf file name
    try:
        cursor = connection.cursor()  # Get a cursor from the connection
        query = """
        INSERT INTO Courseworks (student_uuid, module_id, coursework_id, coursework_content) 
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (student_uuid, module_id, coursework_id, coursework_content))
        connection.commit()  # Commit changes to save the data
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()  # Ensure connection is closed

# Fetch all coursework IDs where marks are NULL
def get_all_courseworks_ids():
    connection = db_conn()
    try:
        cursor = connection.cursor()
        query = """
        SELECT coursework_id FROM Courseworks WHERE coursework_marks IS NULL;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[0] for row in results]  # Extract coursework IDs from results
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        connection.close()  # Ensure connection is closed

# Fetch coursework content for processing
def get_coursework(coursework_id):
    connection = db_conn()
    try:
        cursor = connection.cursor()
        query = """
        SELECT student_uuid, module_id, coursework_id, coursework_content 
        FROM Courseworks 
        WHERE coursework_id = ?;
        """
        cursor.execute(query, (coursework_id,))
        result = cursor.fetchone()
        if result:
            student_uuid, module_id, coursework_id, coursework_content = result
            return {
                "student_uuid": student_uuid,
                "module_id": module_id,
                "coursework_id": coursework_id,
                "coursework_content": coursework_content,
            }
        return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        connection.close()  # Ensure connection is closed

# Fetch marking scheme content for processing
def get_marking_scheme(marking_scheme_id):
    connection = db_conn()
    try:
        cursor = connection.cursor()
        query = """
        SELECT marking_scheme_id, module_id, marking_scheme_content 
        FROM MarkingSchemes
        WHERE marking_scheme_id = ?;
        """
        cursor.execute(query, (marking_scheme_id,))
        result = cursor.fetchone()
        if result:
            marking_scheme_id, module_id, marking_scheme_content = result
            return {
                "marking_scheme_id": marking_scheme_id,
                "module_id": module_id,
                "marking_scheme_content": marking_scheme_content,
            }
        return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        connection.close()  # Ensure connection is closed

# Update coursework marks
def update_coursework_marks(coursework_id, final_marks, final_comments):
    connection = db_conn()
    try:
        cursor = connection.cursor()
        query = """
        UPDATE Autochecker
        SET 
            autochecker_marks = ?,
            autochecker_comments = ? 
        WHERE 
            coursework_id = ?;
        """
        cursor.execute(query, (final_marks, final_comments, coursework_id))
        connection.commit()  # Commit changes to persist the update
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()  # Ensure connection is closed