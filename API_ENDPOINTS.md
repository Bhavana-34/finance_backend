# API Endpoints Reference

## Base URL
```
http://localhost:8000
```

## Authentication Endpoints

### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "role": "analyst"
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}

Response (200):
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

---

## User Management Endpoints

### Get Current User
```http
GET /api/users/me
Authorization: Bearer YOUR_TOKEN

Response (200):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "analyst",
  "status": "active",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Update Current User
```http
PUT /api/users/me
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "email": "newemail@example.com",
  "password": "new_password_123"
}

Response (200): Updated user object
```

### Get User by ID
```http
GET /api/users/{user_id}
Authorization: Bearer YOUR_TOKEN

Response (200): User object
(Own users can view their profile, admins can view all)
```

### List All Users
```http
GET /api/users?skip=0&limit=10
Authorization: Bearer YOUR_TOKEN (ADMIN ONLY)

Response (200): Array of user objects
```

### Update User (Admin)
```http
PUT /api/users/{user_id}
Authorization: Bearer YOUR_TOKEN (ADMIN ONLY)
Content-Type: application/json

{
  "role": "viewer",
  "status": "inactive"
}

Response (200): Updated user object
```

### Delete User
```http
DELETE /api/users/{user_id}
Authorization: Bearer YOUR_TOKEN (ADMIN ONLY)

Response (204): No content
```

### Deactivate User
```http
POST /api/users/{user_id}/deactivate
Authorization: Bearer YOUR_TOKEN (ADMIN ONLY)

Response (200): Updated user object (status: inactive)
```

### Activate User
```http
POST /api/users/{user_id}/activate
Authorization: Bearer YOUR_TOKEN (ADMIN ONLY)

Response (200): Updated user object (status: active)
```

---

## Financial Records Endpoints

### Create Record
```http
POST /api/records
Authorization: Bearer YOUR_TOKEN (ANALYST/ADMIN ONLY)
Content-Type: application/json

{
  "amount": 5000.00,
  "record_type": "income",
  "category": "salary",
  "description": "Monthly salary",
  "transaction_date": "2024-01-15T10:00:00Z"
}

Response (201):
{
  "id": 1,
  "user_id": 1,
  "amount": 5000.00,
  "record_type": "income",
  "category": "salary",
  "description": "Monthly salary",
  "transaction_date": "2024-01-15T10:00:00Z",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Get Specific Record
```http
GET /api/records/{record_id}
Authorization: Bearer YOUR_TOKEN

Response (200): Record object
(Users can only access their own records)
```

### List Records with Filtering
```http
GET /api/records?skip=0&limit=10&record_type=expense&category=food&start_date=2024-01-01T00:00:00Z&end_date=2024-01-31T23:59:59Z
Authorization: Bearer YOUR_TOKEN

Query Parameters:
- skip: number of records to skip (default: 0)
- limit: max records to return (default: 10, max: 100)
- record_type: "income" or "expense" (optional)
- category: transaction category (optional)
- start_date: filter from date (optional)
- end_date: filter until date (optional)

Response (200):
{
  "records": [
    { record_object },
    { record_object }
  ],
  "total_count": 25,
  "skip": 0,
  "limit": 10
}
```

### Update Record
```http
PUT /api/records/{record_id}
Authorization: Bearer YOUR_TOKEN (ANALYST/ADMIN ONLY)
Content-Type: application/json

{
  "amount": 5500.00,
  "category": "bonus"
}

Response (200): Updated record object
```

### Delete Record (Soft Delete)
```http
DELETE /api/records/{record_id}
Authorization: Bearer YOUR_TOKEN (ANALYST/ADMIN ONLY)

Response (204): No content
(Record marked as deleted but not removed from database)
```

### Permanently Delete Record
```http
DELETE /api/records/{record_id}/permanent
Authorization: Bearer YOUR_TOKEN (ADMIN ONLY)

Response (204): No content
(Record permanently removed from database)
```

---

## Dashboard Endpoints

### Get Dashboard Summary
```http
GET /api/dashboard/summary
Authorization: Bearer YOUR_TOKEN

Response (200):
{
  "total_income": 50000.00,
  "total_expenses": 15000.00,
  "net_balance": 35000.00,
  "category_wise_totals": {
    "salary": {
      "total": 45000.00,
      "count": 3
    },
    "food": {
      "total": 5000.00,
      "count": 25
    }
  },
  "recent_records": [
    { record_object },
    { record_object }
  ],
  "monthly_trend": {
    "2024-01": {
      "income": 15000.00,
      "expense": 5000.00
    },
    "2023-12": {
      "income": 12000.00,
      "expense": 4500.00
    }
  }
}
```

---

## Health Check

### Server Status
```http
GET /health

Response (200):
{
  "status": "healthy"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "User role 'viewer' is not permitted for this action"
}
```

### 404 Not Found
```json
{
  "detail": "Record not found"
}
```

---

## Record Type Options
- `income`
- `expense`

## Category Options
- `salary`
- `bonus`
- `investment`
- `freelance`
- `food`
- `transportation`
- `utilities`
- `entertainment`
- `healthcare`
- `education`
- `shopping`
- `rent`
- `other`

## Role Options
- `viewer` - Can only view data
- `analyst` - Can create and manage records
- `admin` - Full access including user management

## User Status Options
- `active`
- `inactive`

---

## cURL Examples

### Register as Analyst
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_analyst",
    "email": "john@example.com",
    "password": "password123",
    "role": "analyst"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_analyst",
    "password": "password123"
  }'
```

### Create Income Record
```bash
TOKEN="your_access_token_here"
curl -X POST "http://localhost:8000/api/records" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "amount": 3000,
    "record_type": "income",
    "category": "freelance",
    "description": "Freelance project payment",
    "transaction_date": "2024-01-15T10:30:00Z"
  }'
```

### Get Dashboard
```bash
TOKEN="your_access_token_here"
curl -X GET "http://localhost:8000/api/dashboard/summary" \
  -H "Authorization: Bearer $TOKEN"
```

### Filter Expenses
```bash
TOKEN="your_access_token_here"
curl -X GET "http://localhost:8000/api/records?record_type=expense&category=food&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Testing with Swagger UI

Best way to test the API is through the built-in Swagger UI:

1. Start the server: `python -m uvicorn app.main:app --reload`
2. Open browser: `http://localhost:8000/docs`
3. Click "Authorize" and enter your token
4. Try endpoints directly from the UI

---

## Notes

- All timestamps are in UTC ISO 8601 format
- All amounts must be positive numbers
- Usernames and emails must be unique
- Passwords are hashed with Bcrypt
- Users can only see their own records (except admins)
- Pagination defaults to 10 items per page, max 100
