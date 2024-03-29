from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include
from django.views.generic import RedirectView

import base
from ToolOwnershipTracker.views import Profile, Login, PasswordReset, PasswordResetSent, PasswordResetForm, PasswordResetDone, SignUp, Jobsites, createJobsite, editJobsite, EditUser, createTool, UserToolboxes, viewToolbox, myToolbox, jobsiteToolboxes, jobsiteInventory, barCodeTest, process_image, process_image_to_tool, ScanToJobsiteToolbox, ScanToUserToolbox, fileToolReport, viewToolReports, toolReportDetails, allTools, editTool, logout, toolTrades

    

urlpatterns = [
    path('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('profile/', Profile.as_view()),
    path('password_reset/', PasswordReset.as_view(), name='password-reset'),
    path('password_reset_sent/', PasswordResetSent.as_view(),
         name='password_reset_sent'),
    path('password_reset_form/<str:token>/',
         PasswordResetForm.as_view(), name='password_reset_form'),
    path('password_reset_done/', PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('jobsites/', Jobsites.as_view(), name='jobsites'),
    path('createJobsite/', createJobsite.as_view(), name='createJobsite'),
    path('editJobsite/<int:jobsite_id>/', editJobsite.as_view(), name='editJobsite'),
    path('edituser/', EditUser.as_view(), name="edituser"),
    path('createTool/', createTool.as_view(), name="createTool"),
    path('userToolboxes/', UserToolboxes.as_view(), name='userToolboxes'),
    path('viewToolbox/<str:user_id>/', viewToolbox.as_view(), name='viewToolbox'),
    path('currentUserToolbox/', myToolbox.as_view(), name='myToolbox'),
    path('jobsiteToolboxes/', jobsiteToolboxes.as_view(), name='jobsiteToolboxes'),
    path('jobsiteInventory/<int:jobsite_id>', jobsiteInventory.as_view(), name='jobsiteInventory'),
    path('', Login.as_view(), name='login'),
    path('barcodeTest/', barCodeTest.as_view(), name="barcodeTest"),
    path('process_image/', process_image, name='process_image'),
    path('barcodeScanToUser/', ScanToUserToolbox.as_view(), name="scanUser"),
    path('barcodeScanToJobsite/', ScanToJobsiteToolbox.as_view(), name="scanJobsite"),
    path('process_image_to_tool/', process_image_to_tool, name='process_image'),
    path('fileToolReport/', fileToolReport.as_view(), name="fileToolReport"),
    path('viewToolReports/', viewToolReports.as_view(), name="viewToolReports"),
    path('toolReportDetails/<int:toolreport_id>', toolReportDetails.as_view(), name="toolReportDetails"),
    path('allTools/', allTools.as_view(), name='allTools'),
    path('editTool/<int:tool_id>', editTool.as_view(), name='editTool'),
    path('logout/', logout, name='logout'),
    path('toolTrades/', toolTrades.as_view(), name='toolTrades'),
]
