from flask import Flask

from applications.config import Config
from applications.database import db
from applications.models import *
from flask_restful import Api
from flask_security import Security, hash_password
from applications.user_datastore import user_datastore
from create_initial_data import create_data
from flask_cors import CORS
from flask_caching import Cache
import flask_excel as excel
from sqlalchemy import text

from celerydir.celery_factory import celery_init_app


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    api = Api(app, prefix='/api/v1')

    app.security = Security(app, user_datastore)
    cache = Cache(app)
    app.cache = cache
    excel.init_excel(app)

    with app.app_context():
        # Enable foreign key constraints for SQLite
        db.session.execute(text('PRAGMA foreign_keys=ON'))
        db.create_all()
        create_data(app, db)

    return app, api


# Create the app and push the context globally
app, api = create_app()
app.app_context().push()  # Push the context globally

with app.app_context():
    celery_app = celery_init_app(app)
    import celerydir.celery_schedule

# Import routes and APIs
from applications.auth_apis import *
from applications.routes import *
from applications.resource_api import *
from applications.resource_api2 import *

# Add API resources
api.add_resource(Registration, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Services, '/service')
api.add_resource(Professionals, '/professionals')
api.add_resource(ApproveProfessional, '/approve/<int:id>')
api.add_resource(Customers, '/customers')
api.add_resource(ProfessionalBasedOnService, '/profs_service/<string:service_name>/<int:id>')
api.add_resource(ServiceDetail, '/services/<int:id>')
api.add_resource(ValidUser, '/valid_user')
api.add_resource(Unapproved_Professionals, '/unapproved_professionals')
api.add_resource(CustomersInputBased, '/customer_input_based')
api.add_resource(Professionals_Input_Based, '/professional_input_based')
api.add_resource(BlockUnblockUser, '/block_unblock/<int:id>')
api.add_resource(ServiceRequestModel, '/service_request')
api.add_resource(ServiceRequestCustomer, '/servicerequestcustomer/<int:customer_id>')
api.add_resource(CreateReview, '/review')
api.add_resource(CloseRequest, '/closerequest/<int:id>')
api.add_resource(AllServiceRequests, '/allservicerequest')
api.add_resource(StatusBasedServiceRequests, '/statusbasedservicerequests/<string:status>')
api.add_resource(ProfessionalsNear, '/nearprofessionals/<int:id>')
api.add_resource(RequestedServiceRequest, '/requested_request/<int:id>')
api.add_resource(AcceptRequest, '/acceptrequest/<int:id>')
api.add_resource(RejectRequest, '/rejectrequest/<int:id>')
api.add_resource(ClosedRequest, '/closedrequest/<int:id>')
api.add_resource(Profile, '/prof_profile/<int:id>')
api.add_resource(UserAddress, '/get_address/<int:id>')
api.add_resource(UserDictionary, '/user_count')
api.add_resource(ServiceRequestStatusCount, '/status_count')
api.add_resource(RatingSummaryData, '/rating_summary/<int:id>')
api.add_resource(ServiceRequestCountProfessional, '/professional_status_count/<int:id>')
api.add_resource(RequestModification, '/editrequest/<int:id>')
api.add_resource(IsBooked, '/isbooked/<int:c_id>/<int:p_id>')
api.add_resource(AcceptedRequests, '/acceptedrequest/<int:id>')
api.add_resource(CloseRequestP, '/closerequestp/<int:id>')
api.add_resource(setServiceforProfessional,'/setservice/<int:id>')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
