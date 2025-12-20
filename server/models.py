from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary= 'workout_exercises', back_populates='exercises', viewonly=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError('Name cannot be empty')
        
        if len(name) > 50:
            raise ValueError('Name must be 50 characters or less.')
        
        return name.strip()
    
class ExerciseSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String()
    equipment_needed = fields.Boolean()
    workout_exercises = fields.Nested('WorkoutExercisesSchema', many=True, exclude=('exercise',))



class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', viewonly=True)

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes < 0:
            raise ValueError('Cannot be a negative number.')
        
        return duration_minutes
    
    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 1000:
            raise ValueError('Cannot be longer than 1000 characters.')
        
        return notes
        
class WorkoutSchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()
    workout_exercises = fields.Nested('WorkoutExercisesSchema', many=True, exclude=('workout',))

    notes = fields.String(validate=validate.Length(max=1000))



class WorkoutExercises(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

class WorkoutExercisesSchema(Schema):
    id = fields.Integer()
    workout_id = fields.Integer()
    exercise_id = fields.Integer()
    reps = fields.Integer()
    sets = fields.Integer()
    duration_seconds = fields.Integer()
    workout = fields.Nested('WorkoutSchema', exclude=('workout_exercises',))
    exercises = fields.Nested('ExerciseSchema', exclude=('workout_exercises',))

    duration_seconds = fields.Integer(validate=validate.Range(min=1))




exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercises_schema = WorkoutExercisesSchema()
workout_exercises_schemas = WorkoutExercisesSchema(many=True)