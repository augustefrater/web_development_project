from django.contrib import admin
from .models import (
    Collection,
    Machine,
    Warning,
    FaultCase,
    FaultNote,
    FaultNoteImage,
    FaultComment,
    MachineAssignment
)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['question_text']
#
#
# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ['question__question_text', 'choice_text']
#     list_select_related = ['question']  # Avoid extra queries using SQL Join

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_id', 'name', 'status', 'importance_level', 'created_at')
    search_fields = ('name', 'machine_id')
    list_filter = ('status', 'importance_level')
    ordering = ('-importance_level', 'name')

@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ('machine', 'warning_text', 'is_active', 'created_by', 'created_at')
    search_fields = ('warning_text', 'machine__name')
    list_filter = ('is_active', 'created_by')
    ordering = ('-created_at',)

@admin.register(FaultCase)
class FaultCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'status', 'created_by', 'created_at', 'resolved_at')
    list_filter = ('status',)
    search_fields = ('machine__name', 'created_by__username')
    ordering = ('-created_at',)

@admin.register(FaultNote)
class FaultNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'fault_case', 'user', 'created_at', 'note_text')
    search_fields = ('note_text', 'user__username')
    ordering = ('created_at',)

@admin.register(FaultNoteImage)
class FaultNoteImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'fault_note', 'image', 'uploaded_at')
    ordering = ('uploaded_at',)

@admin.register(FaultComment)
class FaultCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fault_case', 'user', 'commented_at')
    search_fields = ('comment_text', 'user__username')
    ordering = ('commented_at',)

@admin.register(MachineAssignment)
class MachineAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'user', 'assigned_role', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_role',)
    search_fields = ('user__username', 'machine__name', 'assigned_by__username')
    ordering = ('assigned_at',)