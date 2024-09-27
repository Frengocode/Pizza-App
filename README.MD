# 🚀 Pizza App - Order System 

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FCA121?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![WebSockets](https://img.shields.io/badge/WebSockets-000000?style=for-the-badge&logo=websocket)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://swagger.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-3776AB?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/latest/)

Pizza Apps or Order System Yes, you can call it whatever you want. This app is most similar to an ordering system, What you can do: You can create a product, delete, change, get a product, get all products, you can get products by its category For example, I want to Get All National Products, and you can add products to the Cart and you can remove products from the cart. And now the most important thing is the Order Creation System. How it works you order a product after you order the product you will receive the order status, there are 3 statuses, 1 status is Pending, 2 status in progress is when the order has already been accepted 3 status Ready after the order status is ready then you can pick up your order, you go to the cashier and say that your order was ready and would like to pick up the order,  You pay for the order and the cashier changes the status to Paid and after that the order is closed, but in the future you can see all your orders 


## 📚 Features

- **User Authentication & Authorization**: Secure login, signup, and JWT-based token management.
- **Real-time Notifications.
- **Responsive Design**: Designed to work seamlessly across devices.
- **Efficient Database Management**: Utilizing PostgreSQL with SQLAlchemy ORM and Alembic for migrations.
  
## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance framework for building APIs.
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Powerful, open-source object-relational database.
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper.
- **Real-time Communication**: WebSocket for handling real-time notifications and updates.

## 🖥️ Installation

### Prerequisites

Ensure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started) (for containerization)
- [PostgreSQL](https://www.postgresql.org/download/) (for database management)

### Clone the Repository and You need to specify DATABASE_URL in config/database.py 

```bash
git clone https://github.com/Frengocode/Pizza-App.git
cd Meno

python -m venv venv
./v + Tab/s + Tab/ a + Tab for Liniux Mack sourse/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload

DATABASE_URL  = postgresql://username:password@localohost/Meno
