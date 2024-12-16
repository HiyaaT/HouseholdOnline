from flask_restful import Resource, reqparse, marshal_with, fields
from flask import jsonify, request, make_response, current_app as app
from applications.database import db
from applications.models import *
from flask_security import auth_token_required, roles_required
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import and_


cache = app.cache

parser = reqparse.RequestParser() # convert data to dict

parser.add_argument('name', type=str)
parser.add_argument('base_price', type=int)
parser.add_argument('description', type=str)
parser.add_argument('time_required', type=str)


services_fields={
    'id':fields.Integer,
    'name':fields.String,
    'base_price':fields.Float,
    'description':fields.String,
    'time_required':fields.String,
}

class Services(Resource):
    cache.cached(timeout = 5)
    @marshal_with(services_fields)
    def get(self):
        all_resources = Service.query.all()
        return all_resources

    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        args = parser.parse_args()
        service=Service.query.filter_by(name=args.name).first()
        if service:
            return {'message':'service already exsits'}, 401
        
        service_resource = Service(name = args.name, base_price= args.base_price, description = args.description, time_required=args.time_required)
        db.session.add(service_resource)
        db.session.commit()
        return {'message' : 'resource created'}, 200
    
    
class ServiceDetail(Resource):
    @auth_token_required
    @roles_required('admin')
    def delete(self, id):
        to_del = Service.query.filter_by(id=id).first()
        professionals = Professional.query.filter_by(service_id=id).all()
        for professional in professionals:
            professional.service_id = 0
        sr=ServiceRequest.query.filter_by(service_id=id).all()
        for rq in sr:
            rev=Review.query.filter_by(service_request_id=rq.id).first()
            if rev:
                db.session.delete(rev)
            db.session.delete(rq)
        db.session.delete(to_del)
        db.session.commit()

        return {'message': 'Service deleted successfully, and related professionals have been updated'}, 200

    
    @auth_token_required
    @roles_required("admin")
    def put(self, id):
        update_service=Service.query.filter_by(id=id).first()
        if not update_service:
            return {'message': 'Service not found'}, 404
        args = parser.parse_args()
        if args.name:
            update_service.name=args.name
        if args.base_price:
            update_service.base_price=args.base_price
        if args.description:
            update_service.description=args.description
        if args.time_required:
            update_service.time_required=args.time_required
        db.session.commit()
        return {'message':'success'}, 200
    
    
class ApproveProfessional(Resource):
    @auth_token_required
    @roles_required('admin')
    def put(self, id):
        try:
            user  = User.query.filter_by(id=id).first()
            if not user:
                return make_response(jsonify({'message': 'User not found'}), 404)
            
            user.active = True
            db.session.commit()
            return make_response(jsonify({'message': 'User approved successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)
    
    


class Professionals(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        result = []
        for i in users:
            if 'professional' in [role.name for role in i.roles]:
                address=Address.query.filter_by(user_id=i.id).first()
                response = {
                    'id':i.id,
                    'name': i.name,
                    'email': i.email,
                    'description': i.description,
                    'active': i.active,
                    'service':Service.query.filter_by(id=i.service_id).first().name,
                    'blocked':i.blocked,
                    'experience':i.experience,
                    'pincode':address.pincode,
                    'city':address.city
                    
                }
                result.append(response)
        return make_response(jsonify(result), 200)
    
    
    
class Customers(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        result = []
        for i in users:
            if 'customer' in [role.name for role in i.roles]:
                address=Address.query.filter_by(user_id=i.id).first()
                response = {
                    'id':i.id,
                    'name': i.name,
                    'email': i.email,
                    'active': i.active,
                    'blocked':i.blocked,
                    'pincode':address.pincode,
                    'city':address.city
                    
                }
                result.append(response)
        return make_response(jsonify(result), 200)
    
    


class ProfessionalBasedOnService(Resource):
    @auth_token_required
    def get(self, service_name, id):
        result = []
        customer = Customer.query.filter_by(id=id).first()

        customer_city = customer.addresses[0].city

        service = Service.query.filter_by(name=service_name).first()
        for professional in service.professionals:
            address = Address.query.filter(
                and_(
                    Address.user_id == professional.id,
                    Address.city.ilike(f"%{customer_city}%")  # Partial match for city
                )
            ).first()
            
            if address:
                response = {
                    'id': professional.id,
                    'name': professional.name,
                    'email': professional.email,
                    'active': professional.active,
                    'city': address.city,
                    'pincode': address.pincode,
                    'blocked': professional.blocked,
                    'description': professional.description,
                    'experience': professional.experience,
                    'avg_rating':professional.avg_rating
                }
                result.append(response)
        
        return make_response(jsonify(result), 200)

        
    
class Unapproved_Professionals(Resource):
    @auth_token_required
    def get(self):
        users = User.query.all()
        result = []
        for i in users:
            if any(role.name == 'professional' for role in i.roles) and not i.active:
                service = Service.query.filter_by(id=i.service_id).first()
                service_name = service.name if service else 'N/A'
                address=Address.query.filter_by(user_id=i.id).first()
                
                response = {
                    'id':i.id,
                    'name': i.name,
                    'email': i.email,
                    'description': i.description,
                    'active': i.active,
                    'service': service_name,
                    'blocked':i.blocked,
                    'experience': i.experience,
                    'city':address.city
                }
                result.append(response)
        if not result:
            return make_response(jsonify([]), 200) 

        return make_response(jsonify(result), 200)


class CustomersInputBased(Resource):
    @auth_token_required 
    def get(self):
       
        name = request.args.get('name')
        city = request.args.get('city')
        query = Customer.query.options(joinedload(Customer.addresses))
        if not name and not city:
            return make_response(jsonify([]), 200)
        if name and city:
            query = query.join(Address).filter(
                and_(
                    Customer.name.ilike(f"%{name}%"),
                    Address.city.ilike(f"%{city}%")
                )
            )
        elif name:
            query = query.filter(Customer.name.ilike(f"%{name}%"))
        elif city:
            query = query.join(Address).filter(Address.city.ilike(f"%{city}%"))

        # Fetch the results
        customers = query.all()
        if not customers:
            return make_response(jsonify([]), 200)

        # Format the response data
        result = [
            {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'active': customer.active,
                'city': customer.addresses[0].city if customer.addresses else 'N/A',
                'blocked':customer.blocked
            }
            for customer in customers
        ]

        return make_response(jsonify(result), 200)


class BlockUnblockUser(Resource):
    @auth_token_required
    @roles_required('admin')
    def put(self, id):
        try:
            user  = User.query.filter_by(id=id).first()
            if not user:
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not user.blocked:
               user.blocked = True
               db.session.commit()
               return make_response(jsonify({'message': 'User blocked successfully'}), 200)
            else: 
                user.blocked=False
                db.session.commit()
                return make_response(jsonify({'message': 'User unblocked successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)
        
        

class Professionals_Input_Based(Resource):
    @auth_token_required  
    def get(self):
        name = request.args.get('name')
        service_name = request.args.get('service')
        city = request.args.get('city')
        query = Professional.query.options(joinedload(Professional.addresses)) 
        if not name and not city and not service_name:
            return make_response(jsonify([]), 200)

        if name:
            query = query.filter(Professional.name.ilike(f'%{name}%'))

        if service_name:
            query = query.filter(Professional.service_id.in_(
                db.session.query(Service.id).filter(Service.name.ilike(f'%{service_name}%'))
            ))

        if city:
            query = query.join(Address).filter(Address.city.ilike(f'%{city}%'))

        professionals = query.all()

        if not professionals:
            return make_response(jsonify([]), 200)

        results = [{
            'id': prof.id,
            'name': prof.name,
            'city': prof.addresses[0].city if prof.addresses else None,
            'service': Service.query.filter_by(id=prof.service_id).first().name,  
            'description': prof.description,
            'experience': prof.experience,
            'blocked':prof.blocked,
            'avg_rating':prof.avg_rating
        } for prof in professionals]

        return make_response(jsonify(results), 200)




class ServiceRequestModel(Resource):
    @auth_token_required
    def post(self):
        request_data = request.get_json()
        email = request_data.get('email', None)
        professional_id = request_data.get('professional_id', None)
        remarks = request_data.get('remark', None)
        service_id = request_data.get('service_id', None)

        # Retrieve customer by email
        customer = Customer.query.filter_by(email=email).first()
        if not customer:
            return {'message': 'Customer not found'}, 404

        # Create a new service request
        new_request = ServiceRequest(
            service_id=service_id,
            customer_id=customer.id,
            professional_id=professional_id,
            date_of_request= datetime.now().date(),
            remarks=remarks
        )

        # Add and commit to the database
        db.session.add(new_request)
        db.session.commit()

        return {
            'message': 'Service request created successfully',
            'request_id': new_request.id  
        }, 201  




class ServiceRequestCustomer(Resource):
    @auth_token_required
    def get(self, customer_id):
        requests=ServiceRequest.query.filter_by(customer_id=customer_id).all()
        response=[{
            'professional_id':result.professional_id,
            'id':result.id,
            'customer_id':result.customer_id,
            'professional':Professional.query.filter_by(id=result.professional_id).first().name,
            'service':Service.query.filter_by(id=result.service_id).first().name,
            'status':result.status,
            'date_of_request':result.date_of_request,
            'remarks':result.remarks,
            'reviewed':result.reviewed,
            
        } for result in requests]
        
        return make_response(jsonify(response), 200)
    
    
class CloseRequest(Resource):
    @auth_token_required
    def put(self, id):
        try:
            request  = ServiceRequest.query.filter_by(id=id).first()
            if not request:
                return make_response(jsonify({'message': 'request not found'}), 404)
            
            request.status="closed_c"
            request.date_of_completion=datetime.now().date()
            
            db.session.commit()
            return make_response(jsonify({'message': 'request approved successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)
        

class CreateReview(Resource):
    def post(self):
        data=request.get_json()
        professional_id = data.get('professional_id', None)
        customer_id = data.get('customer_id', None)
        service_request_id = data.get('service_request_id', None)
        rating=data.get('rating')
        comment=data.get('comment')
        
        service_request=ServiceRequest.query.filter_by(id=service_request_id).first()
        service_request.reviewed=True
        
        professional=Professional.query.filter_by(id=professional_id).first()
        professional.avg_rating=(professional.avg_rating*professional.total_ratings+rating)/(professional.total_ratings+1)
        professional.total_ratings+=1
        review=Review(professional_id=professional_id, 
                      customer_id=customer_id, 
                      service_request_id=service_request_id, 
                      rating=rating,
                      comment=comment,
                      date =datetime.now().date()
                      )
        db.session.add(review)
        db.session.commit()
        
        return {
            'message': 'Service review created successfully'
        }, 201  
        
        
class AllServiceRequests(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        requests=ServiceRequest.query.all()
        result=[]
        if requests==[]:
            return make_response(jsonify(result), 200)
        for i in requests:
            sn='DeletedService'
            service=Service.query.filter_by(id=i.service_id).first()
            if service:
                sn=service.name
            response={
                'id':i.id,
                'service':sn,
                'professional':Professional.query.filter_by(id=i.professional_id).first().name,
                'customer':Customer.query.filter_by(id=i.customer_id).first().name,
                'date_of_request':i.date_of_request,
                'date_of_completion':i.date_of_completion,
                'status':i.status,
                
            }
            result.append(response)
            
        return make_response(jsonify(result), 200)
            
            
class StatusBasedServiceRequests(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self, status):
        if status=='closed':
            requests = ServiceRequest.query.filter((ServiceRequest.status == 'closed_p') | (ServiceRequest.status == 'closed_c')).all()

        else:
            requests=ServiceRequest.query.filter_by(status=status).all()
        result=[]
        for i in requests:
            response={
                'id':i.id,
                'service':Service.query.filter_by(id=i.service_id).first().name,
                'professional':Professional.query.filter_by(id=i.professional_id).first().name,
                'customer':Customer.query.filter_by(id=i.customer_id).first().name,
                'date_of_request':i.date_of_request,
                'date_of_completion':i.date_of_completion,
                'status':i.status,
                
            }
            result.append(response)
            
        return make_response(jsonify(result), 200)
    

class ProfessionalsNear(Resource):
    @auth_token_required
    def get(self, id): 
        customer = Customer.query.filter_by(id=id).first()
        city = customer.addresses[0].city

        professionals = Professional.query.filter(
            Professional.addresses.any(Address.city.ilike(f"%{city}%")),
            Professional.blocked == False
        ).all()

        if not professionals:
            return make_response(jsonify([]), 200)

       
        result = []
        for professional in professionals:
            response = {
                'id': professional.id,
                'name': professional.name,
                'city': professional.addresses[0].city if professional.addresses else None,
                'service':  Service.query.filter_by(id=professional.service_id).first().name,
                'description': professional.description,
                'experience': professional.experience,
                'service_id':professional.service_id,
                'avg_rating':professional.avg_rating
            }
            result.append(response)


        return make_response(jsonify(result), 200)


class RequestedServiceRequest(Resource):
    @auth_token_required
    def get(self, id):
        requests=ServiceRequest.query.filter_by(professional_id=id).filter_by(status='requested').all()
        result=[]
        for i in requests:
            customer=Customer.query.filter_by(id=i.customer_id).first()
            address=customer.addresses[0]
            response={
                'id':i.id,
                'customer':customer.name,
                'date_of_request':i.date_of_request,
                'address_line':address.address_line,
                'city':address.city,
                'pincode':address.pincode,
                'email':customer.email
            }
            result.append(response)
        return make_response(jsonify(result), 200)


class AcceptRequest(Resource):
    @auth_token_required
    @roles_required('professional')
    def put(self, id):
        try:
            request  = ServiceRequest.query.filter_by(id=id).first()
            
            request.status = 'accepted'
            db.session.commit()
            return make_response(jsonify({'message': 'request accepted successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)
        
class RejectRequest(Resource):
    @auth_token_required
    @roles_required('professional')
    def put(self, id):
        try:
            request  = ServiceRequest.query.filter_by(id=id).first()
            
            request.status = 'rejected'
            db.session.commit()
            return make_response(jsonify({'message': 'request rejected successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)
    
    
