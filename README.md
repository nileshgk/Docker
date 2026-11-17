<<<<<<< HEAD

# Deploying Multi-Tier Application Using Docker Compose

## 1. Project Overview

This project demonstrates how to deploy a multi-tier application
using Docker and Docker Compose on an AWS Ubuntu EC2 instance.

The application contains three tiers:

1. Presentation Tier - Nginx frontend
2. Application Tier - Python FastAPI backend
3. Database Tier - MySQL database

## 2. Architecture

User Browser
     |
     | Port 8080
     v
Nginx Frontend Container
     |
     | API requests - Port 5000
     v
Python FastAPI Backend Container
     |
     | MySQL - Port 3306
     v
MySQL Database Container

All containers communicate through a private Docker network.

## 3. Technologies Used

- AWS EC2
- Ubuntu 24.04
- Docker
- Docker Compose
- Nginx
- Python
- FastAPI
- MySQL
- Git

## 4. Project Structure

multi-tier-docker-compose/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── frontend/
├── backend/
├── scripts/
└── README.md

## 5. AWS Infrastructure

We will use one Ubuntu EC2 instance.

Required inbound access:

- SSH: Port 22 - restrict to your own IP
- Frontend: Port 8080 - restrict to your own IP during testing
- Backend: Port 5000 - restrict to your own IP during testing

Do not expose MySQL port 3306 publicly.

Check your AWS account's Free Tier or Free Plan eligibility
before launching resources. Charges may apply depending on
account eligibility, usage, region, storage, and data transfer.

## 6. Install Docker

Connect to the EC2 instance using SSH.

Run:

chmod +x scripts/install-docker-ubuntu.sh

sudo ./scripts/install-docker-ubuntu.sh

Verify:

sudo docker --version
sudo docker compose version

## 7. Configure Environment Variables

Copy the example environment file:

cp .env.example .env

Edit the file:

nano .env

Replace the example passwords with strong unique passwords.

## 8. Configure Frontend

Edit:

nano frontend/config.js

Replace YOUR_EC2_PUBLIC_IP with the EC2 public IPv4 address.

Example:

const API_BASE_URL = "http://YOUR_PUBLIC_IP:5000";

## 9. Deploy the Application

Validate Docker Compose configuration:

sudo docker compose config

Build and start the containers:

sudo docker compose up -d --build

Check running containers:

sudo docker compose ps

View logs:

sudo docker compose logs -f

## 10. Verify Application

Open the frontend in a browser:

http://YOUR_EC2_PUBLIC_IP:8080

Test backend health:

curl http://localhost:5000/health

Test frontend:

curl http://localhost:8080

Save a message using the frontend and refresh the messages
to verify that data is stored in MySQL.

## 11. Troubleshooting

Check container status:

sudo docker compose ps

Check frontend logs:

sudo docker compose logs frontend

Check backend logs:

sudo docker compose logs backend

Check database logs:

sudo docker compose logs database

Restart services:

sudo docker compose restart

## 12. Cleanup

Stop containers:

sudo docker compose down

Remove containers and database volume:

sudo docker compose down -v

Warning: The -v option deletes the database's persistent data.

Terminate the EC2 instance when the project is finished
and remove any other resources you created.

## 13. Security Considerations

- Do not commit the .env file to Git.
- Use strong database passwords.
- Restrict SSH access to your own IP.
- Keep MySQL inside the private Docker network.
- Restrict CORS to the frontend origin in production.
- Use HTTPS and proper secret management for production.
- Avoid exposing the backend API publicly unless required.
=======
# Docker
Docker related mini projects
>>>>>>> 140b806cea5f7fc8a4f0b550e81c327ee382d24c
