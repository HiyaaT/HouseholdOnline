from flask_restful import Resource
from flask import jsonify, request, make_response, current_app as app
from applications.database import db
from applications.models import *
from flask_security import auth_token_required,roles_required
from datetime import datetime
from sqlalchemy import or_
cache = app.cache

class ClosedRequest(Resource):
    @auth_token_required
    @cache.memoize(timeout = 5)
    @roles_required('professional')
    def get(self, id):
        review=Review.query.filter_by(professional_id=id).all()
        
        result=[]
        
        for i in review:
            customer=Customer.query.filter_by(id=i.customer_id).first()
            address=customer.addresses[0]
            
            response={
                'id':i.id,
                'customer':customer.name,
                'address_line':address.address_line,
                'date_of_review':i.date,
                'city':address.city,
                'pincode':address.pincode,
                'rating':i.rating,
                'comment':i.comment
            }
            
            result.append(response)
        return make_response(jsonify(result), 200)
    
class Profile(Resource):
    @auth_token_required
    @cache.memoize(timeout = 5)
    def get(self, id):
        p=User.query.filter_by(id=id).first()
        address=p.addresses[0]
        
        if p.roles[0]=='professional':
            sn=None
            service=Service.query.filter_by(id=p.service_id).first()
            if service:
                sn=service.name
            
            response={
            'name':p.name,
            'email':p.email,
            'description':p.description,
            'experience':p.experience,
            'service':sn,
            'avg_rating':p.avg_rating,
            'total_ratings':p.total_ratings,
            'address_line':address.address_line,
            'city':address.city,
            'state':address.state,
            'pincode':address.pincode
            }
        else:
            response={
            'name':p.name,
            'email':p.email,
            'address_line':address.address_line,
            'city':address.city,
            'state':address.state,
            'pincode':address.pincode
                
            }
        return make_response(jsonify(response), 200)
    
class UserAddress(Resource):
    
    @auth_token_required
    @cache.memoize(timeout = 60)
    def get(self, id):
        address=Address.query.filter_by(user_id=id).first()
        address_data = {
            "id":address.id,
            "address_line": address.address_line,
            "city": address.city,
            "state": address.state,
            "pincode": address.pincode
        }
        return make_response(jsonify(address_data), 200)
    
    
    def put(self, id):
        data = request.get_json()
        cache.delete(f"address_{id}")
        address = Address.query.filter_by(id=id).first()
        if address:
            address.address_line = data['address_line']
            address.city = data['city']
            address.state = data['state']
            address.pincode = data['pincode']
            db.session.commit()
            cache.set(f"address_{id}", address)
            return jsonify({'message': 'Address updated successfully'})
        return jsonify({'error': 'Address not found'}), 404
    
    
    
class UserDictionary(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        p=Professional.query.count()
        c=Customer.query.count()
        
        response={
            'label':['professional','customer'],
            'data':[p, c]
        }
        
        return make_response(jsonify(response), 200)
    
class ServiceRequestStatusCount(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        accepted=ServiceRequest.query.filter_by(status='accepted').count()
        requested=ServiceRequest.query.filter_by(status='requested').count()
        rejected=ServiceRequest.query.filter_by(status='rejected').count()
        closed = ServiceRequest.query.filter(
    or_(ServiceRequest.status == 'closed_p', ServiceRequest.status == 'closed_c')
).count()
        
        response={
            'label':['accepted','requested','rejected','closed'],
            'data':[accepted, requested, rejected, closed]
        }
        
        return make_response(jsonify(response), 200)
    
    
class ServiceRequestCountProfessional(Resource):
    @auth_token_required
    @roles_required('professional')
    def get(self, id):
        #accepted, rejected, closed
        requests=ServiceRequest.query.filter_by(professional_id=id).all()
        a=0
        r=0
        c=0
        for i in requests:
            if i.status=='accepted': a=a+1
            if i.status=='rejected': r=r+1
            if i.status=='closed_p':c=c+1
            if i.status=='closed_c':c=c+1
        response={
            'label':['accepted/working', 'rejected', 'completed'],
            'data':[a,r,c]
        }
        
        return make_response(jsonify(response), 200)    
    
class RatingSummaryData(Resource):
    @auth_token_required
    @roles_required('professional')
    def get(self, id):
        reviews=Review.query.filter_by(professional_id=id).all()
        d={'good':0, 'decent':0, 'bad':0}
        for i in reviews:
            if i.rating==4 or i.rating==5:
                d['good']+=1
            elif i.rating==3:
                d['decent']+=1
            else:
                d['bad']+=1
        return make_response(jsonify({'label':list(d.keys()), 'data':list(d.values())}), 200)
                
class RequestModification(Resource):
    @auth_token_required
    def put(self, id):
        req=ServiceRequest.query.filter_by(id=id).first()
        data = request.get_json()
        date_of_request=data.get('date_of_request')
        remark=data.get('remark')
        if remark is not None:
            req.remarks=remark
        if date_of_request:
            parsed_date = datetime.strptime(date_of_request, '%Y-%m-%d').date()
            req.date_of_request = parsed_date
        db.session.commit()
        
        return {
            'message': 'edited succesfully'
        }, 201 
        
    @auth_token_required  
    def delete(self, id):
        req = ServiceRequest.query.filter_by(id=id).first()
        db.session.delete(req)
        db.session.commit()
        return {'message': 'Request deleted successfully'}, 200 
    
    
    
class IsBooked(Resource):
    @auth_token_required
    def get(self, c_id, p_id):
        request=ServiceRequest.query.filter_by(customer_id=c_id).filter_by(professional_id=p_id).filter_by(status='requested').first()
        if request:
            return make_response(jsonify({'check':True}), 200)
        
        return make_response(jsonify({'check':False}), 200)
    
class AcceptedRequests(Resource):
    @auth_token_required
    @roles_required('professional')
    def get(self, id):
        review=ServiceRequest.query.filter_by(professional_id=id).filter_by(status='accepted').all()
        
        result=[]
        
        for i in review:
            customer=Customer.query.filter_by(id=i.customer_id).first()
            address=customer.addresses[0]
            
            response={
                'id':i.id,
                'customer':customer.name,
                'email':customer.email,
                'address_line':address.address_line,
                'date_of_request':i.date_of_request,
                'city':address.city,
                'pincode':address.pincode,
            }
            
            result.append(response)
        return make_response(jsonify(result), 200)
    
    
    




class CloseRequestP(Resource):
    @auth_token_required
    def put(self, id):
        try:
            request  = ServiceRequest.query.filter_by(id=id).first()
            if not request:
                return make_response(jsonify({'message': 'request not found'}), 404)
            
            request.status="closed_p"
            request.date_of_completion=datetime.now().date()
            
            db.session.commit()
            return make_response(jsonify({'message': 'request approved successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal Server Error'}), 500)
        

class setServiceforProfessional(Resource):
    def put(self, id):
        data = request.get_json()

        service_id = data.get('service_id')
        p=Professional.query.filter_by(id=id).first()
        p.service_id=service_id
        db.session.commit()
        return make_response(jsonify({'message': 'success'}), 200)