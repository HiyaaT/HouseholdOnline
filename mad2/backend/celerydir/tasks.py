from celery import shared_task
import time
from applications.models import ServiceRequest, Service
import flask_excel
from celerydir.mail_service import send_email

@shared_task(bind = True, ignore_result=False)
def create_csv(self):
    resource=ServiceRequest.query.filter_by(status='closed_p').all()
    task_id = self.request.id
    filename = f'closed_by_professional_{task_id}.csv'
    column_names=[column.name for column in ServiceRequest.__table__.columns]
    csv_out=flask_excel.make_response_from_query_sets(resource, column_names=column_names, file_type='csv')
    with open(f'./celerydir/user-downloads/{filename}', 'wb') as file:


        file.write(csv_out.data)
    return filename

@shared_task(ignore_result = True)
def email_reminder(to, subject, content):
    send_email(to, subject, content)
    
    
    
