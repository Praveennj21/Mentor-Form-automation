from django.db import models

class Marks(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    sem = models.IntegerField(default=1)
    subject = models.ForeignKey('SubjectDetail', on_delete=models.CASCADE)
    ia_1 = models.IntegerField()
    ia_2 = models.IntegerField()
    ia_3 = models.IntegerField()
    average_ia = models.FloatField(blank=True, null=True)  # To be calculated
    assignment_1 = models.IntegerField()
    assignment_2 = models.IntegerField()
    project_marks = models.IntegerField()
    total_internal_marks = models.FloatField(blank=True, null=True)  # To be calculated
    external_marks = models.IntegerField()
    total_marks = models.FloatField(blank=True, null=True)  # To be calculated
    grade = models.CharField(max_length=2, blank=True, null=True)  # To be calculated
    grade_point = models.FloatField(blank=True, null=True)  # To be calculated

    def __str__(self):
        return f'{self.student} - {self.subject}'


class StudentDetail(models.Model):
        name = models.CharField(max_length=500)
        address = models.CharField(max_length=5000)
        phone_number = models.CharField(max_length=100)
        father_name = models.CharField(max_length=500)
        father_phone_number = models.CharField(max_length=500)
        sslc_marks = models.FloatField()
        high_school_name = models.CharField(max_length=500)
        high_school_passing_year = models.CharField(max_length=100)
        puc_marks = models.FloatField()
        college_name = models.CharField(max_length=500)
        college_passing_year = models.CharField(max_length=100)
        year_of_enrollment = models.IntegerField()
        year_of_passing = models.IntegerField()
    
        def __str__(self):
            return self.name 

class Mentor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Student(models.Model):
        detail = models.OneToOneField(StudentDetail, on_delete=models.CASCADE)
        usn = models.CharField(max_length=500)
        branch = models.CharField(max_length=200)
        schema = models.IntegerField()
        mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True)
    
        def __str__(self):
            return self.usn
    
class SubjectDetail(models.Model):
        subject_code = models.CharField(max_length=500, primary_key=True)  # Updated as primary key
        sem = models.IntegerField(default=1)
        subject_name = models.CharField(max_length=500)
        schema = models.IntegerField()
        credits = models.IntegerField()
        def __str__(self):
            return self.subject_name


class Mark(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    sem = models.IntegerField(default=1)
    subject = models.ForeignKey('SubjectDetail', on_delete=models.CASCADE)
    ia_1 = models.IntegerField()
    ia_2 = models.IntegerField()
    ia_3 = models.IntegerField()
    average_ia = models.FloatField(blank=True, null=True)  # To be calculated
    assignment_1 = models.IntegerField()
    assignment_2 = models.IntegerField()
    project_marks = models.IntegerField()
    total_internal_marks = models.FloatField(blank=True, null=True)  # To be calculated
    external_marks = models.IntegerField()
    total_marks = models.FloatField(blank=True, null=True)  # To be calculated
    grade = models.CharField(max_length=2, blank=True, null=True)  # To be calculated
    grade_point = models.FloatField(blank=True, null=True)  # To be calculated

    def __str__(self):
        return f'{self.student} - {self.subject}'

class studentLogin(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=100)

class professorLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class HODLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Main(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

