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
    workout = Workout.query.get(id)                    
    if not workout:                                   
        return {'error': 'Workout not found'}, 404
    return workout_schema.dump(workout), 200   

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()                     
        
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        new_workout = Workout(                        
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        
        db.session.add(new_workout)                   
        db.session.commit()                           
        
        return workout_schema.dump(new_workout), 201  
    
    except ValidationError as e:                      
        return {'errors': e.messages}, 400
    except ValueError as e:                           
        return {'error': str(e)}, 400
    except Exception as e:                            
        db.session.rollback()                         
        return {'error': str(e)}, 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)                   
    if not workout:                                   
        return {'error': 'Workout not found'}, 404
    
    db.session.delete(workout)                        
    db.session.commit()                               
    
    return '', 204    

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()                  
    return exercises_schema.dump(exercises), 200      

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)                 
    if not exercise:                                  
        return {'error': 'Exercise not found'}, 404
    return exercise_schema.dump(exercise), 200        

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()                     
        
        # Create new exercise object
        new_exercise = Exercise(                      
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        
        db.session.add(new_exercise)                  
        db.session.commit()                           
        
        return exercise_schema.dump(new_exercise), 201  
    
    except ValidationError as e:                      
        return {'errors': e.messages}, 400
    except ValueError as e:                           
        return {'error': str(e)}, 400
    except Exception as e:                            
        db.session.rollback()                         
        return {'error': str(e)}, 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)                 
    if not exercise:                                  
        return {'error': 'Exercise not found'}, 404
    
    db.session.delete(exercise)                       
    db.session.commit()                               
    
    return '', 204   

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        # Check if workout exists
        workout = Workout.query.get(workout_id)       
        if not workout:
            return {'error': 'Workout not found'}, 404
        
        # Check if exercise exists
        exercise = Exercise.query.get(exercise_id)    
        if not exercise:
            return {'error': 'Exercise not found'}, 404
        
        data = request.get_json()                     
        
        # Create WorkoutExercise relationship
        new_workout_exercise = WorkoutExercises(      
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        
        db.session.add(new_workout_exercise)          
        db.session.commit()                           
        
        return workout_exercises_schema.dump(new_workout_exercise), 201  
    
    except ValidationError as e:                      
        return {'errors': e.messages}, 400
    except ValueError as e:                           
        return {'error': str(e)}, 400
    except Exception as e:                            
        db.session.rollback()                         
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)