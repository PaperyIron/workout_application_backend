from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import datetime
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()                    
    return workouts_schema.dump(workouts), 200 

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)                   # ← Query single workout
    if not workout:                                   # ← Handle not found
        return {'error': 'Workout not found'}, 404
    return workout_schema.dump(workout), 200   

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()                     # ← Get JSON from request
        
        # Convert date string to date object
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # Create new workout object
        new_workout = Workout(                        # ← Create model instance
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        
        db.session.add(new_workout)                   # ← Add to session
        db.session.commit()                           # ← Commit to database
        
        return workout_schema.dump(new_workout), 201  # ← Serialize and return 201
    
    except ValidationError as e:                      # ← Handle validation errors
        return {'errors': e.messages}, 400
    except ValueError as e:                           # ← Handle model validation errors
        return {'error': str(e)}, 400
    except Exception as e:                            # ← Handle other errors
        db.session.rollback()                         # ← Rollback on error
        return {'error': str(e)}, 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)                   # ← Find workout
    if not workout:                                   # ← Handle not found
        return {'error': 'Workout not found'}, 404
    
    db.session.delete(workout)                        # ← Delete (cascade handles WorkoutExercises)
    db.session.commit()                               # ← Commit
    
    return '', 204    

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()                  # ← Query all exercises
    return exercises_schema.dump(exercises), 200      # ← Serialize and return

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)                 # ← Query single exercise
    if not exercise:                                  # ← Handle not found
        return {'error': 'Exercise not found'}, 404
    return exercise_schema.dump(exercise), 200        #

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()                     # ← Get JSON from request
        
        # Create new exercise object
        new_exercise = Exercise(                      # ← Create model instance
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        
        db.session.add(new_exercise)                  # ← Add to session
        db.session.commit()                           # ← Commit to database
        
        return exercise_schema.dump(new_exercise), 201  # ← Serialize and return 201
    
    except ValidationError as e:                      # ← Handle validation errors
        return {'errors': e.messages}, 400
    except ValueError as e:                           # ← Handle model validation errors
        return {'error': str(e)}, 400
    except Exception as e:                            # ← Handle other errors
        db.session.rollback()                         # ← Rollback on error
        return {'error': str(e)}, 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)                 # ← Find exercise
    if not exercise:                                  # ← Handle not found
        return {'error': 'Exercise not found'}, 404
    
    db.session.delete(exercise)                       # ← Delete (cascade handles WorkoutExercises)
    db.session.commit()                               # ← Commit
    
    return '', 204   

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        # Check if workout exists
        workout = Workout.query.get(workout_id)       # ← Validate workout exists
        if not workout:
            return {'error': 'Workout not found'}, 404
        
        # Check if exercise exists
        exercise = Exercise.query.get(exercise_id)    # ← Validate exercise exists
        if not exercise:
            return {'error': 'Exercise not found'}, 404
        
        data = request.get_json()                     # ← Get JSON data
        
        # Create WorkoutExercise relationship
        new_workout_exercise = WorkoutExercises(      # ← Create join table record
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        
        db.session.add(new_workout_exercise)          # ← Add to session
        db.session.commit()                           # ← Commit
        
        return workout_exercises_schema.dump(new_workout_exercise), 201  # ← Serialize and return
    
    except ValidationError as e:                      # ← Handle schema validation errors
        return {'errors': e.messages}, 400
    except ValueError as e:                           # ← Handle model validation errors
        return {'error': str(e)}, 400
    except Exception as e:                            # ← Handle other errors
        db.session.rollback()                         # ← Rollback on error
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)