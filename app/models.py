from . import db
from flask_login import UserMixin
import bcrypt

class Gammu(db.Model):
    __tablename__ = 'gammu'
    Version = db.Column(db.SmallInteger, primary_key=True, default=0)

class Inbox(db.Model):
    __tablename__ = 'inbox'
    UpdatedInDB = db.Column(db.DateTime, nullable=False)
    ReceivingDateTime = db.Column(db.DateTime, nullable=False)
    Text = db.Column(db.Text, nullable=False)
    SenderNumber = db.Column(db.String(20), nullable=False, default='')
    Coding = db.Column(db.String(255), nullable=False, default='Default_No_Compression')
    UDH = db.Column(db.Text, nullable=False)
    SMSCNumber = db.Column(db.String(20), nullable=False, default='')
    Class = db.Column(db.Integer, nullable=False, default=-1)
    TextDecoded = db.Column(db.Text, nullable=False, default='')
    ID = db.Column(db.Integer, primary_key=True)
    RecipientID = db.Column(db.Text, nullable=False)
    Processed = db.Column(db.Boolean, nullable=False, default=False)
    Status = db.Column(db.Integer, nullable=False, default=-1)

class Outbox(db.Model):
    __tablename__ = 'outbox'
    UpdatedInDB = db.Column(db.DateTime, nullable=False)
    InsertIntoDB = db.Column(db.DateTime, nullable=False)
    SendingDateTime = db.Column(db.DateTime, nullable=False)
    SendBefore = db.Column(db.Time, nullable=False, default='23:59:59')
    SendAfter = db.Column(db.Time, nullable=False, default='00:00:00')
    Text = db.Column(db.Text)
    DestinationNumber = db.Column(db.String(20), nullable=False, default='')
    Coding = db.Column(db.String(255), nullable=False, default='Default_No_Compression')
    UDH = db.Column(db.Text)
    Class = db.Column(db.Integer, default=-1)
    TextDecoded = db.Column(db.Text, nullable=False, default='')
    ID = db.Column(db.Integer, primary_key=True)
    MultiPart = db.Column(db.Boolean, nullable=False, default=False)
    RelativeValidity = db.Column(db.Integer, default=-1)
    SenderID = db.Column(db.String(255))
    SendingTimeOut = db.Column(db.DateTime, nullable=False)
    DeliveryReport = db.Column(db.String(10), default='default')
    CreatorID = db.Column(db.Text, nullable=False)
    Retries = db.Column(db.Integer, default=0)
    Priority = db.Column(db.Integer, default=0)
    Status = db.Column(db.String(255), nullable=False, default='Reserved')
    StatusCode = db.Column(db.Integer, nullable=False, default=-1)

class OutboxMultipart(db.Model):
    __tablename__ = 'outbox_multipart'
    Text = db.Column(db.Text)
    Coding = db.Column(db.String(255), nullable=False, default='Default_No_Compression')
    UDH = db.Column(db.Text)
    Class = db.Column(db.Integer, default=-1)
    TextDecoded = db.Column(db.Text)
    ID = db.Column(db.Integer, primary_key=True)
    SequencePosition = db.Column(db.Integer, primary_key=True, default=1)
    Status = db.Column(db.String(255), nullable=False, default='Reserved')
    StatusCode = db.Column(db.Integer, nullable=False, default=-1)

class Phones(db.Model):
    __tablename__ = 'phones'
    ID = db.Column(db.Text, nullable=False)
    UpdatedInDB = db.Column(db.DateTime, nullable=False)
    InsertIntoDB = db.Column(db.DateTime, nullable=False)
    TimeOut = db.Column(db.DateTime, nullable=False)
    Send = db.Column(db.Boolean, nullable=False, default=False)
    Receive = db.Column(db.Boolean, nullable=False, default=False)
    IMEI = db.Column(db.String(35), primary_key=True, nullable=False)
    IMSI = db.Column(db.String(35), nullable=False)
    NetCode = db.Column(db.String(10), default='ERROR')
    NetName = db.Column(db.String(35), default='ERROR')
    Client = db.Column(db.Text, nullable=False)
    Battery = db.Column(db.Integer, nullable=False, default=-1)
    Signal = db.Column(db.Integer, nullable=False, default=-1)
    Sent = db.Column(db.Integer, nullable=False, default=0)
    Received = db.Column(db.Integer, nullable=False, default=0)

class Sentitems(db.Model):
    __tablename__ = 'sentitems'
    UpdatedInDB = db.Column(db.DateTime, nullable=False)
    InsertIntoDB = db.Column(db.DateTime, nullable=False)
    SendingDateTime = db.Column(db.DateTime, nullable=False)
    DeliveryDateTime = db.Column(db.DateTime)
    Text = db.Column(db.Text, nullable=False)
    DestinationNumber = db.Column(db.String(20), nullable=False, default='')
    Coding = db.Column(db.String(255), nullable=False, default='Default_No_Compression')
    UDH = db.Column(db.Text, nullable=False)
    SMSCNumber = db.Column(db.String(20), nullable=False, default='')
    Class = db.Column(db.Integer, nullable=False, default=-1)
    TextDecoded = db.Column(db.Text, nullable=False, default='')
    ID = db.Column(db.Integer, primary_key=True)
    SenderID = db.Column(db.String(255), nullable=False)
    SequencePosition = db.Column(db.Integer, primary_key=True, default=1)
    Status = db.Column(db.String(255), nullable=False, default='SendingOK')
    StatusError = db.Column(db.Integer, nullable=False, default=-1)
    TPMR = db.Column(db.Integer, nullable=False, default=-1)
    RelativeValidity = db.Column(db.Integer, nullable=False, default=-1)
    CreatorID = db.Column(db.Text, nullable=False)
    StatusCode = db.Column(db.Integer, nullable=False, default=-1)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship dengan UserDevice
    device_assignments = db.relationship('UserDevice', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class UserDevice(db.Model):
    __tablename__ = 'user_device'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone_id = db.Column(db.String(50), nullable=False)  # ID dari tabel Phones
    
    # Relationships
    user = db.relationship('User', back_populates='device_assignments')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'phone_id', name='unique_user_device'),)
