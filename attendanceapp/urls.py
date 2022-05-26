from django.urls import path
from .views import *

urlpatterns = [
   # path('login/', LoginView.as_view()),
    path('student/register/', Student_register.as_view()),
    path('professor/login/', professor_register.as_view()),
    path('student/list', StudentList.as_view()),
    path('student/attendance_activation', StudentAttendanceActivation.as_view()),
    path('student/dashboard', StudentDashboard.as_view()),
    path('student/verifyimage',VerifyImage.as_view()),
    path('student/attendancesheet',Attendancesheet.as_view()),
    path('Missingperson/report',Missingpersonregister.as_view()),
    path('foundperson/report',Foundpersonregister.as_view()),
    path('Missingperson/list',MissingpersonList.as_view()),
    path('Missing/person_details',Missingperson_details.as_view()),
    path('Foundperson/list',FoundpersonList.as_view()),
    path('Found/person_details',Foundpersondetails.as_view()),
    path('mycomplain/missing',Mymissincomplain.as_view()),
   path('mycomplain/found',Myfoundcomplain.as_view()),
   path('mycomplain/matchfoundedface',MatchesFoundface.as_view()),
   path('mycomplain/matchinfoundedface',MatchesINFoundfaces.as_view()),
   path('testing',Testing.as_view()),
   path('mycomplain/delete_missing_complain',Delete_Missing.as_view()),
   path('mycomplain/delete_found_complain',Delete_found.as_view()),
   # path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
   # path('giveid/', giveid.as_view()),
   
]