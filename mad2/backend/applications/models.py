from applications.database import db
from flask_security import UserMixin, RoleMixin


class User(db.Model, UserMixin):
   
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password=db.Column(db.String, nullable=False)
    active=db.Column(db.Boolean)
    fs_uniquifier=db.Column(db.String(),nullable=False)
    fs_token_uniquifier = db.Column(db.String(255),unique=True)
    blocked=db.Column(db.Boolean, default=False)
    
    addresses = db.relationship(
        'Address',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    roles = db.relationship('Role', secondary='user_roles', 
                            backref=db.backref('users', lazy=True))
    
    type = db.Column(db.String(50))  # This field will store the polymorphic type

    __mapper_args__ = {
        'polymorphic_on': type,  # Tells SQLAlchemy to use this field for polymorphic identity
        'polymorphic_identity': 'user'  # Default identity for base class
    }

    
class Role(db.Model, RoleMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(86), unique=True, nullable=False)
    description=db.Column(db.String)
    
    
class userRoles(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'))
    
    
class Professional(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    description = db.Column(db.Text, nullable=True)
    service_id = db.Column(db.Integer,db.ForeignKey('service.id'))
    experience = db.Column(db.Integer, nullable=False)
    total_ratings=db.Column(db.Integer, default=0)
    avg_rating=db.Column(db.Numeric(4, 2), default=0.0)

    __mapper_args__ = {
        'polymorphic_identity': 'professional'
    }

# Customer Model
class Customer(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    #name = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

#one professional can have many address
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address_line = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
#one servcie can have many professional
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    time_required = db.Column(db.String(50))
    
    professionals= db.relationship('Professional', backref='services')

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'))
    date_of_request = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_of_completion = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="requested")
    remarks = db.Column(db.Text)
    reviewed=db.Column(db.Boolean, default=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

