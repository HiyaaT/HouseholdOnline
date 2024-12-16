from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from flask_security import hash_password, utils, auth_token_required
from applications.user_datastore import user_datastore
from applications.database import db
import uuid
from applications.models import *
from flask_security import current_user


class ValidUser(Resource):
    def post(self):
        data=request.get_json()
        
        email=data.get('email', None)
        
        if email:
            user=User.query.filter_by(email=email).first()
            if user:
                return make_response(jsonify({'message':'Email exists'}), 405)
        return make_response(jsonify({'message':'you can use this email'}), 200)

class Registration(Resource):
    def post(self):
        data=request.get_json()
        email = data.get('email', None)
        password = data.get('password', None)
        name = data.get('name', None)
        role = data.get('role', None)
        description=data.get('description')
        service_id=data.get('service_id')
        experience=data.get('experience')
        
        
        
        address_line = data.get('address_line', None)
        city = data.get('city', None)
        state = data.get('state', None)
        pincode = data.get('pincode', None)
        
        if not email or '@' not in email:
            return make_response(jsonify({'message': 'email is required or Invalid email Entered '}), 401)
        
        if not name:
            return make_response(jsonify({'message': 'name is required'}), 401)
        
        if not password or len(password) < 6:
            return make_response(jsonify({'message': 'password is required and should be atleast 6 characters'}), 401)
        
        if role not in ['customer', 'professional']:
            return make_response(jsonify({'message': 'role is required and should be either customer or store_manager'}), 401)
        
        if not all([address_line, city, state, pincode]):
            return make_response(jsonify({'message': 'Complete address is required'}), 401)
        
        user = user_datastore.find_user(email=email)
        if user: 
            return make_response(jsonify({'message': 'User already exists with this email'}), 401)
        
        try:
            r=user_datastore.find_role(role)
            
            if role == 'customer':
                user=Customer(
                email=email,
                name=name,
                password=hash_password(password),
                active=True,
                fs_uniquifier=str(uuid.uuid4()),
                fs_token_uniquifier = str(uuid.uuid4()),
                roles=[r]  
               )
                db.session.add(user)
            
            else:
                if not description or not service_id or not experience:
                    return make_response(jsonify({'message': 'please enter professional details'}), 401)
                    
                user=Professional(
                    email=email,
                    name=name,
                    description=description,
                    service_id=service_id,
                    password=hash_password(password),
                    active=False,
                    fs_uniquifier=str(uuid.uuid4()),
                    fs_token_uniquifier = str(uuid.uuid4()),
                    experience=experience,
                    roles=[r] 
                )
                db.session.add(user)
                
            address = Address(
                user=user,
                address_line=address_line,
                city=city,
                state=state,
                pincode=pincode      
            )
            db.session.add(address)
                   
            user_datastore.commit()

            

            return {'message':'success'}, 201
        except Exception as e:
            response = {
                'message': 'Internal Server Error',
                'error': str(e)
            }
            return make_response(jsonify(response), 500)
        
        
        
class Login(Resource):
    def post(self):
        request_data = request.get_json()
        email = request_data.get('email', None)
        password = request_data.get('password', None)

        if not email or not password:
            return make_response(jsonify({'message': 'email and password are required'}), 401)
        
        user = user_datastore.find_user(email=email)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 401)
        
        if not utils.verify_password(password, user.password):
            return make_response(jsonify({'message': 'Invalid Password'}), 401)
        
        if not user.active:
            return make_response(jsonify({'message': 'User account is not active, login not allowed'}), 403)
        if user.blocked:
            return make_response(jsonify({'message': 'User account has been blocked authentication denied ;-;'}), 403)

        
        
       

        try:
            utils.login_user(user)
            auth_token = user.get_auth_token()
            
            if user.roles[0]=='professional':
                response={
                    'message': 'User successfully logged in',
                "login_credentials": {
                    'id':user.id,
                    'email': user.email,
                    'name':user.name,
                    'roles': [role.name for role in user.roles],
                    'auth_token': auth_token,
                    'service_id':user.service_id
                },
                }
            elif user.roles[0]=='admin' or user.roles[0]=='customer':
                 response={
                'message': 'User successfully logged in',
                "login_credentials": {
                    'id':user.id,
                    'email': user.email,
                    'name':user.name,
                    'roles': [role.name for role in user.roles],
                    'auth_token': auth_token
                },
                }

            return make_response(jsonify(response), 200)
        
        except Exception as e:
            response = {
                'message': 'Internal Server Error',
                'error': str(e)
            }
            return make_response(jsonify(response), 500)
        

class Logout(Resource):
    @auth_token_required
    def post(self):
        
        utils.logout_user()
    
        response = {
            'message': 'logged out'
        }
        return make_response(jsonify(response), 200)


