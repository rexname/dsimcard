from flask import Blueprint, render_template, request, redirect, url_for, jsonify

dashboard_bp = Blueprint('dashboard', __name__)



from .models import Phones
from flask import current_app
import re


@dashboard_bp.route('/')
def index():
    # Ambil semua data phones
    phones = Phones.query.all()
    # Natural sort by ID (e.g. mp16p-1, mp16p-2, ..., mp16p-10)
    def natural_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s.ID)]
    phones = sorted(phones, key=natural_key)
    return render_template('dashboard/index.html', phones=phones)

@dashboard_bp.route('/send_sms', methods=['GET'])
def send_sms_select():
    # Ambil semua data phones untuk dipilih
    phones = Phones.query.all()
    # Natural sort by ID (e.g. mp16p-1, mp16p-2, ..., mp16p-10)
    def natural_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s.ID)]
    phones = sorted(phones, key=natural_key)
    return render_template('dashboard/send_sms_select.html', phones=phones)

@dashboard_bp.route('/send_sms', methods=['POST'])
def send_sms_ajax():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        creator_id = request.form.get('creator_id')
        destination = request.form.get('destination')
        text = request.form.get('text')

        if not all([creator_id, destination, text]):
            return jsonify({'error': 'All fields are required'}), 400

        try:
            from datetime import datetime
            sms = Outbox(
                DestinationNumber=destination,
                TextDecoded=text,
                CreatorID=creator_id,
                Status='Reserved',
                UpdatedInDB=datetime.now(),
                InsertIntoDB=datetime.now(),
                SendingDateTime=datetime.now(),
                SendBefore='23:59:59',
                SendAfter='00:00:00',
                Coding='Default_No_Compression',
                UDH=None,
                Class=-1,
                MultiPart=False,
                RelativeValidity=-1,
                SenderID=None,
                SendingTimeOut=datetime.now(),
                DeliveryReport='default',
                Retries=0,
                Priority=0,
                StatusCode=-1
            )
            db.session.add(sms)
            db.session.commit()
            return jsonify({'success': True, 'message': 'SMS queued successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to queue SMS'}), 500
    else:
        return jsonify({'error': 'Invalid request'}), 400

# Route untuk kirim pesan

from .models import Outbox
from . import db

@dashboard_bp.route('/send_sms/<phone_id>', methods=['GET', 'POST'])
def send_sms(phone_id):
    message = None
    if request.method == 'POST':
        destination = request.form.get('destination')
        text = request.form.get('text')
        if destination and text:
            from datetime import datetime
            sms = Outbox(
                DestinationNumber=destination,
                TextDecoded=text,
                CreatorID=phone_id,
                Status='Reserved',
                UpdatedInDB=datetime.now(),
                InsertIntoDB=datetime.now(),
                SendingDateTime=datetime.now(),
                SendBefore='23:59:59',
                SendAfter='00:00:00',
                Coding='Default_No_Compression',
                UDH=None,
                Class=-1,
                MultiPart=False,
                RelativeValidity=-1,
                SenderID=None,
                SendingTimeOut=datetime.now(),
                DeliveryReport='default',
                Retries=0,
                Priority=0,
                StatusCode=-1
            )
            db.session.add(sms)
            db.session.commit()
            message = 'Pesan berhasil dikirim ke antrian Outbox.'
        else:
            message = 'Nomor tujuan dan isi pesan wajib diisi.'
    return render_template('dashboard/send_sms.html', phone_id=phone_id, message=message)

# Route untuk lihat pesan
from .models import Sentitems, Inbox
from flask import render_template

@dashboard_bp.route('/view_sms/<phone_id>')
def view_sms(phone_id):
    # Ambil SMS terkirim (sentitems) dan masuk (inbox) untuk device
    sent = Sentitems.query.filter_by(SenderID=phone_id).order_by(Sentitems.SendingDateTime.desc()).all()
    inbox = Inbox.query.filter_by(RecipientID=phone_id).order_by(Inbox.ReceivingDateTime.desc()).all()
    return render_template('dashboard/view_sms.html', phone_id=phone_id, sent=sent, inbox=inbox)

@dashboard_bp.route('/api/messages/<phone_id>')
def api_messages(phone_id):
    sent = Sentitems.query.filter_by(SenderID=phone_id).order_by(Sentitems.SendingDateTime.desc()).all()
    inbox = Inbox.query.filter_by(RecipientID=phone_id).order_by(Inbox.ReceivingDateTime.desc()).all()
    sent_data = [
        {
            'SendingDateTime': sms.SendingDateTime.strftime('%Y-%m-%d %H:%M:%S') if sms.SendingDateTime else '',
            'DestinationNumber': sms.DestinationNumber,
            'TextDecoded': sms.TextDecoded,
            'Status': sms.Status
        } for sms in sent
    ]
    inbox_data = [
        {
            'ReceivingDateTime': sms.ReceivingDateTime.strftime('%Y-%m-%d %H:%M:%S') if sms.ReceivingDateTime else '',
            'SenderNumber': sms.SenderNumber,
            'TextDecoded': sms.TextDecoded,
            'Status': sms.Status
        } for sms in inbox
    ]
    return jsonify({'sent': sent_data, 'inbox': inbox_data})

# Route Inbox
@dashboard_bp.route('/inbox')
def inbox():
    from .models import Inbox
    inbox = Inbox.query.order_by(Inbox.ReceivingDateTime.desc()).limit(100).all()
    return render_template('dashboard/inbox.html', inbox=inbox)

# Route Outbox
@dashboard_bp.route('/outbox')
def outbox():
    from .models import Outbox, Sentitems
    outbox = Outbox.query.order_by(Outbox.InsertIntoDB.desc()).limit(100).all()
    sentitems = Sentitems.query.order_by(Sentitems.SendingDateTime.desc()).limit(100).all()
    phones = Phones.query.all()
    # Natural sort by ID (e.g. mp16p-1, mp16p-2, ..., mp16p-10)
    def natural_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s.ID)]
    phones = sorted(phones, key=natural_key)
    return render_template('dashboard/outbox.html', outbox=outbox, sentitems=sentitems, phones=phones)

# Route Setting
import json
import os
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'settings.json')

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH) as f:
            return json.load(f)
    return {"phone_id": ""}

def save_settings(data):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(data, f)

@dashboard_bp.route('/setting', methods=['GET', 'POST'])
def setting():
    message = None
    settings = load_settings()
    current_id = settings.get('phone_id', '')
    if request.method == 'POST':
        new_id = request.form.get('phone_id')
        if new_id:
            settings['phone_id'] = new_id
            save_settings(settings)
            message = 'Phone ID berhasil diupdate.'
            current_id = new_id
        else:
            message = 'Phone ID tidak boleh kosong.'
    return render_template('dashboard/setting.html', current_id=current_id, message=message)