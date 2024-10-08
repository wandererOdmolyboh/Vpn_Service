﻿# Vpn_Service

## Introduction

This project is a simple VPN service implemented using Django. The service provides a web interface where users can register, access a personal account, manage personal data, and use a VPN to visit websites anonymously.
## Technologies

- Python
- Django
- PostgreSQL


## Installation

This project uses Docker. To run the project, follow these steps:

1. Create the environment in `.env`. Yoc can start local or by docker-compose. For local start use `HOST=localhost`:
```ini
NAME=vpn
USER=root
PASSWORD=root
# HOST=localhost # for local start or use docker-compose
HOST postgres
PORT=5432
```

2. Use docker-compose. For local start use `HOST=postgres`:
```shell
docker-compose up 
```
## Endpoints
Here are the endpoints for your Django application:  
1. [Registration](http://localhost:8000/register/) \
Method: POST
Description: Register a new user.
Body: User data (username, password, etc.)
2. [Profile](http://localhost:8000/profile/) \
Method: GET, PUT
Description: View and update the profile of the logged-in user.
3. [User Sites](http://localhost:8000/user_sites/) \
Method: GET, POST
Description: View and create sites for the logged-in user.
4. [Statistics](http://localhost:8000/statistics/) \
Method: GET
Description: View VPN usage statistics for the logged-in user.
5. [Create Site](http://localhost:8000/create_site/) \
Method: GET, POST
Description: Create a new site for the logged-in user.
6. [Site List](http://localhost:8000/site_list/) \
Method: GET
Description: View a list of sites for the logged-in user.
7. [Proxy View](http://localhost:8000/proxy_view/)  
/proxy_view/<site_name>/<path>/  
Method: GET
Description: Use the VPN to visit a site.

