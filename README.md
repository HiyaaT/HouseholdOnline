# HouseholdOnline
This project is made using vue cli for frontend, python flask for backend api, slite3 for database, sqlAlchemy as orm, with token based authentication via flask security.

 Celery and redis for csv export and parallel task scheduling.

# Architecture and Features
•	Controller admin: consists of admin dashboard, search, create service and summary of user and request status. Admin can create, update and delete a service. It can view user profile and approve a professional and can block or unblock a user. It can search based on customer, professional and service.
•	Controller user customer: a customer dashboard consists of service containers, when clicked gives professional details in its city, customer can book a same service again only if the request to the service is not in requested status. If a customer closes a request, it is automatically given a pop up to review it, else if closed by the professional in the request history section it can review it. If can edit or delete a requested service request. It can search a professional based on his name/ city/ service or professional near it based on city.
•	Controller user professional: professional can accept reject a service, it can close a service. It has a profile section where it can update its address.
•	Register/Login: Login is role based, when a user logins, its credential details such as name, role and id is stored in local storage. Once on successful login, redirects to their respective home page. Admin is automatically created when project launched for first time. In registration of user, if clicked on professional, a modal pops up taking input for additional professional details.
