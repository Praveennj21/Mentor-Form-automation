# urls.py
from django.urls import path
from form.views import register,login,hod_dashboard,pro_dashboard,logout_view,generate_pdf,student_dashboard,mentor_allocation_list,register_mentor,allot_mentor,index_view,hod_register_view,hod_login_view,professor_login_view,professor_register_view,student_login_view,student_register_view,new_subject_list,new_subject_marks,all_marks,import_marks_from_excel,export_student_marks_to_excel,import_students_from_excel,export_all_students_to_excel,export_student_detail_to_excel,export_marks_to_excel,filter_subjects_view,calculate_cgpa,calculate_sgpa_view,student_marks_view,display_marks_view,student_detail_form,enter_marks_view,student_list_view,add_student, student_detail_list_view,enter_marks_view, dashboard_view,student_detail_view,subject_list_view,subject_entry_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('student/', student_detail_form, name='student_detail_form'),
    path('students/', student_detail_list_view, name='student_detail_list'),
    path('student/<int:pk>/', student_detail_view, name='student_detail_display'),
    path('subject/entry/', subject_entry_view, name='subject_entry'),
    path('subjects/', subject_list_view, name='subject_list'),
    path('student/<int:student_id>/marks/', student_marks_view, name='student_marks'),
    path('add_student/', add_student, name='add_student'),
    path('student_list/', student_list_view, name='student_list'),
    path('enter_marks/<str:usn>/', enter_marks_view, name='enter_marks_view'),
    path('marks/', display_marks_view, name='display_marks'),
    path('calculate-sgpa/', calculate_sgpa_view, name='calculate_sgpa'),
    path('cgpa_results/', calculate_cgpa, name='cgpa_results'),
    path('filter_subjects/', filter_subjects_view,name='filter_subjects'),
    path('export-marks/', export_marks_to_excel, name='export_marks'),
    path('export-student/<int:student_id>/', export_student_detail_to_excel, name='export_student_to_excel'),
    path('export_students/', export_all_students_to_excel, name='export_all_students_to_excel'),
    path('import_students/', import_students_from_excel, name='import_students_from_excel'),
    path('export-student-marks/<int:student_id>/', export_student_marks_to_excel, name='export_student_marks'),
    path('import-marks/', import_marks_from_excel, name='import_marks'),
    path('marks/all/',all_marks, name='all_marks'),
    path('new_subject_list/',new_subject_list, name='new_subject_list'),
    path('new_subject_list/<str:subject_code>/marks/',new_subject_marks, name='new_subject_marks'),
    path('login/',student_login_view, name='student_login'),
    path('register/',student_register_view, name='student_register'),
    path('professor/login/', professor_login_view, name='professor_login'),
    path('professor/register/',professor_register_view, name='professor_register'),
    path('hod/login/', hod_login_view, name='hod_login'),
    path('hod/register/', hod_register_view, name='hod_register'),
    path('',index_view, name='index'),
    path('allot-mentor/',allot_mentor, name='allot_mentor'),
    path('register-mentor/',register_mentor, name='register_mentor'),
    path('mentor-allocation-list/',mentor_allocation_list, name='mentor_allocation_list'),
    path('student_dashboard/',student_dashboard, name='student_dashboard'),
    path('generate-pdf/<int:student_id>/', generate_pdf, name='generate_pdf'),
    path('logout_view/',logout_view, name='logout'),
    path('pro_dashboard/',pro_dashboard, name='pro'),
    path('hod_dashboard/',hod_dashboard, name='hod'),
     path('registeradmin/',register, name='register'),
    path('loginadmin/', login, name='login'),




]
