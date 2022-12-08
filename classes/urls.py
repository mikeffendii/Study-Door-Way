from django.urls import path
from . import views


urlpatterns = [
	path('classes/create_class/',views.create_class_view,name='create_class'),
	path('classes/class_info/<int:id>/',views.class_info_view,name='class_info'),
	path('classes/s_class_info/<int:id>/',views.s_class_info_view,name='s_class_info'),

	path('classes/s_class_info/<int:class_id>/<int:assignment_id>/details',views.s_assignment_detail_view,name='s_assignment_detail'),
	path('classes/class_info/<int:class_id>/<int:assignment_id>/update_assignment',views.update_assignment_view,name='update_assignment'),
	path('classes/class_info/<int:class_id>/<int:assignment_id>/delete_assignment',views.delete_assignment_view,name='delete_assignment'),
	
	path('classes/class_info/<int:class_id>/<int:announcement_id>/update_announcement',views.announcement_update_view,name='update_announcement'),
	path('classes/like/<int:pk>/<int:class_id>',views.announcement_likes_view,name='announcement_likes'),
	path('classes/comment/<int:announcement_id>/<int:class_id>',views.announcement_comments_view,name='announcement_comments'),
	path('classes/class_info/<int:class_id>/<int:announcement_id>/delete_announcement',views.announcement_delete_view,name='delete_announcement'),
	
	path('classes/<int:class_id>/<int:assignment_id>/student_work',views.student_work_view,name='student_work'),
	path('classes/notification/<int:notification_id>/',views.delete_notification_view,name='delete_notification'),
	# path('classes/s_class_info/<int:id>/<int:assignment_id>',views.submit_assignment_view,name='submit_assignment'),
	path('classes/class_info/<int:class_id>/attendance',views.attendance_view,name='attendance'),
	path('classes/class_info/<int:class_id>/view_attendance',views.view_attendance,name='view_attendance'),
	path('classes/class_info/<int:class_id>/<int:att_id>/edit_attendance',views.edit_attendance,name='edit_attendance'),
	path('classes/class_info/<int:class_id>/export_attendance',views.export_attendance_xls,name='export_excel'),

	path('classes/class_info/<int:class_id>/<int:quiz_id>/add_question',views.add_question_view,name='add_question'),

	path('classes/class_info/<int:class_id>/<int:s_id>/print_pdf',views.render_pdf_view,name='print_pdf'),

	path('classes/class_info/<int:class_id>/<int:s_id>/final_marks',views.add_final_marks_view,name='final_marks'),
	
	path('classes/class_info/<int:class_id>/Rate',views.rate,name='rate'),

]