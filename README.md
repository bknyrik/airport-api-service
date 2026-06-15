# Airport Api Service
___
## Description
This project allows you track flights between airports, order tickets to these flights, manage users and more. 

DB structure:

![DB structure](documentation/airport_api_service.drawio.png)

BrowsableAPI pages:

Facility list:
![Facility list page](documentation/facility_list.png)

Facility detail:
![Facility detail page](documentation/facility_detail.png)

Airplane type list:
![Airplane type list page](documentation/airplane_type_list.png)

Airplane type detail:
![Airplane type detail page](documentation/airplane_type_detail.png)

Airplane list:
![Airplane list page](documentation/airplane_list.png)

Airplane detail:
![Airplane detail page](documentation/airplane_detail.png)

Airplane upload image:
![Airplane upload image page](documentation/airplane_upload_image.png)

Airport list:
![Airport list page](documentation/airport_list.png)

Airport detail:
![Airport detail page](documentation/airport_detail.png)

Airport upload image:
![Airport upload image page](documentation/airport_upload_image.png)

Crew list:
![Crew list page](documentation/crew_list.png)

Crew detail:
![Crew detail page](documentation/crew_detail.png)

Route list:
![Route list page](documentation/route_list.png)

Route detail:
![Route detail page](documentation/route_detail.png)

Flight list:
![Route list page](documentation/flight_list.png)

Flight detail:
![Flight detail page](documentation/flight_detail.png)

Order list:
![Order list page](documentation/order_list.png)

Order detail:
![Order detail page](documentation/order_detail.png)

User register:
![User register page](documentation/user_register.png)

User manage:
![User manage page](documentation/user_manage.png)

User list:
![User list page](documentation/user_list.png)

User detail:
![User detail page](documentation/user_detail.png)

Token obtain pair:
![Token obtain pair page](documentation/token_obtain.png)

Token refresh:
![Token refresh page](documentation/token_refresh.png)

Token verify:
![Token verify page](documentation/token_verify.png)

## Features
___
- JWT Authentication
- Documentation at `/api/schema/swagger-ui/` and `/api/schema/redoc/`
- Managing orders and tickets
- Creating airplanes with airplane types and facilities
- Creating flights with routes, airports and crewmembers
- Filtering airplanes, airports, routes, flights, crewmembers and users
- Creating and managing users

## Installation
___
1. Clone the repository - `git clone https://github.com/bknyrik/airport-api-service.git`;
2. Create the virtual environment - `python -m venv .venv`;
3. Activate the virtual environment:
    - Windows - `airport-api-service\Scripts\activate`;
    - macOS/Linux - `source airport-api-service/bin/activate`.
4. Install all dependencies - `pip install -r requirements.txt`
5. Add `.env` file according to the `.env.sample` template. Note: If you are going to launch project in the Docker container,
set `POSTGRES_HOST=database`;
6. Apply all migrations - `python manage.py migrate`;

## Usage
___
### Run locally
___
Run the server `python manage.py runserver`.
### Run with Docker
___
1. Build services - `docker-compose build`;
2. Create and start containers - `docker-compose up -d`.

Visit `http://127.0.0.1:8000/` in your browser to use the application. \
And also don't forget to create a superuser:
```python manage.py createsuperuser```.

NOTE: If you are running project in the Docker container, create superuser inside the container.

## Getting access
___
- register user via `/api/users/register/`
- manage user via `/api/users/me/`
- list with users via `api/users/accounts/`
- get user by `pk` via `/api/users/accounts/{pk}/`
- obtain access and refresh token via `api/auth/token/obtain/`
- refresh access token via `api/auth/token/refresh/`
- verify token via `api/auth/token/verify`
- get list with airplane types via `api/airport/airplane_types/`
- get airplane type by `pk` via `api/airport/airplane_types/{pk}/`
- get list with facilities via `api/airport/facilities/`
- get facility by `pk` via `api/airport/facilities/{pk}/`
- get list with airplanes via `api/airport/airplanes/`
- get airplane by `pk` via `api/airport/airplanes/{pk}/`
- upload an image to airplane by `pk` via `api/airport/airplanes/{pk}/`
- get list with airports via `api/airport/airports/`
- get airport by `pk` via `api/airport/airports/{pk}/`
- upload an image to airport by `pk` via `api/airport/airports/{pk}/`
- get list with routes via `api/airport/routes/`
- get route by `pk` via `api/airport/routes/{pk}/`
- get list with crewmembers via `api/airport/crewmembers/`
- get crew by `pk` via `api/airport/crewmembers/{pk}/`
- get list with flights via `api/airport/flights/`
- get flight by `pk` via `api/airport/flights/{pk}/`
- get list with orders via `api/airport/orders/`
- get order by `pk` via `api/airport/orders/{pk}/`

## Contact
Email: knyrikkolesnichenko2004@gmail.com
