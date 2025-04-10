from django.db import models
from django.conf import settings # To reference the AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

# --- Choices ---

STATUS_CHOICES = [
    ('OK', 'OK'),
    ('Warning', 'Warning'),
    ('Fault', 'Fault'),
]

FAULT_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('Resolved', 'Resolved'),
]

ASSIGNMENT_ROLE_CHOICES = [
    ('Technician', 'Technician'),
    ('Repair', 'Repair'),
]

# --- Models ---

class Collection(models.Model):
    """
    User-definable collections for grouping machines (e.g., by location, type).
    Corresponds to the 'collections' table suggestion.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\-]+$',
                message='Collection name must contain only letters, numbers, or hyphens.'
            )
        ],
        help_text="Unique name for the collection (e.g., Building-A, Model-53A)."
    )
    description = models.TextField(blank=True, null=True, help_text="Optional description for the collection.")
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional: Add created_by ForeignKey to User if needed

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] # Default ordering


class Machine(models.Model):
    """
    Represents a piece of factory machinery.
    Corresponds to the 'machines' table.
    """
    machine_id = models.CharField(
        max_length=12, # Keep CHAR(12) as CharField for simplicity unless specific needs arise
        primary_key=True,
        help_text="Unique 12-character identifier for the machine."
    )
    name = models.CharField(max_length=100, help_text="Human-readable name of the machine.")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
        db_index=True, # Index for faster status lookups
        help_text="Current operational status of the machine."
    )
    importance_level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Importance level (1-5), used for prioritization."
    )
    collections = models.ManyToManyField(
        Collection,
        related_name='machines',
        blank=True, # A machine doesn't have to belong to a collection
        help_text="Collections this machine belongs to."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.machine_id})"

    class Meta:
        ordering = ['-importance_level', 'name'] # Order by importance first, then name


class Warning(models.Model):
    """
    Stores active or historical warnings associated with a machine.
    Corresponds to the 'warnings' table with added 'is_active' status.
    """
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE, # If machine is deleted, its warnings are too
        related_name='warnings'
    )
    warning_text = models.TextField(help_text="Description of the warning.")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Prevent deleting users who created warnings? Or SET_NULL?
        related_name='warnings_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        default=True,
        db_index=True, # Index for quickly finding active warnings
        help_text="Is this warning currently active?"
    )
    # Optional: Add 'resolved_by' and 'resolved_at' if needed for tracking who cleared it

    def __str__(self):
        return f"Warning for {self.machine.name} ({'Active' if self.is_active else 'Inactive'}) - {self.warning_text[:50]}..."

    class Meta:
        ordering = ['-created_at']


class FaultCase(models.Model):
    """
    Represents a specific fault or breakdown incident for a machine.
    Corresponds to the 'fault_cases' table.
    """
    # Django adds 'id' primary key automatically
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE, # If machine is deleted, its fault cases are too
        related_name='fault_cases'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Prevent deleting users who created cases?
        related_name='fault_cases_created'
    )
    status = models.CharField(
        max_length=10,
        choices=FAULT_STATUS_CHOICES,
        default='Open',
        db_index=True, # Index for finding open/resolved cases
        help_text="Current status of the fault case."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the fault case was marked as resolved."
    )

    def __str__(self):
        return f"Fault Case #{self.id} for {self.machine.name} ({self.status})"

    def resolve(self, user):
        """Marks the case as resolved."""
        self.status = 'Resolved'
        self.resolved_at = timezone.now()
        # Optionally link the resolving user
        # self.resolved_by = user
        self.machine.status = 'OK' # Return machine to OK status
        self.machine.save()
        self.save()

    class Meta:
        ordering = ['-created_at']

class FaultNote(models.Model):
    """
    Detailed notes or updates added to a fault case.
    Corresponds to the 'fault_notes' table.
    """
    fault_case = models.ForeignKey(
        FaultCase,
        on_delete=models.CASCADE, # Notes deleted with the case
        related_name='notes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Keep notes even if user is deleted? Or SET_NULL?
        related_name='fault_notes_added'
    )
    note_text = models.TextField(help_text="Content of the note.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note on Case #{self.fault_case.id} by {self.user.username} at {self.created_at}"

    class Meta:
        ordering = ['created_at'] # Show notes chronologically

class FaultNoteImage(models.Model):
    """
    Images associated with a specific fault note.
    Corresponds to 'fault_note_images', using ImageField.
    """
    fault_note = models.ForeignKey(
        'FaultNote',  # Use string 'FaultNote' if defined later in file, or import
        on_delete=models.CASCADE,
        related_name='images'
    )
    # Django will automatically handle filename conflicts if needed
    image = models.ImageField(
        upload_to='fault_images/%Y/%m/%d/',  # Organizes uploads by year/month/day
        # Or just: upload_to='fault_images/',
        help_text="Image file related to the fault note."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # self.image.name contains the path relative to MEDIA_ROOT
        return f"Image for Note ID {self.fault_note.id} ({self.image.name})"

    class Meta:
        ordering = ['uploaded_at']

class FaultComment(models.Model):
    """
    User comments on a fault case (simpler than full notes).
    Corresponds to 'fault_comments'.
    """
    fault_case = models.ForeignKey(
        FaultCase,
        on_delete=models.CASCADE, # Comments deleted with the case
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Keep comments? Or SET_NULL?
        related_name='fault_comments_made'
    )
    comment_text = models.TextField(help_text="The comment text.")
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on Case #{self.fault_case.id} by {self.user.username}"

    class Meta:
        ordering = ['commented_at'] # Show comments chronologically

class MachineAssignment(models.Model):
    """
    Assigns a Technician or Repair user to a specific machine.
    Corresponds to 'machine_assignments'.
    """
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # If user is deleted, remove their assignments
        related_name='machine_assignments',
        limit_choices_to={'groups__name__in': ['Technician', 'Repair']}
    )
    assigned_role = models.CharField(
        max_length=10,
        choices=ASSIGNMENT_ROLE_CHOICES,
        help_text="Role assigned to the user for this specific machine."
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep assignment record even if assigner is deleted
        null=True,
        blank=True,
        related_name='assignments_made'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} assigned as {self.assigned_role} to {self.machine.name}"

    class Meta:
        unique_together = ('machine', 'user') # Prevent assigning same user multiple times to same machine
        ordering = ['assigned_at']