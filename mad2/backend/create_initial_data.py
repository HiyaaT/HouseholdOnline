from flask_security.utils import hash_password
from applications.models import *
import uuid

def create_data(app, db):
    # Create or get roles
    admin_role = app.security.datastore.find_or_create_role(name='admin', description='Administrator')
    customer_role = app.security.datastore.find_or_create_role(name='customer', description='Customer')
    professional_role = app.security.datastore.find_or_create_role(name='professional', description='Professional')
    
    db.session.commit()

    # Add Services before creating Professionals
    services = [
        {
            'name': 'House Cleaning',
            'base_price': 50.00,
            'description': 'Thorough cleaning of your home including dusting, vacuuming, and mopping.',
            'time_required': '2 hours'
        },
        {
            'name': 'Plumbing',
            'base_price': 100.00,
            'description': 'Professional plumbing services for repairs and installations.',
            'time_required': '1 hour'
        },
        {
            'name': 'Electrical Repair',
            'base_price': 150.00,
            'description': 'Expert electrical repair services including wiring and installations.',
            'time_required': '1.5 hours'
        },
        {
            'name': 'Gardening',
            'base_price': 75.00,
            'description': 'Full garden maintenance and landscaping services.',
            'time_required': '3 hours'
        },
        {
            'name': 'Carpentry',
            'base_price': 120.00,
            'description': 'Custom woodworking and carpentry services.',
            'time_required': '2 hours'
        }
    ]

    for service_data in services:
        if not Service.query.filter_by(name=service_data['name']).first():
            service = Service(
                name=service_data['name'],
                base_price=service_data['base_price'],
                description=service_data['description'],
                time_required=service_data['time_required']
            )
            db.session.add(service)

    db.session.commit()  # Commit after adding all services

    # Create admin user if not exists
    if not app.security.datastore.find_user(email='admin@gmail.com'):
        app.security.datastore.create_user(
            name='admin',
            email='admin@gmail.com',
            password=hash_password('admin'),
            active=True,
            fs_uniquifier=str(uuid.uuid4()),
            roles=[admin_role]
        )

    # Create Customer if not exists
    if not Customer.query.filter_by(email='harry@gmail.com').first():
        customer = Customer(
            email='harry@gmail.com',
            name='Harry Singh',
            password=hash_password('123456'),
            active=True,
            fs_uniquifier=str(uuid.uuid4()),
            fs_token_uniquifier=str(uuid.uuid4()),
            roles=[customer_role]
        )
        db.session.add(customer)
        
        address = Address(
            user=customer, 
            address_line='123 Main Street',
            city='bhopal',
            state='MP',
            pincode='12345'
        )
        db.session.add(address)

    # Create Professional if not exists
    if not Professional.query.filter_by(email='ron@gmail.com').first():
        professional = Professional(
            email='ron@gmail.com',
            name='Ron roy',
            description='Expert service provider',
            password=hash_password('123456'),
            active=True,
            fs_uniquifier=str(uuid.uuid4()),
            fs_token_uniquifier=str(uuid.uuid4()),
            experience=5,
            roles=[professional_role],
            service_id=1  # Ensure service_id exists in the Service table
        )
        db.session.add(professional)
        
        address = Address(
            user=professional, 
            address_line='sp apartments',
            city='Bhopal',
            state='Madhya pradesh',
            pincode='45231'
        )
        db.session.add(address)

    db.session.commit()
