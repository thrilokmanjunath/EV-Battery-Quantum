# EV Battery Quantum Optimization Architecture

## Overview
The architecture is designed for web scalability, utilizing a microservices approach with asynchronous task processing.

## Components
1. **Frontend**: A web application serving the user interface (Node.js based).
2. **API (Backend)**: The core service exposing RESTful endpoints.
3. **Database (PostgreSQL)**: Persistent storage for user data, battery configurations, and historical optimization results.
4. **Task Queue/Cache (Redis)**: Acts as a message broker for Celery and caching layer for fast data retrieval.
5. **Background Workers (Celery)**: Dedicated workers to execute computationally heavy Quantum (QAOA) and Evolutionary (NSGA-II) algorithms.

## Flow
1. User submits an optimization request via the **Frontend**.
2. **Frontend** makes a REST API call (`POST /optimize`) to the **API**.
3. **API** validates the request, saves a pending record to the **Database**, and queues a task in **Redis**.
4. The **API** immediately returns a `task_id` and a `202 Accepted` response.
5. A **Background Worker** picks up the task from **Redis** and executes `run_optimization_task()`.
6. Upon completion, the worker updates the **Database** with the result.
7. **Frontend** polls the API (`GET /optimize/{task_id}`) or receives a WebSocket notification to retrieve the final result.
