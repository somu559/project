Little Lemon — Restaurant API (Django REST Framework)
=====================================================

API Endpoints
-------------
- /api/menu/
- /api/bookings/
- /api/users/
- /api-token-auth/

Menu detail routes (router): /api/menu/<id>/

Admin: /admin/

User model: Django's built-in django.contrib.auth.models.User (manage users in Admin under Authentication and Authorization).

Setup and run
-------------
1. Create and activate a virtual environment (from project root):

   Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   macOS / Linux:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

   For MySQL on Windows, install mysqlclient separately if the requirement is skipped, or use SQLite (default).

3. Environment (optional):
   - DJANGO_SECRET_KEY   — production secret
   - DJANGO_DEBUG        — false in production
   - DJANGO_ALLOWED_HOSTS — comma-separated hosts
   - USE_MYSQL=1         — switch to MySQL; set MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT

4. Migrate and create superuser:
   python manage.py migrate
   python manage.py createsuperuser

5. Run server:
   python manage.py runserver

Example requests
----------------
Register:
  POST http://127.0.0.1:8000/api/users/
  Content-Type: application/json
  {"username": "alice", "email": "alice@example.com", "password": "yourpassword"}

Obtain token:
  POST http://127.0.0.1:8000/api-token-auth/
  Content-Type: application/json
  {"username": "alice", "password": "yourpassword"}
  Response: {"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}

List menu (public):
  GET http://127.0.0.1:8000/api/menu/

Create menu item (authenticated):
  POST http://127.0.0.1:8000/api/menu/
  Authorization: Token <your-token>
  Content-Type: application/json
  {"title": "Lemon Dessert", "price": "7.50", "inventory": 12}

List bookings (public):
  GET http://127.0.0.1:8000/api/bookings/

Create booking (authenticated):
  POST http://127.0.0.1:8000/api/bookings/
  Authorization: Token <your-token>
  Content-Type: application/json
  {"name": "Bob", "no_of_guests": 4, "booking_date": "2025-04-01T19:30:00Z"}

Query parameters (optional)
---------------------------
- Pagination: ?page=1 (10 items per page by default)
- Menu search: ?search=salad
- Menu ordering: ?ordering=price or ?ordering=-title
- Bookings search/ordering: ?search=..., ?ordering=booking_date

Run tests
---------
  python manage.py test restaurant
