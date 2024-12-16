from celery.schedules import crontab
import csv  
from flask import current_app as app, render_template
from celerydir.tasks import email_reminder
from applications.models import Professional, ServiceRequest, Customer
from datetime import date, timedelta
from celerydir.mail_service import send_email
from datetime import datetime
from applications.database import db
import os

celery_app = app.extensions['celery']

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Setup periodic tasks using Celery Beat.
    """
    # Daily reminders for professionals
    sender.add_periodic_task(
        crontab(hour=17, minute=14),
        send_daily_reminders.s(),
        name='Send daily reminders to professionals',
    )

    # Monthly report task for customers on the 19th of each month
    sender.add_periodic_task(
        crontab(hour=17, minute=28, day_of_month=8),
        send_monthly_reports.s(),
        name='Send monthly reports to customers',
    )

@celery_app.task(ignore_result=True)
def send_daily_reminders():
    """
    Task to check pending service requests and send reminders to professionals via email.
    """
    from applications.database import db 
    professionals = (
        db.session.query(Professional)
        .join(ServiceRequest, Professional.id == ServiceRequest.professional_id)
        .filter(ServiceRequest.status == "requested")
        .distinct()
        .all()
    )

    for professional in professionals:
        
        pending_count = db.session.query(ServiceRequest).filter_by(
            professional_id=professional.id,
            status="requested"
        ).count()

        subject = "Daily Reminder: accept/reject your pending Service Requests"
        body = (
            f"Hello {professional.name},<br><br>"
            f"You have <b>{pending_count}</b> pending service request(s). "
            "Please visit the portal to review and take necessary actions.<br><br>"
            "Best Regards,<br>Service Team"
        )

        if professional.email:
            email_reminder.delay(professional.email, subject, body)

    print("Daily reminders sent successfully!")


@celery_app.task(ignore_result=True)
def send_monthly_reports():
    """
    Task to generate and send monthly activity reports to customers via email.
    """
    from applications.database import db  
    today = date.today()
    current_month_8th = today.replace(day=8)
    last_month_8th = (current_month_8th - timedelta(days=30)).replace(day=8)

   
    customers = Customer.query.all()

    for customer in customers:
        
        services = ServiceRequest.query.filter(
            ServiceRequest.customer_id == customer.id,
            ServiceRequest.date_of_request >= last_month_8th,
            ServiceRequest.date_of_request <= current_month_8th, 
        ).all()

    
        total_requests = len(services)
        total_completed = len([s for s in services if s.status == "closed_p" or s.status=="closed_c"])

       
        report_content = render_template(
            "customer_mail.html",
            customer=customer,
            services=services,
            total_requests=total_requests,
            total_completed=total_completed,
            month_range=f"{last_month_8th.strftime('%d %b %Y')} - {current_month_8th.strftime('%d %b %Y')}",
        )

       
        if customer.email:
            subject = f"Monthly Activity Report: {last_month_8th.strftime('%d %b %Y')} - {current_month_8th.strftime('%d %b %Y')}"
            email_reminder.delay(customer.email, subject, report_content)

    print(f"Monthly reports from {last_month_8th.strftime('%d %b %Y')} to {current_month_8th.strftime('%d %b %Y')} sent successfully!")




