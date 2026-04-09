from django.contrib import admin
from .models import Poll, Option, Vote

# This allows you to add Options directly inside the Poll page
class OptionInline(admin.TabularInline):
    model = Option
    extra = 3  # Show 3 empty rows by default

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'start_time', 'end_time', 'is_secret', 'is_result_revealed')
    inlines = [OptionInline] # Add options while creating the poll

admin.site.register(Poll, PollAdmin)
admin.site.register(Option)
admin.site.register(Vote)
