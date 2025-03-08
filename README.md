# Shuhnaty 360

**Shuhnaty 360** is a shipment management system that facilitates tracking and managing shipments between factories and warehouses. The system serves as an intermediary between transport company owners, factories, and their customers.

## 🚀 Technologies Used

- **Django** - Backend framework
- **Django REST Framework (DRF)** - API development
- **PostgreSQL/MySQL** - Database (choose based on deployment)
- **Docker** *(optional)* - Containerization
- **Postman** - API documentation & testing
- **Swagger (drf-yasg)** - Interactive API documentation

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

### 4️⃣ Create dummy data to first time
```bash
python dummy_data.py
```

### 5️⃣ API Documentation (Postman & Swagger)

- Import the Postman collection from the `docs/` folder.
- Base API URL: `http://127.0.0.1:8000/api/`
- **Swagger UI:** [`http://127.0.0.1:8000/swagger/`](http://127.0.0.1:8000/swagger/)
- **ReDoc UI:** [`http://127.0.0.1:8000/redoc/`](http://127.0.0.1:8000/redoc/)

## 📜 API Endpoints

| Method     | Endpoint                        | Description           |
| ---------- | ------------------------------- | --------------------- |
| **GET**    | `/shipments/`                   | List all shipments    |
| **POST**   | `/shipments/`                   | Create a new shipment |
| **GET**    | `/shipments/<tracking_number>/` | Get shipment details  |
| **PUT**    | `/shipments/<tracking_number>/` | Update a shipment     |
| **DELETE** | `/shipments/<tracking_number>/` | Delete a shipment     |

## 🛠 Future Enhancements

- Implement WebSockets for real-time tracking.
- Add role-based access control (RBAC).
- Optimize queries for large-scale data.

## 📞 Support

For any issues or feature requests, please create an issue in the repository or contact the development team.

---

**Developed with ❤️ using Django & DRF**

