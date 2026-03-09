# Weather API Platform
### COMP3011 — Web Services and Web Data - Coursework 1

A data-driven weather analytics platform built with **FastAPI**, **PostgreSQL**, and **Next.js**.

The system collects weather observations, stores them in a database, and provides analytics endpoints for temperature, humidity and temperature trends.  
A web dashboard allows users to explore weather data interactively.

---

# Project Overview

This project demonstrates the design and implementation of a **RESTful Web API with database integration and analytics capabilities**.

Main capabilities include:

- Location management (CRUD)
- Weather observations storage
- Featured locations dashboard
- Analytics (temperature and humidity)
- Temperature trend visualisation
- Web dashboard interface

Weather data is collected from the **OpenWeatherMap API**.

---

# Technology Stack

## Backend

- FastAPI
- SQLModel
- Pydantic
- PostgreSQL
- Alembic (database migrations)

Architecture:

- Domain-Driven Design (DDD inspired)
- Bounded Contexts

## Frontend

- Next.js
- TypeScript
- React
- Feature-based architecture

## Data Source

- OpenWeatherMap API

---

# System Architecture

The system consists of a backend API and a frontend dashboard.

```
Frontend (Next.js)
    │
    │ REST API
    ▼
Backend (FastAPI)
    │
    │ SQLModel ORM
    ▼
PostgreSQL Database
```


The frontend consumes REST endpoints provided by the backend to display analytics and weather insights.

---

# Architecture (DDD)

The backend follows a **Domain-Driven Design (DDD) inspired architecture**.

## Bounded Contexts

Each domain is organised as a **bounded context** located in:

`backend/src/contexts/`

Current contexts include:

- locations
- observations
- analytics


## Layered Structure

Each context follows a layered architecture:

- **domain**  
  Core business entities and domain logic.

- **app (application layer)**  
  Application services and use cases that coordinate domain logic.

- **infra (infrastructure layer)**  
  Database access, repository implementations, and external API integrations.

- **api (interface layer)**  
  FastAPI routers, request/response schemas, and HTTP endpoints.


## Dependency Rule

Dependencies follow a one-direction rule:
```
api → app → domain  
infra → domain
```

Meaning:

- The **API layer** calls application services.
- The **application layer** orchestrates domain logic.
- The **domain layer** contains the core business rules.
- The **infrastructure layer** implements technical details such as database access.

---

# Project Structure

## Backend Structure

The backend follows a **DDD-inspired architecture organised around bounded contexts**.

```
backend/
├ src/
│ ├ main.py
│ ├ api/
│ │ └ router.py
│ ├ contexts/
│ │ ├ locations/
│ │ ├ observations/
│ │ └ analytics/
│ └ shared/
└ migrations/
```

### contexts

Each context represents a domain module.

- **locations** – manages tracked cities
- **observations** – stores weather observation data
- **analytics** – computes aggregated statistics and trends

Each context typically contains:

- api – FastAPI routers and request/response schemas
- app – application services (use cases)
- domain – entities and repository interfaces
- infra – database access and external API clients

### api (Composition Layer)

The `src/api` directory assembles routers from each context and registers them with FastAPI.

It contains no business logic.

### shared

Contains infrastructure shared across contexts:

- database session
- configuration
- error handling
- pagination utilities

---

## Frontend Structure

The frontend uses a **feature-based architecture**.

```
frontend/
├ app/
│ ├ layout.tsx
│ └ page.tsx
│
└ src/
  ├ features/
  │ ├ home/
  │ ├ locations/
  │ └ analytics/
  │
  └ shared/
```
  
### features

Each feature contains UI components and API functions related to a specific functionality.

Examples:

- **home** – dashboard UI and featured weather display
- **locations** – location management interface
- **analytics** – charts and analytical visualisations

### shared

Contains reusable utilities such as the API client wrapper.

---

# Prerequisites

To run this project locally, ensure the following tools are installed:

- Python 3.10+
- Node.js (LTS)
- PostgreSQL
- npm
- Git

### Tested Environment

Python 3.11  
Node.js 20  
PostgreSQL 15  
Windows 11

---

# Running the Project

## Backend Setup

``` bash
cd backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

copy .env.example .env

uvicorn src.main:app --reload
```

Backend API: `http://localhost:8000`

Swagger API documentation: `http://localhost:8000/docs`


---

## Frontend Setup

The frontend project was bootstrapped using:

``` bash
npx create-next-app frontend
```

To run the frontend:

``` bash
cd frontend

npm install
npm run dev
```

Open the Home dashboard: `http://localhost:3000`


---

# Database Setup

Example `.env` configuration:
``` bash
DATABASE_URL=postgresql://username:password@localhost:5432/comp3011_cw1
```

Run database migrations:

``` bash
alembic upgrade head
```


---

# API Endpoints


Base URL: `http://localhost:8000`


For a detailed specification of all endpoints, parameters, and example responses:

📄 **API Documentation**  : [API Documents (PDF)](docs/API_documents.pdf)



## Locations

| Method | Endpoint | Description |
|------|------|------|
| GET | /locations | Retrieve all locations |
| POST | /locations | Create location |
| PATCH | /locations/{id} | Partially update location |
| DELETE | /locations/{id} | Soft delete location |

## Observations

| Method | Endpoint | Description |
|------|------|------|
| GET | /observations | Retrieve observations |
| POST | /observations | Store observation data |
| GET | /observations/location/{id} | Observations by location |

## Analytics

| Method | Endpoint | Description |
|------|------|------|
| GET | /analytics/temperature | Average temperature |
| GET | /analytics/humidity | Average humidity |
| GET | /analytics/trend/{location_id} | Temperature trend |

---

# Example API Responses

### GET /locations

```json
[
  {
    "id": 1,
    "name": "London",
    "country": "GB",
    "is_featured": true,
    "is_active": true
  },
  {
    "id": 2,
    "name": "Seoul",
    "country": "KR",
    "is_featured": false,
    "is_active": true
  }
]
```

### GET /analytics/trend/1

``` json
{
  "location": "London",
  "trend": [
    {"date": "2026-02-25", "temperature": 12.3},
    {"date": "2026-02-26", "temperature": 13.1},
    {"date": "2026-02-27", "temperature": 14.0}
  ]
}
```

# Dashboard(home)  Screenshots


## Featured Location Panel and Location Dashboard

<p align="center">
<img src="docs/Screenshots/HomeDashboard.png" width="700">
</p>

Displays featured locations (Max 2 locations) and weather summaries. (`is_featured=true`)

Location search and addition

Displays active locations (`is_active=true`)


## Analytics Panel

<p align="center">
<img src="docs/Screenshots/AnalyticsPanel.png" width="700">
</p>


Shows temperature and humidity analytics.

Displays temperature trends over time.


## Version Control

Development follows a feature branch workflow.


## Generative AI Usage

Generative AI tools were used during development for:

* architecture exploration
* debugging support
* documentation drafting

Tools used:
* ChatGPT
* GitHub Copilot


## Data Source

Weather data provided by:

OpenWeatherMap API : `https://openweathermap.org/api`


## License

This project was developed for academic purposes as part of:

COMP3011 — Web Services and Web Data

University of Leeds


## Notes
- Don't commit `.env`, `venv/`, `node_modules/`, or PostgreSQL data directories.