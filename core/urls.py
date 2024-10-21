from django.conf.urls.static import static
from django.urls import path

from project import settings
from project.settings import MEDIA_URL, MEDIA_ROOT
from .views import *
from rest_framework.routers import DefaultRouter
from core import views

urlpatterns = [
    path('', Welcome.as_view(), name='home'),
    path('tasks/', Tasks.as_view(), name='tasks'),
    path('calendar/', Calendar.as_view(), name='calendar'),
    path('pomodoro/', Pomodoro.as_view(), name='pomodoro'),
    path('search/', Search.as_view(), name='search'),
    path('add_task/', AddingTask.as_view(), name='add_task'),
    path('delete_task/<int:task_id>/', DeletingTask.as_view(), name='delete_task'),
    path('complete_task/<int:task_id>/', CompletingTask.as_view(), name='complete_task'),
    path('edit_task/<int:task_id>/', EditingTask.as_view(), name='edit_task'),
    path('update_task/<int:task_id>/', UpdatingTask.as_view(), name='update_task'),
    path('change_priority/<int:task_id>', ChangingPriority.as_view(), name='change_priority'),
    path('delete_task_search/<int:task_id>/', DeletingTaskSearch.as_view(), name='delete_task_search'),
    path('complete_task_search/<int:task_id>/', CompletingTaskSearch.as_view(), name='complete_task_search'),
    path('update_task_search/<int:task_id>/', UpdatingTaskSearch.as_view(), name='update_task_search'),
    path('change_priority_search/<int:task_id>', ChangingPrioritySearch.as_view(), name='change_priority_search'),
    path('login/', Login.as_view(), name='login'),
    path('registration/', Registration.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<int:user_id>', Profile.as_view(), name='profile'),
    path('find_friends/', FindingFriends.as_view(), name='find_friends'),
    path('friends/<int:user_id>', UserFriends.as_view(), name='user_friends'),
    path('add_friends/<int:user_id>', AddingFriends.as_view(), name='adding_friends'),
    path('invite_to_user/<int:user_id>', UserInvites.as_view(), name='user_invites'),
    path('accept_friend/<int:inviting_user_id>', AcceptingFriend.as_view(), name='accept_friend'),
    path('delete_friend/<int:deleting_user_id>', DeletingFriend.as_view(), name='delete_friend'),
    path('give_task/<int:task_id>/<int:friend_id>', GivingTask.as_view(), name='give_task'),
]

if settings.DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)