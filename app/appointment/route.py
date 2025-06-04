# app/appointment/route.py

from flask import Blueprint, jsonify
from flask_login import login_required
from datetime import timedelta, date
from app.models.teacher_available_schedule import Teacher_Available_Schedule

appointment_bp = Blueprint(
    'appointment',
    __name__,
    url_prefix='/api/appointment/'
)

@appointment_bp.route('/teacher/<int:teacher_id>/available_slots', methods=['GET'])
@login_required
def get_teacher_available_slots(teacher_id):
    today = date.today()
    last_day = today + timedelta(days=30)

    all_slots = Teacher_Available_Schedule.query.filter_by(
        teacher_id=teacher_id,
        is_available=True
    ).all()

    result = []

    for single_date in (today + timedelta(n) for n in range(31)):
        weekday = single_date.weekday()
        for slot in all_slots:
            if slot.weekday == weekday:
                result.append({
                    'date': single_date.isoformat(),
                    'weekday': slot.weekday,
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                })

    return jsonify(result)