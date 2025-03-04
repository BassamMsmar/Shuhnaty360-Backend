# Shuhnaty 360

**Shuhnaty 360** is a shipment management system that facilitates tracking and managing shipments between factories and warehouses. The system serves as an intermediary between transport company owners, factories, and their customers.

## 🚀 Technologies Used

- **Django** - Backend framework
- **Django REST Framework (DRF)** - API development
- **PostgreSQL/MySQL** - Database (choose based on deployment)
- **Docker** *(optional)* - Containerization
- **Postman** - API documentation & testing

## 📌 Features

- **Shipment Management**: Create, update, and track shipments.
- **Clients & Drivers Management**: Add and manage clients and drivers.
- **QR Code Integration**: Each shipment has a QR code for easy tracking.
- **Infinite Scrolling Pagination**: Load shipments dynamically without reloading pages.
- **Authentication & Permissions**: Secure API endpoints using DRF authentication.

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/BassamMsmar/Shuhnaty360.git
cd Shuhnaty360
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations & Run Server
```bash
python manage.py migrate
python manage.py runserver
```

### 4️⃣ To add dummy data for the first time only.
```bash
python dummy_data.py
```
Note:
A main user is created with the following credentials:
Username: admin


Password: admin**Developed with ❤️ using Django & DRF**

