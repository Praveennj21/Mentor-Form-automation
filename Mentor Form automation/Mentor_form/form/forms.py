from django import forms
from .models import StudentDetail, SubjectDetail, Marks, Student
from django.core.exceptions import ValidationError
from django import forms


class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentDetail
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sslc_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'high_school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'high_school_passing_year': forms.TextInput(attrs={'class': 'form-control'}),
            'puc_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'college_passing_year': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_enrollment': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SubjectDetailForm(forms.ModelForm):
    class Meta:
        model = SubjectDetail
        fields = ['sem', 'subject_name', 'subject_code', 'credits', 'schema']
        widgets = {
            'sem': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'schema': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['detail', 'usn', 'branch', 'schema']
        widgets = {
            'detail': forms.Select(attrs={'class': 'form-control'}),
            'usn': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'schema': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['sem', 'subject', 'ia_1', 'ia_2', 'ia_3', 'assignment_1', 'assignment_2', 'project_marks', 'external_marks']

    def clean(self):
        cleaned_data = super().clean()
        sem = cleaned_data.get('sem')
        subject = cleaned_data.get('subject')

        if subject and sem:
            if subject.sem != sem:
                raise ValidationError(f'The subject {subject.subject_name} does not belong to semester {sem}.')

        return cleaned_data

class SubjectFilterForm(forms.Form):
    sem = forms.IntegerField(label='Semester',required=True)
    schema = forms.CharField(label='Schema', required=True)
    
from django import forms

class ImportFileForm(forms.Form):
    file = forms.FileField()
    
from django import forms
from .models import Main

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = Main
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
