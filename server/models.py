from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

# Define Models here
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise')
    workouts = db.relationship('Workout', secondary= 'workout_exercises', back_populates='exercises')

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip) == 0:
            raise ValueError('Name cannot be empty')
        
        if len(name) > 50:
            raise ValueError('Name must be 50 characters or less.')
        
        return name.strip()


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercises', back_populates='workout')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes < 0:
            raise ValueError('Cannot be a negative number.')
        
        return duration_minutes
    
    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 1000:
            raise ValueError('Cannot be longer than 1000 characters.')


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