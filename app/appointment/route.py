# app/appointment/route.py

from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from datetime import timedelta, date, datetime
from app.models.teacher_available_schedule import Teacher_Available_Schedule
from app.models.appointment import Appointment
from app.extensions import db

appointment_bp = Blueprint(
    'appointment',
    __name__,
    url_prefix='/api/appointment',
    template_folder='templates'
)

@appointment_bp.route('/student')
@login_required
def student_appointment_page():
    # 這裡只負責渲染頁面，實際資料由 JS 透過 API 讀取
    return render_template('appointment/student_appointment.html')

# 取得教師某段時間內開放的預約時段（例如未來30天）
@appointment_bp.route('/teacher/<int:teacher_id>/available_slots', methods=['GET'])
@login_required
def get_teacher_available_slots(teacher_id):
    today = date.today()
    last_day = today + timedelta(days=30)

    # 取得該教師所有可預約的時段 (固定星期幾時間段)
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
                    'slot_id': slot.id,
                    'date': single_date.isoformat(),
                    'weekday': slot.weekday,
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                })

    return jsonify({"slots": result})

# 學生新增預約
@appointment_bp.route('/add', methods=['POST'])
@login_required
def add_appointment():
    data = request.get_json()
    try:
        slot_id = data['slot_id']
        reason = data.get('reason', '')
        date_str = data['date']  # 前端需提供預約日期

        # 解析日期
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # 由 slot_id 找到時段
        slot = Teacher_Available_Schedule.query.filter_by(id=slot_id, is_available=True).first()
        if not slot:
            return jsonify({"error": "找不到對應的可預約時段"}), 400

        # 檢查日期的星期幾和 slot.weekday 是否符合
        if date_obj.weekday() != slot.weekday:
            return jsonify({"error": "預約日期與可預約時段星期不符"}), 400

        # 確認是否已有同時間預約
        exists = Appointment.query.filter_by(
            student_id=current_user.id,
            teacher_id=slot.teacher_id,
            date=date_obj,
            start_time=slot.start_time,
            end_time=slot.end_time
        ).first()

        if exists:
            return jsonify({"error": "你已經預約過這個時段"}), 400

        new_appointment = Appointment(
            student_id=current_user.id,
            teacher_id=slot.teacher_id,
            date=date_obj,
            start_time=slot.start_time,
            end_time=slot.end_time,
            note=reason
        )

        db.session.add(new_appointment)
        db.session.commit()

        return jsonify({"message": "預約已送出，等待教師審核"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 學生取消預約
@appointment_bp.route('/cancel/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.student_id != current_user.id:
        return jsonify({"error": "無權取消此預約"}), 403

    now = datetime.now()
    appointment_datetime = datetime.combine(appointment.date, appointment.start_time)
    if appointment_datetime <= now:
        return jsonify({"error": "預約已開始或過期，無法取消"}), 400

    if appointment.status in ['cancelled', 'rejected']:
        return jsonify({"error": "此預約已無法取消"}), 400

    appointment.status = 'cancelled'
    db.session.commit()

    return jsonify({"message": "預約已取消"})

@appointment_bp.route('/student/list', methods=['GET'])
@login_required
def get_student_appointments():
    appointments = Appointment.query.filter_by(student_id=current_user.id).order_by(Appointment.date.desc(), Appointment.start_time).all()
    result = []
    for app in appointments:
        result.append({
            'id': app.id,
            'teacher_name': app.teacher.display_name,  # 假設User模型有name欄位
            'date': app.date.isoformat(),
            'start_time': app.start_time.strftime('%H:%M'),
            'end_time': app.end_time.strftime('%H:%M'),
            'status': app.status,
            'note': app.note
        })
    return jsonify({'appointments': result})
