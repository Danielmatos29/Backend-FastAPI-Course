# Python & FastAPI Backend Development

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb)

A comprehensive backend repository demonstrating fundamental to intermediate web development concepts using Python and FastAPI. Built following the curriculum by [@MoureDev](https://github.com/mouredev).

---

## Key Features & Architecture

- **RESTful API Design:** Implemented full CRUD routing across modular resources using standard HTTP methods.
- **Type Safety & Validation:** Leveraged Pydantic models and Python type hints for payload parsing and automatic request validation.
- **Authentication & Security:** Built token-based authentication flows using **OAuth2 Password Bearer** and **JWT (JSON Web Tokens)** with password hashing (`passlib`/`bcrypt`).
- **Database Integration:** Asynchronous and synchronous data handling using **MongoDB** with **PyMongo** / **Motor** and MongoDB Atlas cloud storage.
- **API Structuring:** Organised scalable application routes using `APIRouter` to maintain separation of concerns.

---

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI, Uvicorn (ASGI server)
- **Database:** MongoDB, MongoDB Atlas
- **Authentication:** OAuth2, JWT, Passlib
- **Data Validation:** Pydantic

---

## Project Structure

```text
├── routers/          # API route definitions (users, auth, products)
├── db/               # Database connection setups & models
│   ├── client.py     # MongoDB connection client
│   └── models/       # Pydantic schemas and database models
├── main.py           # Application entrypoint & global configs
├── requirements.txt  # Project dependencies
└── README.md