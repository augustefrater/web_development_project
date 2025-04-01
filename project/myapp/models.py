from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class User(models.Model):
    # Unique user ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Login username, unique and required
    username = models.CharField(max_length=50, unique=True, null=False)

    # Hashed password, required
    password_hash = models.CharField(max_length=255, null=False)

    # User role enum, required
    ROLE_CHOICES = (
    ('Technician', 'Technician'), ('Repair', 'Repair'), ('Manager', 'Manager'), ('ViewOnly', 'ViewOnly'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)

    # Registration timestamp, auto-set to current time
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username



class Machine(models.Model):
    # Machine ID, fixed 12-character primary key
    machine_id = models.CharField(max_length=12, primary_key=True)

    # Machine name, max 100 characters
    name = models.CharField(max_length=100)

    # Machine status enum with default 'OK'
    STATUS_CHOICES = (('OK', 'OK'), ('Warning', 'Warning'), ('Fault', 'Fault'))
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='OK')

    # Importance level between 1-5, default is 1
    importance_level = models.IntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])

    # Creation timestamp, auto-set to current time
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'machines'

    def __str__(self):
        return f'{self.name} ({self.machine_id})'



class Warning(models.Model):
    # Unique warning ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Related machine, foreign key to machines table
    machine_id = models.ForeignKey('Machine', on_delete=models.CASCADE, to_field='machine_id', null=False)

    # Warning description, required
    warning_text = models.TextField(null=False)

    # User who added the warning, foreign key to users table
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id', null=False)

    # Timestamp, auto-set to current time
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'warnings'

    def __str__(self):
        return f"Warning {self.id} for {self.machine_id}"



class FaultCase(models.Model):
    # Unique fault case ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Faulty machine, foreign key to machines table
    machine_id = models.ForeignKey('Machine', on_delete=models.CASCADE, to_field='machine_id', null=False)

    # Who created the case, foreign key to users table
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id', null=False)

    # Case status enum with default 'Open'
    STATUS_CHOICES = (('Open', 'Open'), ('Resolved', 'Resolved'))
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Open')

    # When it was created, auto-set to current time
    created_at = models.DateTimeField(auto_now_add=True)

    # When it was resolved, nullable
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'fault_cases'

    def __str__(self):
        return f"Fault {self.id} for {self.machine_id}"



class FaultNote(models.Model):
    # Unique note ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Related fault case, foreign key to fault_cases table
    fault_case_id = models.ForeignKey('FaultCase', on_delete=models.CASCADE, to_field='id', null=False)

    # Who made the note, foreign key to users table
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id', null=False)

    # The note content, required
    note_text = models.TextField(null=False)

    # When it was written, auto-set to current time
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fault_notes'

    def __str__(self):
        return f"Note {self.id} for Fault {self.fault_case_id}"



class FaultNoteImage(models.Model):
    # Unique image ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Which note this image belongs to, foreign key to fault_notes table
    fault_note_id = models.ForeignKey('FaultNote', on_delete=models.CASCADE, to_field='id', null=False)

    # The binary image data, required
    image_data = models.BinaryField(null=False)

    # Original filename, nullable
    filename = models.CharField(max_length=100, null=True, blank=True)

    # Upload time, auto-set to current time
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fault_note_images'

    def __str__(self):
        return f"Image {self.id} for Note {self.fault_note_id}"



class FaultComment(models.Model):
    # Unique comment ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Which fault case the comment belongs to, foreign key to fault_cases table
    fault_case_id = models.ForeignKey('FaultCase', on_delete=models.CASCADE, to_field='id', null=False)

    # Who made the comment, foreign key to users table
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id', null=False)

    # The comment, required
    comment_text = models.TextField(null=False)

    # Time of commenting, auto-set to current time
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fault_comments'

    def __str__(self):
        return f"Comment {self.id} for Fault {self.fault_case_id}"



class MachineAssignment(models.Model):
    # Unique assignment ID, auto-incrementing primary key
    id = models.AutoField(primary_key=True)

    # Related machine, foreign key to machines table
    machine_id = models.ForeignKey('Machine', on_delete=models.CASCADE, to_field='machine_id', null=False)

    # Assigned user, foreign key to users table
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id', null=False, related_name='assignments')

    # Role on this machine enum, required
    ROLE_CHOICES = (('Technician', 'Technician'), ('Repair', 'Repair'))
    assigned_role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)

    # Who made the assignment, foreign key to users table
    assigned_by = models.ForeignKey('User', on_delete=models.CASCADE, to_field='id', null=False,
                                    related_name='assigned_tasks')

    # Assignment time, auto-set to current time
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'machine_assignments'

    def __str__(self):
        return f"{self.assigned_role} assignment for {self.machine_id} to {self.user_id}"