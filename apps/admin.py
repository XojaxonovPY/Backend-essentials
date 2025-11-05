from django.contrib import admin

from apps.models import Videos, TestCase, BugReporter


# @admin.register(Videos)
# class VideosAdmin(admin.ModelAdmin):
#     pass


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'pre_conditions', 'test_data', 'steps', 'expected_result']


@admin.register(BugReporter)
class BugReporterAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'severity', 'priority', 'steps_to_reproduce', 'expected_result',
                    'actual_result', 'created_at', 'updated_at']
