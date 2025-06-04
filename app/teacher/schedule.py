# app/routes/teacher_schedule_routes.py

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user, login_required
from app.models.teacher_schedule import Teacher_Schedule
from app.extensions import db
from datetime import time
from app.utils.decorators import teacher_required  # ⬅️

teacher_schedule_bp = Blueprint(
    "teacher_schedule",
    __name__,
    url_prefix="/api/teacher",  # 統一api路徑前綴
    template_folder="templates"
)

# 節次時間映射（與前端相同）
PERIOD_MAP = {
    1: (time(8,10), time(9,0)),
    2: (time(9,10), time(10,0)),
    3: (time(10,10), time(11,0)),
    4: (time(11,10), time(12,0)),
    5: (time(12,10), time(13,0)),
    6: (time(13,10), time(14,0)),
    7: (time(14,10), time(15,0)),
    8: (time(15,10), time(16,0)),
}

# 1. 任何人都可取得老師課表（公開）
@teacher_schedule_bp.route('/schedules', methods=['GET'])
def get_all_teacher_schedules():
    schedules = Teacher_Schedule.query.all()
    data = [{
        'id': s.id,
        'teacher_id': s.teacher_id,
        'teacher_name': s.teacher.nickname,  # 改用nickname
        'weekday': s.weekday,
        'start_time': s.start_time.strftime('%H:%M'),
        'end_time': s.end_time.strftime('%H:%M'),
        'course_name': s.course_name,
        'location': s.location
    } for s in schedules]
    return jsonify(data)


# 教師查看自己課表頁面（前端頁面）
@teacher_schedule_bp.route('/teacher/schedule', methods=['GET'])
@login_required
@teacher_required
def teacher_schedule_page():
    return render_template('teacher/teacher_schedule.html', currentUserId=current_user.id)


# 2. 新增課表（老師本人）
@teacher_schedule_bp.route('/schedules', methods=['POST'])
@login_required
@teacher_required
def add_teacher_schedule():
    data = request.json
    weekday = data.get('weekday')
    periods = data.get('periods')  # 範例: [1,2,3]
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


# 3. 取得特定課表（編輯用，老師本人）
@teacher_schedule_bp.route('/schedules/<int:schedule_id>', methods=['GET'])
@login_required
@teacher_required
def get_teacher_schedule(schedule_id):
    schedule = Teacher_Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    # 反查節次 period
    period = None
    for k, v in PERIOD_MAP.items():
        if v[0] == schedule.start_time and v[1] == schedule.end_time:
            period = k
            break

    data = {
        'id': schedule.id,
        'weekday': schedule.weekday,
        'period': period,
        'course_name': schedule.course_name,
        'location': schedule.location,
    }
    return jsonify(data)


# 4. 更新課表（老師本人）
@teacher_schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
@login_required
@teacher_required
def update_teacher_schedule(schedule_id):
    schedule = Teacher_Schedule.query.get_or_404(schedule_id)
    if schedule.teacher_id != current_user.id:
        return jsonify({'error': '無權限'}), 403

    data = request.json
    weekday = data.get('weekday')
    period = data.get('period')  # 單一節次
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


# 5. 刪除課表（老師本人）
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
