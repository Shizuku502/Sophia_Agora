# app/appointment/route.py

from flask import Blueprint, jsonify, request, render_template, url_for
from flask_login import login_required, current_user
from datetime import timedelta, date, datetime
from app.models.teacher_available_schedule import Teacher_Available_Schedule
from app.models.appointment import Appointment
from app.models.notification import Notification  # ✅ 新增
from app.models.user import User
from app.extensions import db

appointment_bp = Blueprint(
    'appointment',
    __name__,
    url_prefix='/api/appointment',
    template_folder='templates'
)

# === 學生相關路由 ===

@appointment_bp.route('/student')
@login_required
def student_appointment_page():
    return render_template('appointment/student_appointment.html')


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
                    'slot_id': slot.id,
                    'date': single_date.isoformat(),
                    'weekday': slot.weekday,
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                })
    return jsonify({"slots": result})


@appointment_bp.route('/add', methods=['POST'])
@login_required
def add_appointment():
    data = request.get_json()
    try:
        slot_id = data['slot_id']
        reason = data.get('reason', '')
        date_str = data['date']
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        slot = Teacher_Available_Schedule.query.filter_by(id=slot_id, is_available=True).first()
        if not slot:
            return jsonify({"error": "找不到對應的可預約時段"}), 400

        if date_obj.weekday() != slot.weekday:
            return jsonify({"error": "預約日期與可預約時段星期不符"}), 400

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

        # ✅ 發送通知給教師
        teacher = User.query.get(slot.teacher_id)
        notification = Notification(
            user_id=teacher.id,
            type='appointment',
            content=f"{current_user.display_name} 提出了新的預約申請。",
            link=url_for('appointment.teacher_appointment_page')
        )
        db.session.add(notification)

        db.session.commit()
        return jsonify({"message": "預約已送出，等待教師審核"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = Appointment.query.filter_by(student_id=current_user.id)\
        .order_by(Appointment.date.desc(), Appointment.start_time)\
        .paginate(page=page, per_page=per_page, error_out=False)

    appointments = pagination.items
    result = []
    for app in appointments:
        result.append({
            'id': app.id,
            'teacher_name': app.teacher.display_name,
            'date': app.date.isoformat(),
            'start_time': app.start_time.strftime('%H:%M'),
            'end_time': app.end_time.strftime('%H:%M'),
            'status': app.status,
            'note': app.note,
            'rejection_reason': app.rejection_reason or ''
        })

    return jsonify({
        'appointments': result,
        'page': pagination.page,
        'pages': pagination.pages,
        'total': pagination.total
    })


# === 教師相關路由 ===

@appointment_bp.route('/teacher')
@login_required
def teacher_appointment_page():
    return render_template('appointment/teacher_appointment.html')


@appointment_bp.route('/teacher/list', methods=['GET'])
@login_required
def get_teacher_appointments():
    appointments = Appointment.query.filter_by(
        teacher_id=current_user.id
    ).order_by(Appointment.date.desc(), Appointment.start_time).all()

    result = []
    for app in appointments:
        result.append({
            'id': app.id,
            'student_name': app.student.display_name,
            'date': app.date.isoformat(),
            'start_time': app.start_time.strftime('%H:%M'),
            'end_time': app.end_time.strftime('%H:%M'),
            'status': app.status,
            'note': app.note,
            'rejection_reason': app.rejection_reason
        })

    return jsonify({'appointments': result})


@appointment_bp.route('/teacher/respond/<int:appointment_id>', methods=['POST'])
@login_required
def respond_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.teacher_id != current_user.id:
        return jsonify({'error': '無權處理此預約'}), 403

    if appointment.status != 'pending':
        return jsonify({'error': '預約已處理過'}), 400

    data = request.get_json()
    action = data.get('action')
    reason = data.get('reason', '')

    if action == 'accept':
        appointment.status = 'accepted'
        message = f"{current_user.display_name} 已接受你的預約申請。"
    elif action == 'reject':
        appointment.status = 'rejected'
        appointment.rejection_reason = reason
        message = f"{current_user.display_name} 拒絕了你的預約申請，原因：{reason}"
    else:
        return jsonify({'error': '未知的操作'}), 400

    # ✅ 發送通知給學生
    student = User.query.get(appointment.student_id)
    notification = Notification(
        user_id=student.id,
        type='appointment',
        content=message,
        link=url_for('appointment.student_appointment_page')
    )
    db.session.add(notification)

    db.session.commit()
    return jsonify({'message': f'預約已{appointment.status}'})
