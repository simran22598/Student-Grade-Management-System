import pymysql
import getpass

class GradeSystem:
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="root",  
            database="gradb"
        )
        self.cursor = self.db.cursor()
        self.student_name = ""
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_number INT UNIQUE,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                student_email VARCHAR(100),
                subject VARCHAR(100),
                grade VARCHAR(5),
                FOREIGN KEY (student_email) REFERENCES students(email)
            )
        """)
        self.db.commit()

    def admin_login(self):
        admin_user = input("Enter admin username: ")
        admin_pass = getpass.getpass("Enter admin password: ")
        if admin_user == "simran" and admin_pass == "simran123":
            print("----->| Welcome Admin |<-----")
            while True:
                print("\n1. Add Student\n2. Add/Update Grade\n3. View All Students\n4. Exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    self.register_student()
                elif choice == "2":
                    self.add_update_grade()
                elif choice == "3":
                    self.view_all_students()
                elif choice == "4":
                    break
                else:
                    print("Invalid choice.")
        else:
            print("Incorrect admin credentials.")

    def register_student(self):
        try:
            roll_number = int(input("Enter student roll number: "))
        except ValueError:
            print("Roll number must be a number.")
            return

        name = input("Enter student name: ")
        email = input("Enter email: ")
        if "@gmail.com" not in email:
            print("Invalid email format.")
            return

        self.cursor.execute("SELECT * FROM students WHERE email = %s OR roll_number = %s", (email, roll_number))
        if self.cursor.fetchone():
            print("Email or roll number already registered.")
            return


        password = getpass.getpass("Create password: ")
        self.cursor.execute(
            "INSERT INTO students (roll_number, name, email, password) VALUES (%s, %s, %s, %s)",
            (roll_number, name, email, password)
        )
        self.db.commit()
        print("Student registered successfully.")

    def student_login(self):
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        self.cursor.execute("SELECT name FROM students WHERE email = %s AND password = %s", (email, password))
        result = self.cursor.fetchone()
        if result:
            self.student_name = result[0]
            print(f"----->| Welcome {self.student_name} |<-----")
            self.view_grades(email)
        else:
            print("Invalid email or password.")

    def view_grades(self, email):
        self.cursor.execute("SELECT subject, grade FROM grades WHERE student_email = %s", (email,))
        grades = self.cursor.fetchall()
        if grades:
            print("Your Grades:")
            for subject, grade in grades:
                print(f"{subject}: {grade}")
        else:
            print("No grades available.")

    def add_update_grade(self):
        email = input("Enter student email: ")
        self.cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        if not self.cursor.fetchone():
            print("Student not found.")
            return
        subject = input("Enter subject name: ")
        grade = input("Enter grade: ")
        self.cursor.execute("SELECT * FROM grades WHERE student_email = %s AND subject = %s", (email, subject))
        if self.cursor.fetchone():
            self.cursor.execute("UPDATE grades SET grade = %s WHERE student_email = %s AND subject = %s",
                                (grade, email, subject))
        else:
            self.cursor.execute("INSERT INTO grades (student_email, subject, grade) VALUES (%s, %s, %s)",
                                (email, subject, grade))
        self.db.commit()
        print("Grade added/updated successfully.")

    def view_all_students(self):
        self.cursor.execute("SELECT roll_number, name, email FROM students")
        students = self.cursor.fetchall()
        if not students:
            print("No students found.")
            return
        for roll, name, email in students:
            print(f"\nRoll No: {roll} | Name: {name} | Email: {email}")
            self.cursor.execute("SELECT subject, grade FROM grades WHERE student_email = %s", (email,))
            grades = self.cursor.fetchall()
            if grades:
                for subject, grade in grades:
                    print(f"   {subject}: {grade}")
            else:
                print("   No grades available.")

    def home(self):
        print("\n----->| Student Grade Management System |<-----")
        while True:
            print("\n1. Admin Login\n2. Student Login\n3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.student_login()
            elif choice == "3":
                print("visit again")
                break
            else:
                print("Invalid choice. Try again.")

system = GradeSystem()
system.home()


