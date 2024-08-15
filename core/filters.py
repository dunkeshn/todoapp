import django_filters
from core import models

class Tasks(django_filters.FilterSet):
    title = django_filters.CharFilter(label='Имя', lookup_expr='icontains')

    class Meta:
        model = models.Tasks
        fields = '__all__'
        exclude = ('completed', 'owners', )
