from django.contrib import admin

# from .models import Choice, Question

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['question_text']
#
#
# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ['question__question_text', 'choice_text']
#     list_select_related = ['question']  # Avoid extra queries using SQL Join
from .models import Machine, Collection, Warning, FaultCase, FaultNote, FaultNoteImage, FaultComment, MachineAssignment

admin.site.register(Machine)
admin.site.register(Collection)
admin.site.register(Warning)
admin.site.register(FaultCase)
admin.site.register(FaultNote)
admin.site.register(FaultNoteImage)
admin.site.register(FaultComment)
admin.site.register(MachineAssignment)