from django.contrib import admin
from django.urls import path
from app import views


app_name='app'

urlpatterns = [
            path('upload/',views.upload_view.as_view(),name='Upld'),
            path('release/',views.ReleaseListView.as_view(),name='release_list'),
            path('release/<release>/',views.ReleaseObjectListView.as_view(),name='release_objects'),
            path('release/<release>/Overview',views.rel_overview.as_view(),name='release_overview'),
            path('release/<release>/impplan',views.imp_plan.as_view(),name='imp_plan'),
            path('release/<release>/update_from_jira',views.update_release_items,name='upd_from_jira'),
            path('release/<release_plan>/impplan/pdf',views.render_pdf_view,name='imp_pdf'),
            path('release/<release>/pdf',views.render_pdf_view,name='pdf'),
            path('release/<release>/rel_notes',views.rel_notes_listview.as_view(),name='notes'),
            path('release/<release>/<pk>',views.ReleaseObjectDetailView.as_view(),name='object'),
            path('release/<release>/<pk>/update',views.wmobject_detail_update.as_view(),name='update'),
            path('release/<release>/<pk>/update_from_jira',views.update_item,name='update_from_jira'),
            path('release/<release>/<pk>/attach',views.wmobject_attach_update.as_view(),name='update_attach'),
            path('release/<release>/<pk>/relnot',views.rel_notes_view.as_view(),name='rel_notes'),
            path('test/',views.my_test_view,name='test'),
            path('auth/',views.test_view,name='auth'),
]