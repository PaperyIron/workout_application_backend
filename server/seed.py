#!/usr/bin/env python3

from app import app
from models import *
from datetime import date

with app.app_context():
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    push_ups = Exercise(name="Push-ups", category="strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="strength", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)
    deadlifts = Exercise(name="Deadlifts", category="strength", equipment_needed=True)

    db.session.add_all([push_ups, squats, bench_press, deadlifts])
    db.session.commit()

    workout1 = Workout(date=date(2024, 12, 15), duration_minutes=45, notes="Great upper body workout!")
    workout2 = Workout(date=date(2024, 12, 16), duration_minutes=30, notes="Quick leg day session.")
    workout3 = Workout(date=date(2024, 12, 17), duration_minutes=60, notes="Cardio day - long run.")
    workout4 = Workout(date=date(2024, 12, 18), duration_minutes=25, notes="Recovery with yoga.")

    db.session.add_all([workout1, workout2, workout3, workout4])
    db.session.commit()

    we1 = WorkoutExercises(workout_id=workout1.id, exercise_id=push_ups.id, reps=15, sets=4)
    we2 = WorkoutExercises(workout_id=workout1.id, exercise_id=bench_press.id, reps=10, sets=4)
    we3 = WorkoutExercises(workout_id=workout2.id, exercise_id=squats.id, reps=12, sets=3)
    we4 = WorkoutExercises(workout_id=workout2.id, exercise_id=deadlifts.id, reps=8, sets=3)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()