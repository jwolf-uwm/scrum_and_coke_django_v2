"""scrum_and_coke_django_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from ta_assign.views import Index, Login, Logout, CreateAccount, AccessInfo, CreateCourse, EditAccount, EditInfo,\
    AssignInstructorToCourse, AssignTAToCourse, ViewCourseAssignments, CourseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index1'),
    path('index/', Index.as_view(), name='index1'),
    path('login/', Login.as_view(), name='Login1'),
    path('logout/', Logout.as_view(), name='Logout1'),
    path('create_account/', CreateAccount.as_view(), name='CreateAccount1'),
    path('create_course/', CreateCourse.as_view(), name='CreateCourse1'),
    path('access_info/', AccessInfo.as_view(), name='AccessInfo1'),
    path('edit_account/', EditAccount.as_view(), name='EditAccount1'),
    path('assign_ta/', AssignTAToCourse.as_view(), name='AssignTACourse1'),
    path('assign_instructor/', AssignInstructorToCourse.as_view(), name='AssignInstructor1'),
    path('view_course_assignments/', ViewCourseAssignments.as_view(), name='ViewCourseAssignments1'),
    path('edit_info/', EditInfo.as_view(), name='EditInfo1'),
    url(r'^course/(?P<coursename>\d+)/$', CourseView.as_view(), name='Course1'),
]
