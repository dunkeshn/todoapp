import django_filters
from django.db.models import Q

from core import models


class Tasks(django_filters.FilterSet):
    title = django_filters.CharFilter(label='Имя', lookup_expr='icontains')

    class Meta:
        model = models.Tasks
        fields = '__all__'
        exclude = ('completed', 'owners',)


class Users(django_filters.FilterSet):

    user_search = django_filters.CharFilter(method='user_filter', label='Имя или никнейм пользователя')

    def user_filter(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(username__icontains=value))


    class Meta:
        model = models.Users
        fields = ()
        exclude = ('picture', 'about',)