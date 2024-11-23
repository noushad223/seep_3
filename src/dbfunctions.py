import sqlite3

# Create a database connection
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# Permissions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Permissions (
    permission_id INTEGER PRIMARY KEY,
    role TEXT NOT NULL
);
""")

# Insert default permissions
cursor.executemany("""
INSERT OR IGNORE INTO Permissions (permission_id, role) VALUES (?, ?);
""", [
    (0, 'Student'),
    (1, 'Teacher'),
    (2, 'Module Leader')
])

# Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    uuid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    permission_id INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (permission_id) REFERENCES Permissions (permission_id)
);
""")

# Modules Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Modules (
    module_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name TEXT NOT NULL
);
""")

# Courseworks Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Courseworks (
    student_uuid TEXT NOT NULL,
    module_id INTEGER NOT NULL,
    coursework_id TEXT NOT NULL,
    coursework_marks REAL DEFAULT NULL,
    coursework_content TEXT NOT NULL,
    FOREIGN KEY (student_uuid) REFERENCES Students (uuid),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id),
    FOREIGN KEY (coursework_marks) REFERENCES TeacherCourseworks (teacher_marks)
);
""")

# Teachers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teachers (
    uuid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    permission_id INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (permission_id) REFERENCES Permissions (permission_id)
);
""")

# Teacher Coursework Marks Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TeacherCourseworks (
    teacher_uuid TEXT NOT NULL,
    coursework_id INTEGER NOT NULL,
    teacher_marks REAL DEFAULT NULL, 
    FOREIGN KEY (teacher_uuid) REFERENCES Teachers (uuid),
    FOREIGN KEY (coursework_id) REFERENCES Courseworks (coursework_id)
);
""")

# Module Leaders Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ModuleLeaders (
    uuid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    permission_id INTEGER NOT NULL DEFAULT 2,
    FOREIGN KEY (permission_id) REFERENCES Permissions (permission_id)
);
""")

# Module Leader Modules Relationship Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ModuleLeaderModules (
    leader_uuid TEXT NOT NULL,
    module_id INTEGER NOT NULL,
    FOREIGN KEY (leader_uuid) REFERENCES ModuleLeaders (uuid),
    FOREIGN KEY (module_id) REFERENCES Modules (module_id),
    PRIMARY KEY (leader_uuid, module_id)
);
""")

# Marking Scheme Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS MarkingSchemes (
    marking_scheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    marking_scheme_content TEXT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES Modules (module_id)
);
""")

# Autochecker Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Autochecker (
    coursework_id INTEGER NOT NULL,
    autochecker_marks REAL DEFAULT NULL,
    autochecker_comments TEXT NOT NULL,
    FOREIGN KEY (coursework_id) REFERENCES Courseworks (coursework_id),
    PRIMARY KEY (coursework_id)
);
""")

# Commit and close the database connection
conn.commit()
conn.close()

print("Database schema created successfully!")