from django.urls import path, include

from djangoTemplates.forumApp.views import index, dashboard, add_post, delete_post, details_page, edit_post, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-post/', add_post, name='add-post'),
    path('<int:pk>/', include([
        path('delete-post/', delete_post, name='delete-post'),
        path('details-post/', details_page, name='details-post'),
        path('edit-post/', edit_post, name='edit-post'),
    ]))
]