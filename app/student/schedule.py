# app/student/schedule.py
from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from app.extensions import db 
from app.models.student_schedule import Student_Schedule
from datetime import time
from sqlalchemy import or_, and_
import traceback

student_schedule_bp = Blueprint(
    "student_schedule",
    __name__,
    url_prefix="/api/schedules",
    template_folder="templates"
)

# 節次對應時間表 (固定)
PERIOD_TIME_MAP = {
    1: (time(8,10), time(9,0)),
    2: (time(9,10), time(10,0)),
    3: (time(10,10), time(11,0)),
    4: (time(11,10), time(12,0)),
    5: (time(12,10), time(13,0)),
    6: (time(13,10), time(14,0)),
    7: (time(14,10), time(15,0)),
    8: (time(15,10), time(16,0)),
    9: (time(16,10), time(17,0)),
    10: (time(17,10), time(18,0)),
    11: (time(18,10), time(19,0)),
    12: (time(19,10), time(20,0)),
    13: (time(20,10), time(21,0)),
    14: (time(21,10), time(22,0)),
}

def get_period_from_time(start_time, end_time):
    """比對時間並取得對應的節次，允許毫秒差異"""
    for k, (s, e) in PERIOD_TIME_MAP.items():
        if s.hour == start_time.hour and s.minute == start_time.minute and \
           e.hour == end_time.hour and e.minute == end_time.minute:
            return k
    return None

@student_schedule_bp.route('/page', methods=['GET'])
@login_required
def schedule_page():
    return render_template('student/student_schedule.html')

@student_schedule_bp.route('', methods=['GET'])
@login_required
def get_schedule():
    user = current_user
    schedules = Student_Schedule.query.filter_by(student_id=user.id).all()

    def schedule_to_dict(s):
        return {
            "id": s.id,
            "weekday": s.weekday,
            "start_time": s.start_time.strftime("%H:%M") if s.start_time else None,
            "end_time": s.end_time.strftime("%H:%M") if s.end_time else None,
            "course_name": s.course_name,
            "location": s.location
        }

    return jsonify([schedule_to_dict(s) for s in schedules])

@student_schedule_bp.route('', methods=['POST'])
@login_required
def add_schedule():
    data = request.get_json()
    weekday = data.get('weekday')
    periods = data.get('periods')
    course_name = data.get('course_name', '').strip()
    location = data.get('location', '').strip()

    if not isinstance(weekday, int) or not (0 <= weekday <= 6):
        return jsonify({'error': 'weekday 必須是 0 到 6 的整數'}), 400
    if not isinstance(periods, list) or not periods:
        return jsonify({'error': 'periods 必須是非空的節次列表'}), 400

    schedules_to_add = []
    for p in periods:
        if not isinstance(p, int) or p not in PERIOD_TIME_MAP:
            return jsonify({'error': f'節次 {p} 不合法'}), 400
        start_time, end_time = PERIOD_TIME_MAP[p]

        conflict = Student_Schedule.query.filter_by(student_id=current_user.id, weekday=weekday).filter(
            or_(
                and_(Student_Schedule.start_time <= start_time, Student_Schedule.end_time > start_time),
                and_(Student_Schedule.start_time < end_time, Student_Schedule.end_time >= end_time),
                and_(Student_Schedule.start_time >= start_time, Student_Schedule.end_time <= end_time)
            )
        ).first()
        if conflict:
            return jsonify({'error': f'節次 {p} 的時間與現有課表衝突'}), 400

        schedules_to_add.append((start_time, end_time))

    try:
        for start_time, end_time in schedules_to_add:
            schedule = Student_Schedule(
                student_id=current_user.id,
                weekday=weekday,
                start_time=start_time,
                end_time=end_time,
                course_name=course_name,
                location=location
            )
            db.session.add(schedule)
        db.session.commit()
        return jsonify({'message': '課表新增成功'}), 201
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': '資料庫錯誤，新增失敗', 'details': str(e)}), 500

@student_schedule_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_schedule(id):
    schedule = Student_Schedule.query.get_or_404(id)
    if schedule.student_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    data = request.get_json()
    weekday = data.get('weekday')
    course_name = data.get('course_name', '').strip()
    location = data.get('location', '').strip()

    if not isinstance(weekday, int) or not (0 <= weekday <= 6):
        return jsonify({'error': 'weekday 必須是 0 到 6 的整數'}), 400

    period = data.get('period')
    if not isinstance(period, int) or period not in PERIOD_TIME_MAP:
        return jsonify({'error': 'period 節次不合法'}), 400

    start_time, end_time = PERIOD_TIME_MAP[period]

    conflict = Student_Schedule.query.filter_by(student_id=current_user.id, weekday=weekday).filter(
        Student_Schedule.id != id
    ).filter(
        or_(
            and_(Student_Schedule.start_time <= start_time, Student_Schedule.end_time > start_time),
            and_(Student_Schedule.start_time < end_time, Student_Schedule.end_time >= end_time),
            and_(Student_Schedule.start_time >= start_time, Student_Schedule.end_time <= end_time)
        )
    ).first()
    if conflict:
        return jsonify({'error': '課程時間與現有課表衝突'}), 400

    schedule.weekday = weekday
    schedule.start_time = start_time
    schedule.end_time = end_time
    schedule.course_name = course_name
    schedule.location = location
    db.session.commit()
    return jsonify({'message': '課表更新成功'})

@student_schedule_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_single_schedule(id):
    schedule = Student_Schedule.query.get_or_404(id)
    if schedule.student_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    try:
        period = get_period_from_time(schedule.start_time, schedule.end_time)

        return jsonify({
            'id': schedule.id,
            'weekday': schedule.weekday,
            'period': period,
            'start_time': schedule.start_time.strftime('%H:%M') if schedule.start_time else None,
            'end_time': schedule.end_time.strftime('%H:%M') if schedule.end_time else None,
            'course_name': schedule.course_name,
            'location': schedule.location
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': '伺服器錯誤', 'details': str(e)}), 500

@student_schedule_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_schedule(id):
    schedule = Student_Schedule.query.get_or_404(id)
    if schedule.student_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': '課表刪除成功'})
