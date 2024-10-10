from django.shortcuts import render
from openpyxl import Workbook

# Create your views here.
# views.py
from django.shortcuts import render, redirect
from .forms import StudentDetailForm,SubjectDetailForm
from .models import StudentDetail,SubjectDetail,Student, Marks,Mark
from django.contrib import messages
from django.db.models import Sum, F

def student_detail_form(request):
    if request.method == "POST":
        form = StudentDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentDetailForm()
    return render(request, 'student_detail_form.html', {'form': form})

def student_detail_list_view(request):
    students = StudentDetail.objects.all()
    return render(request, 'student_detail_list.html', {'students': students})

def dashboard_view(request):
    return render(request, 'dashboard.html')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import StudentDetail

def student_detail_view(request, pk):
    # Get the student details or return a 404 error if not found
    student = get_object_or_404(StudentDetail, pk=pk)
    return render(request, 'student_detail_display.html', {'student': student})

def subject_entry_view(request):
    if request.method == 'POST':
        form = SubjectDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectDetailForm()
    return render(request, 'subject_entry.html', {'form': form})

def subject_list_view(request):
    subjects = SubjectDetail.objects.all().order_by('sem')
    semesters = {}
    for subject in subjects:
        if subject.sem not in semesters:
            semesters[subject.sem] = []
        semesters[subject.sem].append(subject)
    return render(request, 'subject_list.html', {'semesters': semesters})





from .models import Student
from .forms import StudentForm

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')  # Redirect to a page that lists students
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def student_list_view(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

from .forms import MarksForm
from .models import Marks

def enter_marks_view(request, usn):
    student = get_object_or_404(Student, usn=usn)
    
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student  # Associate the marks with the student

            # Check if marks for this student and subject already exist
            if Marks.objects.filter(student=student, subject=marks.subject).exists():
                messages.error(request, 'Marks for this student and subject have already been entered.')
                return redirect('enter_marks_view', usn=usn)
            
            # Calculate averages and total marks
            ia_average = (marks.ia_1 + marks.ia_2 + marks.ia_3) / 3
            assignment_average = (marks.assignment_1 + marks.assignment_2) / 2
            internal_marks = ia_average + assignment_average + marks.project_marks
            marks.total_internal_marks = internal_marks 
            total_marks = internal_marks + marks.external_marks
            marks.total_marks = total_marks

            # Assign grade and grade points based on total marks
            if total_marks >= 90:
                marks.grade = 'O'
                marks.grade_point = 10.0
            elif total_marks >= 80:
                marks.grade = 'E'
                marks.grade_point = 9.0
            elif total_marks >= 70:
                marks.grade = 'A'
                marks.grade_point = 8.0
            elif total_marks >= 60:
                marks.grade = 'B'
                marks.grade_point = 7.0
            elif total_marks >= 50:
                marks.grade = 'C'
                marks.grade_point = 6.0
            elif total_marks >= 40:
                marks.grade = 'D'
                marks.grade_point = 5.0
            else:
                marks.grade = 'F'
                marks.grade_point = 0.0

            marks.save()
            return redirect('student_list')  # Redirect to the marks list page or any other page
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        # Provide initial data for semester if needed (e.g., fetched from student or some logic)
        form = MarksForm()

    return render(request, 'student_marks_form.html', {'form': form})

def display_marks_view(request):
    marks = Marks.objects.all().order_by('sem', 'student__usn')
    
    marks_by_semester = {}
    for mark in marks:
        if mark.sem not in marks_by_semester:
            marks_by_semester[mark.sem] = []
        marks_by_semester[mark.sem].append(mark)
    
    return render(request, 'student_marks_display.html', {'marks_by_semester': marks_by_semester})

def student_marks_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Retrieve and organize marks by semester
    marks = Marks.objects.filter(student=student).select_related('subject').order_by('sem', 'subject__subject_code')
    marks_by_semester = {}
    
    for mark in marks:
        sem = mark.sem
        if sem not in marks_by_semester:
            marks_by_semester[sem] = []
        marks_by_semester[sem].append(mark)
    
    # Calculate SGPA for each semester
    sgpa_by_semester = {}
    
    for sem, marks_list in marks_by_semester.items():
        total_grade_points = 0
        total_credits = 0
        
        for mark in marks_list:
            subject = mark.subject
            credits = subject.credits
            
            # Calculate grade points for each mark
            if mark.total_marks >= 90:
                grade_point = 10.0
            elif mark.total_marks >= 80:
                grade_point = 9.0
            elif mark.total_marks >= 70:
                grade_point = 8.0
            elif mark.total_marks >= 60:
                grade_point = 7.0
            elif mark.total_marks >= 50:
                grade_point = 6.0
            elif mark.total_marks >= 40:
                grade_point = 5.0
            else:
                grade_point = 0.0
            
            # Accumulate grade points and credits
            total_grade_points += grade_point * credits
            total_credits += credits
        
        # Calculate SGPA for the semester
        sgpa = total_grade_points / total_credits if total_credits > 0 else 0
        sgpa_by_semester[sem] = sgpa
    
    # Render the template with the organized marks and SGPA
    context = {
        'student': student,
        'marks_by_semester': marks_by_semester,
        'sgpa_by_semester': sgpa_by_semester,
    }
    
    return render(request, 'student_marks.html', context)

def calculate_sgpa_view(request):
    # Dictionary to store SGPA results
    results = {}

    # Fetch all students
    students = Student.objects.all()

    for student in students:
        # Initialize a dictionary to store SGPA per semester for each student
        results[student.usn] = {}

        # Fetch all semesters that the student has marks for
        semesters = Marks.objects.filter(student=student).values_list('sem', flat=True).distinct()

        for sem in semesters:
            # Fetch all subjects for the current semester
            subjects = SubjectDetail.objects.filter(sem=sem)

            # Calculate total credits for the semester
            total_credits = subjects.aggregate(total_credits=Sum('credits'))['total_credits']

            # Fetch the student's marks for the current semester
            marks = Marks.objects.filter(student=student, sem=sem)

            # Calculate the total grade score
            total_grade_score = marks.annotate(
                weighted_score=F('grade_point') * F('subject__credits')
            ).aggregate(total_grade_score=Sum('weighted_score'))['total_grade_score']

            # Calculate SGPA for the semester
            sgpa = round(total_grade_score / total_credits, 2) if total_credits > 0 else 0

            # Store the SGPA in the results dictionary
            results[student.usn][sem] = sgpa

    # Render the results in a template
    return render(request, 'sgpa_results.html', {'results': results})

def calculate_cgpa(request):
    students = Student.objects.all()
    results = {}

    for student in students:
        # Retrieve marks for the student
        marks = Marks.objects.filter(student=student)

        total_grade_score = 0.0
        total_credits = 0
        
        for mark in marks:
            # Add the total grade points (grade_point) and credits (subject's credits) to the totals
            total_grade_score += mark.grade_point * mark.subject.credits
            total_credits += mark.subject.credits

        if total_credits > 0:
            cgpa = total_grade_score / total_credits
        else:
            cgpa = 0.0

        results[student.usn] = {
            'cgpa': round(cgpa, 2),  # Rounding to 2 decimal places
        }

    return render(request, 'cgpa_results.html', {'results': results})

from django.shortcuts import render
from .models import SubjectDetail
from .forms import SubjectFilterForm  # Replace with your actual form

def filter_subjects_view(request):
    subjects = None
    form = SubjectFilterForm(request.GET or None)  # Use GET method to handle form submissions

    if form.is_valid():
        sem = form.cleaned_data.get('sem')
        schema = form.cleaned_data.get('schema')
        
        # Retrieve subjects based on the selected semester and schema
        subjects = SubjectDetail.objects.filter(sem=sem, schema=schema)
    
    return render(request, 'filter_subjects.html', {'form': form, 'subjects': subjects})



import pandas as pd
from django.http import HttpResponse
from .models import Marks

def export_marks_to_excel(request):
    # Query all data from the Marks model with related fields from Student and SubjectDetail
    marks_data = Marks.objects.all().values(
        'student__usn',                          # USN of the student
        'student__branch',                       # Branch of the student
        'student__detail__name',                 # Name of the student
        'student__detail__phone_number',         # Phone number of the student
        'subject__subject_code',                 # Subject code
        'subject__subject_name',                 # Subject name
        'sem',                                   # Semester
        'ia_1',                                  # IA 1 marks
        'ia_2',                                  # IA 2 marks
        'ia_3',                                  # IA 3 marks
        'assignment_1',                          # Assignment 1 marks
        'assignment_2',                          # Assignment 2 marks
        'project_marks',                         # Project marks
        'total_internal_marks',                  # Total internal marks
        'external_marks',                        # External marks
        'total_marks',                           # Total marks
        'grade',                                 # Grade
        'grade_point',                           # Grade point
    )

    # Convert the data to a DataFrame
    df = pd.DataFrame(list(marks_data))

    # Create an HttpResponse object with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=marks.xlsx'

    # Use the ExcelWriter to write the DataFrame to the response as an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Marks')

    return response

def export_student_detail_to_excel(request, student_id):
    student = get_object_or_404(StudentDetail, id=student_id)
    
    # Create an Excel workbook and a sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Student Details"
    
    # Add headers
    headers = [
        "name", "address", "phone_number", "father_name",
        "father_phone_number", "sslc_marks", "high_school_name",
        "high_school_passing_year", "puc_marks", "college_name",
        "college_passing_year", "year_of_enrollment", "year_of_passing"
    ]
    ws.append(headers)
    
    # Add student data
    student_data = [
        student.name, student.address, student.phone_number,
        student.father_name, student.father_phone_number,
        student.sslc_marks, student.high_school_name,
        student.high_school_passing_year, student.puc_marks,
        student.college_name, student.college_passing_year,
        student.year_of_enrollment, student.year_of_passing
    ]
    ws.append(student_data)
    
    # Create response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={student.name}_details.xlsx'
    wb.save(response)
    return response


def export_all_students_to_excel(request):
    # Query all student details
    students = StudentDetail.objects.all()

    # Create a DataFrame from the student details
    df = pd.DataFrame(list(students.values()))

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_details.xlsx'

    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Student Details')

    return response


from .forms import ImportFileForm

def import_students_from_excel(request):
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file, engine='openpyxl')

            # Convert the DataFrame to a list of dictionaries and bulk create
            student_data = df.to_dict(orient='records')
            StudentDetail.objects.bulk_create([StudentDetail(**data) for data in student_data])
            
            return HttpResponse('Student details imported successfully!')
    else:
        form = ImportFileForm()

    return render(request, 'import_students.html', {'form': form})

def export_student_marks_to_excel(request, student_id):
    # Query Marks data for the specified student
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return HttpResponse("Student not found", status=404)

    marks_data = Marks.objects.filter(student=student)

    # Prepare data for export
    data = []
    for mark in marks_data:
        data.append({
            'Semester': mark.sem,
            'Subject': mark.subject.subject_name,
            'IA 1': mark.ia_1,
            'IA 2': mark.ia_2,
            'IA 3': mark.ia_3,
            'Average IA': mark.average_ia,
            'Assignment 1': mark.assignment_1,
            'Assignment 2': mark.assignment_2,
            'Project Marks': mark.project_marks,
            'Total Internal Marks': mark.total_internal_marks,
            'External Marks': mark.external_marks,
            'Total Marks': mark.total_marks,
            'Grade': mark.grade,
            'Grade Point': mark.grade_point,
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create a response object with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={student.usn}_marks.xlsx'

    # Use Pandas to write the DataFrame to the Excel file
    df.to_excel(response, index=False)

    return response


def import_marks_from_excel(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            df = pd.read_excel(file)

            for index, row in df.iterrows():
                usn = row['usn']
                student_name = row['student_name']
                subject_name = row['subject_name']

                # Find or create Student
                try:
                    student = Student.objects.get(usn=usn)
                except Student.DoesNotExist:
                    return HttpResponse(f"Student with USN {usn} not found", status=404)

                # Find SubjectDetail
                try:
                    subject = SubjectDetail.objects.get(subject_name=subject_name)
                except SubjectDetail.DoesNotExist:
                    return HttpResponse(f"Subject {subject_name} not found", status=404)

                # Create or update Mark record
                mark, created = Marks.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        'sem': row['sem'],
                        'ia_1': row['ia_1'],
                        'ia_2': row['ia_2'],
                        'ia_3': row['ia_3'],
                        'average_ia': row.get('average_ia', None),
                        'assignment_1': row['assignment_1'],
                        'assignment_2': row['assignment_2'],
                        'project_marks': row['project_marks'],
                        'total_internal_marks': row.get('total_internal_marks', None),
                        'external_marks': row['external_marks'],
                        'total_marks': row.get('total_marks', None),
                        'grade': row.get('grade', None),
                        'grade_point': row.get('grade_point', None)
                    }
                )

            return HttpResponse("Marks imported successfully!")

    return render(request, 'import_marks.html')

def all_marks(request):
    marks = Marks.objects.all()

    context = {
        'marks': marks,
    }
    return render(request, 'all_marks.html', context)

def new_subject_list(request):
    subjects = SubjectDetail.objects.all()
    return render(request, 'new_subject_list.html', {'subjects': subjects})

def new_subject_marks(request, subject_code):
    subject = get_object_or_404(SubjectDetail, subject_code=subject_code)
    marks = Marks.objects.filter(subject__subject_code=subject_code)
    return render(request, 'new_subject_marks.html', {'subject': subject, 'marks': marks})


from .models import studentLogin

def student_login_view(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        name = request.POST['name']

        try:
            student = studentLogin.objects.get(usn=usn, name=name)
            # Redirect to a success page or student's dashboard
            return redirect('student_dashboard')
        except studentLogin.DoesNotExist:
            # Invalid credentials, reload login page with an error
            return render(request, 'student_login.html', {'error': 'Invalid USN or Name'})

    return render(request, 'student_login.html')


def student_register_view(request):
    if request.method == 'POST':
        usn = request.POST['usn']
        name = request.POST['name']

        # Check if the student already exists
        if studentLogin.objects.filter(usn=usn).exists():
            # If the student already exists, reload registration page with an error
            return render(request, 'student_register.html', {'error': 'USN already registered'})

        # Create new student record
        student = studentLogin.objects.create(usn=usn, name=name)
        # Redirect to a success page or the login page
        return redirect('student_login')

    return render(request, 'student_register.html')


from .models import professorLogin,HODLogin

def professor_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            professor = professorLogin.objects.get(username=username, password=password)
            # Redirect to a success page or professor's dashboard
            return redirect('pro')
        except professorLogin.DoesNotExist:
            # Invalid credentials, reload login page with an error
            return render(request, 'professor_login.html', {'error': 'Invalid username or password'})

    return render(request, 'professor_login.html')

def professor_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the professor already exists
        if professorLogin.objects.filter(username=username).exists():
            # If the professor already exists, reload registration page with an error
            return render(request, 'professor_register.html', {'error': 'Username already taken'})

        # Create new professor record
        professor = professorLogin.objects.create(username=username, password=password)
        # Redirect to the login page
        return redirect('professor_login')

    return render(request, 'professor_register.html')

def hod_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            hod = HODLogin.objects.get(username=username, password=password)
            # Redirect to HOD dashboard or success page
            return redirect('hod')
        except HODLogin.DoesNotExist:
            # Invalid credentials, reload login page with an error
            return render(request, 'hod_login.html', {'error': 'Invalid username or password'})

    return render(request, 'hod_login.html')

def hod_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the HOD already exists
        if HODLogin.objects.filter(username=username).exists():
            # If the HOD already exists, reload registration page with an error
            return render(request, 'hod_register.html', {'error': 'Username already taken'})

        # Create new HOD record
        hod = HODLogin.objects.create(username=username, password=password)
        # Redirect to the login page
        return redirect('hod_login')

    return render(request, 'hod_register.html')

def index_view(request):
    return render(request,'index.html')


from .models import Mentor, Student

def allot_mentor(request):
    # Fetch mentors
    mentors = Mentor.objects.all()
    
    # Fetch students who do not have a mentor assigned yet
    students = Student.objects.filter(mentor__isnull=True)

    if request.method == 'POST':
        # Retrieve selected students and mentor from the form
        selected_students = request.POST.getlist('students')
        mentor_id = request.POST.get('mentor')

        mentor = Mentor.objects.get(id=mentor_id)

        # Assign selected students to the chosen mentor
        for student_id in selected_students:
            student = Student.objects.get(id=student_id)
            student.mentor = mentor
            student.save()

        return redirect('allot_mentor')  # Redirect to a success page or another view

    return render(request, 'allot_mentor.html', {'mentors': mentors, 'students': students})
def register_mentor(request):
    if request.method == 'POST':
        mentor_name = request.POST.get('mentor_name')
        if mentor_name:
            Mentor.objects.create(name=mentor_name)
            return redirect('register_mentor')  # Redirect to a success page or mentor list
    return render(request, 'register_mentor.html')


def mentor_allocation_list(request):
    # Fetch all mentors with their allotted students
    mentors = Mentor.objects.prefetch_related('student_set').all()

    return render(request, 'mentor_allocation_list.html', {'mentors': mentors})


def student_dashboard(request):
    return render(request,'student_dashboard.html')

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_pdf(request, student_id):
    student = Student.objects.get(id=student_id)
    marks_by_semester = {
        sem: Marks.objects.filter(student=student, subject__sem=sem)
        for sem in range(1, 9)  # Assuming 8 semesters
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.usn}_marks.pdf"'

    p = canvas.Canvas(response, pagesize=A4)  # Set to A4 size
    p.setTitle(f"Marks for {student.detail.name} ({student.usn})")
    
    # Title with double-line spacing
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"Marks for {student.detail.name}")
    p.drawString(100, 780, f"({student.usn})")
    
    y = 740  # Initial Y position after the title
    
    # Iterate through semesters and marks
    for sem, marks in marks_by_semester.items():
        if y < 100:  # Check if we need to create a new page
            p.showPage()
            y = 800
        
        # Semester Header
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, f"Semester {sem}")
        y -= 30  # Increased spacing
        
        # Table Headers with background
        p.setFont("Helvetica-Bold", 10)
        p.setFillColor(colors.lightgrey)
        p.rect(95, y - 5, 450, 15, fill=True, stroke=False)  # Adjusted width to fit A4
        p.setFillColor(colors.black)
        
        p.drawString(100, y, "Subject")
        p.drawString(180, y, "IA 1")
        p.drawString(220, y, "IA 2")
        p.drawString(260, y, "IA 3")
        p.drawString(300, y, "Assignment 1")
        p.drawString(360, y, "Assignment 2")
        p.drawString(420, y, "Project Marks")
        p.drawString(490, y, "Internal Marks")
        p.drawString(550, y, "External Marks")
        p.drawString(620, y, "Total Marks")
        p.drawString(680, y, "Grade")
        p.drawString(720, y, "Grade Points")
        y -= 20
        
        # Draw horizontal line below headers
        p.line(95, y + 10, 745, y + 10)  # Adjusted width to fit A4

        p.setFont("Helvetica", 10)
        for mark in marks:
            if y < 100:
                p.showPage()
                y = 800
            
            p.drawString(100, y, mark.subject.subject_name)
            p.drawString(180, y, str(mark.ia_1))
            p.drawString(220, y, str(mark.ia_2))
            p.drawString(260, y, str(mark.ia_3))
            p.drawString(300, y, str(mark.assignment_1))
            p.drawString(360, y, str(mark.assignment_2))
            p.drawString(420, y, str(mark.project_marks))
            p.drawString(490, y, f"{mark.total_internal_marks:.2f}")
            p.drawString(550, y, str(mark.external_marks))
            p.drawString(620, y, f"{mark.total_marks:.2f}")
            p.drawString(680, y, mark.grade)
            p.drawString(720, y, f"{mark.grade_point:.2f}")
            
            # Draw horizontal line after each row
            y -= 20
            p.line(95, y + 10, 745, y + 10)
        
        y -= 40  # Space between semesters
    
    p.showPage()
    p.save()
    return response

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return render(request,'index.html') 

def pro_dashboard(request):
    return render(request,'pro_dashboard.html')

def hod_dashboard(request):
    return render(request,'hod_dashboard.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import Main
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create a new Main object but do not save it yet
            user = form.save(commit=False)
            # Hash the password and save it
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = Main.objects.get(username=username)
                if check_password(password, user.password):
                    # Successfully authenticated
                    return redirect('dashboard')  # Redirect to the desired page after login
                else:
                    form.add_error(None, 'Invalid username or password')
            except Main.DoesNotExist:
                form.add_error(None, 'Invalid username or password')
    else:
        form = RegistrationForm()
    return render(request, 'login.html', {'form': form})