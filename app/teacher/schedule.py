# app/teacher/schedule.py

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user, login_required
from app.models.teacher_schedule import Teacher_Schedule
from app.models.teacher_available_schedule import Teacher_Available_Schedule
from app.models.user import User
from app.extensions import db
from datetime import time
from app.utils.decorators import teacher_required

# API用的 blueprint
teacher_schedule_bp = Blueprint(
    "teacher_schedule",
    __name__,
    url_prefix="/api/teacher",
    template_folder="templates"
)

# 前端公開頁面用 blueprint（路徑更友善）
teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher",
    template_folder="templates/teacher"
)

PERIOD_MAP = {
    1: (time(8, 10), time(9, 0)),
    2: (time(9, 10), time(10, 0)),
    3: (time(10, 10), time(11, 0)),
    4: (time(11, 10), time(12, 0)),
    5: (time(12, 10), time(13, 0)),
    6: (time(13, 10), time(14, 0)),
    7: (time(14, 10), time(15, 0)),
    8: (time(15, 10), time(16, 0)),
}

# ---------- 課表功能 ----------

@teacher_schedule_bp.route('/schedules', methods=['GET'])
def get_all_teacher_schedules():
    schedules = Teacher_Schedule.query.all()
    data = [{
        'id': s.id,
        'teacher_id': s.teacher_id,
        'teacher_name': s.teacher.nickname,
        'weekday': s.weekday,
        'start_time': s.start_time.strftime('%H:%M'),
        'end_time': s.end_time.strftime('%H:%M'),
        'course_name': s.course_name,
        'location': s.location
    } for s in schedules]
    return jsonify(data)

@teacher_bp.route('/public_profile/<string:account>')
def public_profile(account):
    teacher = User.query.filter_by(account=account).first_or_404()
    schedules = Teacher_Schedule.query \
        .filter_by(teacher_id=teacher.id) \
        .order_by(Teacher_Schedule.weekday, Teacher_Schedule.start_time) \
        .all()
    return render_template('teacher/public_profile.html', teacher=teacher, schedules=schedules)

@teacher_schedule_bp.route('/teacher/schedule', methods=['GET'])
@login_required
@teacher_required
def teacher_schedule_page():
    return render_template('teacher/teacher_schedule.html', currentUserId=current_user.id)

@teacher_schedule_bp.route('/schedules', methods=['POST'])
@login_required
@teacher_required
def add_teacher_schedule():
    data = request.json
    weekday = data.get('weekday')
    periods = data.get('periods')
    course_name = data.get('course_name')
    location = data.get('location')

    if weekday is None or not periods or not course_name or not location:
        return jsonify({'error': '資料不完整'}), 400

    for p in periods:
        start_time, end_time = PERIOD_MAP.get(p, (None, None))
        if not start_time:
            continue
        new_schedule = Teacher_Schedule(
            teacher_id=current_user.id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            course_name=course_name,
            location=location
        )
        db.session.add(new_schedule)

    db.session.commit()
    return jsonify({'message': '新增成功'}), 201

@teacher_schedule_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
@login_required
@teacher_required
def get_teacher_schedule(schedule_id):
    schedule = Teacher_Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    period = next((k for k, v in PERIOD_MAP.items()
                   if v[0] == schedule.start_time and v[1] == schedule.end_time), None)

    data = {
        'id': schedule.id,
        'weekday': schedule.weekday,
        'period': period,
        'course_name': schedule.course_name,
        'location': schedule.location,
    }
    return jsonify(data)

@teacher_schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
@login_required
@teacher_required
def update_teacher_schedule(schedule_id):
    schedule = Teacher_Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    data = request.json
    weekday = data.get('weekday')
    period = data.get('period')
    course_name = data.get('course_name')
    location = data.get('location')

    if None in (weekday, period) or not course_name or not location:
        return jsonify({'error': '資料不完整'}), 400

    start_time, end_time = PERIOD_MAP.get(period, (None, None))
    if not start_time:
        return jsonify({'error': '無效的節次'}), 400

    schedule.weekday = weekday
    schedule.start_time = start_time
    schedule.end_time = end_time
    schedule.course_name = course_name
    schedule.location = location

    db.session.commit()
    return jsonify({'message': '更新成功'})

@teacher_schedule_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
@login_required
@teacher_required
def delete_teacher_schedule(schedule_id):
    schedule = Teacher_Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        return jsonify({'error': '無權限'}), 403
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': '刪除成功'})

# ---------- 可預約空堂設定 ----------

@teacher_schedule_bp.route('/available_slots', methods=['POST'])
@login_required
@teacher_required
def set_available_slots():
    data = request.json
    weekday = data.get('weekday')
    periods = data.get('periods')  # 範例: [3,4]

    if weekday is None or not periods:
        return jsonify({'error': '資料不完整'}), 400

    for p in periods:
        start_time, end_time = PERIOD_MAP.get(p, (None, None))
        if not start_time:
            continue
        slot = Teacher_Available_Schedule(
            teacher_id=current_user.id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            is_available=True
        )
        db.session.add(slot)

    db.session.commit()
    return jsonify({'message': '可預約時段設定成功'})

@teacher_schedule_bp.route('/available_slots', methods=['GET'])
@login_required
@teacher_required
def get_my_available_slots():
    slots = Teacher_Available_Schedule.query.filter_by(
        teacher_id=current_user.id, is_available=True
    ).order_by(Teacher_Available_Schedule.weekday, Teacher_Available_Schedule.start_time).all()

    result = [{
        'id': s.id,
        'weekday': s.weekday,
        'start_time': s.start_time.strftime('%H:%M'),
        'end_time': s.end_time.strftime('%H:%M')
    } for s in slots]
    return jsonify(result)

@teacher_schedule_bp.route('/available_slots/<int:slot_id>', methods=['DELETE'])
@login_required
@teacher_required
def delete_available_slot(slot_id):
    slot = Teacher_Available_Schedule.query.get_or_404(slot_id)

    if slot.teacher_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    db.session.delete(slot)
    db.session.commit()
    return jsonify({'message': '刪除成功'})
