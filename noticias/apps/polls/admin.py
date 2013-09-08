from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ('title','created_date','is_active')
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)

