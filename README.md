# Finance Dashboard Backend

A comprehensive backend system for managing financial records with role-based access control, user management, and analytics dashboards.

## Features

- **User & Role Management**: Create users, assign roles (Admin, Analyst, Viewer), and manage user status
- **Financial Records Management**: Create, read, update, and delete financial transactions with soft delete support
- **Access Control**: Role-based access control enforced at the API level
- **Dashboard Analytics**: Aggregated financial data including totals, trends, and category breakdowns
- **Authentication**: JWT-based token authentication
- **Input Validation**: Comprehensive validation using Pydantic schemas
- **Error Handling**: Proper HTTP status codes and meaningful error messages
- **Pagination & Filtering**: Support for pagination and multiple filter options on records

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (can be switched to PostgreSQL)
- **Authentication**: JWT (Python-Jose)
- **Password Hashing**: Bcrypt
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Project Structure

```
finance_backend/
├── app/
│   ├── models/              # SQLAlchemy models (User, Record)
│   ├── schemas/             # Pydantic schemas for validation
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── record.py
│   │   └── analytics_service.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── records.py
│   │   └── dashboard.py
│   ├── core/                # Security and dependencies
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── enums.py             # Enum definitions
│   ├── database.py          # Database setup
│   └── main.py              # FastAPI app initialization
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## Installation

### 1. Clone/Setup the Repository
```bash
cd finance_backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Development Server
```bash
# From the project root
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Access API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication Endpoints (`/api/auth`)
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token

### User Endpoints (`/api/users`)
- `GET /me` - Get current user information
- `PUT /me` - Update current user
- `GET /{user_id}` - Get specific user (own or admin only)
- `GET ` - List all users (admin only)
- `PUT /{user_id}` - Update user (admin only)
- `DELETE /{user_id}` - Delete user (admin only)
- `POST /{user_id}/deactivate` - Deactivate user (admin only)
- `POST /{user_id}/activate` - Activate user (admin only)

### Financial Records Endpoints (`/api/records`)
- `POST ` - Create record (Admin/Analyst only)
- `GET /{record_id}` - Get specific record
- `GET ` - List user records with filtering and pagination
- `PUT /{record_id}` - Update record (Admin/Analyst only)
- `DELETE /{record_id}` - Soft delete record
- `DELETE /{record_id}/permanent` - Permanently delete record (Admin only)

### Dashboard Endpoints (`/api/dashboard`)
- `GET /summary` - Get dashboard summary with analytics

## Usage Examples

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"john_doe\",
    \"email\": \"john@example.com\",
    \"password\": \"secure_password_123\",
    \"role\": \"analyst\"
  }"
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"john_doe\",
    \"password\": \"secure_password_123\"
  }"
```

Store the returned `access_token` for subsequent requests.

### 3. Create a Financial Record
```bash
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{
    \"amount\": 5000,
    \"record_type\": \"income\",
    \"category\": \"salary\",
    \"description\": \"Monthly salary\",
    \"transaction_date\": \"2024-01-15T10:00:00Z\"
  }"
```

### 4. Get Dashboard Summary
```bash
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. List Records with Filters
```bash
curl -X GET "http://localhost:8000/api/records?record_type=expense&category=food&skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Role-Based Access Control

### Roles and Permissions

| Role | Can Create Records | Can Update Records | Can Delete Records | Can View All Users | Can Manage Users |
|------|--------------------|--------------------|--------------------|--------------------|------------------|
| Viewer | ❌ | ❌ | ❌ | ❌ | ❌ |
| Analyst | ✅ | ✅ | ✅ | ❌ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

## Data Models

### User Model
- `id`: Unique identifier
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `role`: User role (admin, analyst, viewer)
- `status`: User status (active, inactive)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Record Model
- `id`: Unique identifier
- `user_id`: Associated user ID
- `amount`: Transaction amount
- `record_type`: Income or Expense
- `category`: Transaction category
- `description`: Optional description
- `transaction_date`: Date of transaction
- `is_deleted`: Soft delete flag
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Categories

The system supports the following transaction categories:
- Income: salary, bonus, investment, freelance
- Expense: food, transportation, utilities, entertainment, healthcare, education, shopping, rent, other

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK` - Successful GET request
- `201 Created` - Successful resource creation
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - User lacks required permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Security Considerations

### Implemented
- ✅ JWT token-based authentication
- ✅ Bcrypt password hashing
- ✅ Role-based access control (RBAC)
- ✅ User status management (active/inactive)
- ✅ Input validation with Pydantic
- ✅ CORS protection

### For Production
- 🔐 Change `SECRET_KEY` to a strong random value
- 🔐 Use environment variables for sensitive data
- 🔐 Switch to PostgreSQL or production database
- 🔐 Enable HTTPS
- 🔐 Implement rate limiting
- 🔐 Add refresh token mechanism
- 🔐 Implement audit logging

## Assumptions & Design Decisions

1. **SQLite for Simplicity**: Used SQLite for database to make setup easy. Can be switched to PostgreSQL.

2. **Soft Delete**: Records can be soft deleted (marked as deleted) or hard deleted (permanently removed by admins).

3. **Role-Based Access**: 
   - Only Analysts and Admins can create/update records
   - Viewers can only read records and dashboard
   - Admins can manage users and perform hard deletes

4. **User-Scoped Records**: Users can only access their own records unless they're admin.

5. **JWT Authentication**: Stateless token-based auth for scalability.

6. **UTC Timestamps**: All timestamps stored in UTC for consistency.

7. **Dashboard Analytics**: Provides aggregated data (totals, trends, category breakdown) without returning raw records.

## Testing the API

You can test the API using:
1. **Swagger UI** at `http://localhost:8000/docs`
2. **cURL commands** as shown in examples
3. **Postman** or similar tools
4. **Python requests library**

## Performance Considerations

- Database indexes on frequently queried fields (user_id, transaction_date, category)
- Pagination to prevent large data transfers
- Aggregation queries for analytics instead of in-memory processing

## Future Enhancements

- Unit and integration tests
- Pagination improvements (cursor-based pagination)
- Advanced search capabilities
- Bulk operations (create/delete multiple records)
- Export functionality (CSV, PDF)
- Email notifications
- Two-factor authentication
- API rate limiting
- Caching layer (Redis)
- Webhook support for real-time updates

## Troubleshooting

### Database Lock Error
- Delete `finance_backend.db` and restart the application to reset the database

### Token Expired
- Get a new token by logging in again

### Permission Denied
- Ensure your user role has permissions for the action
- Check your JWT token is valid and included in headers

## License

This project is provided as-is for educational and assessment purposes.

## Support

For issues or questions, please review the API documentation at `/docs` or check the error messages returned by the API.
