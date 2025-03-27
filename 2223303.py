import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host='localhost',  
    user='root',  
    password='admin@123',  
    database='bajaj'  
)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    student_id INT,
    attendance_date DATE,
    status VARCHAR(10)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INT,
    student_name VARCHAR(100),
    parent_email VARCHAR(100)
);
''')

attendance_data = [
    (101, '2024-03-01', 'Absent'),
    (101, '2024-03-02', 'Absent'),
    (101, '2024-03-03', 'Absent'),
    (101, '2024-03-04', 'Absent'),
    (101, '2024-03-05', 'Present'),
    (102, '2024-03-02', 'Absent'),
    (102, '2024-03-03', 'Absent'),
    (102, '2024-03-04', 'Absent'),
    (102, '2024-03-05', 'Absent'),
    (103, '2024-03-05', 'Absent'),
    (103, '2024-03-06', 'Absent'),
    (103, '2024-03-07', 'Absent'),
    (103, '2024-03-08', 'Absent'),
    (103, '2024-03-09', 'Absent'),
    (104, '2024-03-01', 'Present'),
    (104, '2024-03-02', 'Present'),
    (104, '2024-03-03', 'Absent'),
    (104, '2024-03-04', 'Present'),
    (104, '2024-03-05', 'Present')
]

students_data = [
    (101, 'Alice Johnson', 'alice_parent@example.com'),
    (102, 'Bob Smith', 'bob_parent@example.com'),
    (103, 'Charlie Brown', 'invalid_email.com'),
    (104, 'David Lee', 'invalid_email.com'),
    (105, 'Eva White', 'eva_white@example.com'),
]

cursor.executemany('INSERT INTO attendance (student_id, attendance_date, status) VALUES (%s, %s, %s)', attendance_data)
cursor.executemany('INSERT INTO students (student_id, student_name, parent_email) VALUES (%s, %s, %s)', students_data)
conn.commit()

def find_absent_students():
    cursor.execute('''
    SELECT student_id, COUNT(*) AS total_absent_days
    FROM attendance
    WHERE status = 'Absent'
    GROUP BY student_id
    HAVING total_absent_days > 3;
    ''')
    return cursor.fetchall()  

def validate_emails(absence_data):
    s = []
    
    for student_id, total_absent_days in absence_data:
        cursor.execute(f'''
        SELECT parent_email, student_name
        FROM students
        WHERE student_id = {student_id};
        ''')
        student_info = cursor.fetchone()  
        
        if student_info:
            parent_email, student_name = student_info
            
            if '@' in parent_email and '.' in parent_email:
                 = f'Dear Parent, your child {student_name} was absent for {total_absent_days} days. Please ensure their attendance improves.'
                s.append((student_id, ))
    
    return s

def run():
    path = r'C:\Users\Admin\Desktop\test\data - sample.xlsx'  
    df = pd.read_excel(path)
    return df

conn.close()
