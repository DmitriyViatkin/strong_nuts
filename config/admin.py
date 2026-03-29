from django.contrib import admin
from django_celery_results.models import TaskResult, GroupResult
from django_celery_results.admin import TaskResultAdmin, GroupResultAdmin
from unfold.admin import ModelAdmin

# Сначала отменяем стандартную регистрацию
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)

# Затем регистрируем заново, но с использованием Unfold
@admin.register(TaskResult)
class UnfoldTaskResultAdmin(TaskResultAdmin, ModelAdmin):
    pass

@admin.register(GroupResult)
class UnfoldGroupResultAdmin(GroupResultAdmin, ModelAdmin):
    pass