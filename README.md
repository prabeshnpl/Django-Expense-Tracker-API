# 💸 Django Expense Tracker API

A secure, RESTful Expense & Income Tracking API built with Django and Django REST Framework. This project was developed as an intern-level task and includes JWT-based authentication, full CRUD operations, tax calculations, and permission-based access control.

---

## 🚀 Features

- ✅ User Registration & Login with JWT Authentication
- ✅ Track personal expenses and incomes
- ✅ Auto-tax calculation (flat or percentage)
- ✅ Role-based access:
  - **Regular users** manage only their data
  - **Superusers** can access all records (Default Django Admin page is used)
- ✅ Paginated API responses
- ✅ Secure endpoints with permission handling
- ✅ Clean RESTful design and proper HTTP status codes

---

## 🧱 Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT via `djangorestframework-simplejwt`
- **Database:** SQLite (development)
- **Language:** Python 3.8+

---

## 🗃️ Models

### `User`
- Uses Django’s built-in user model.

### `ExpenseIncome`
| Field | Type | Description |
|-------|------|-------------|
| user | ForeignKey | Linked user |
| title | CharField | Max 200 chars |
| description | TextField | Optional |
| amount | DecimalField | 10 digits, 2 decimal places |
| transaction_type | CharField | Choices: `credit`, `debit` |
| tax | DecimalField | Default: 0 |
| tax_type | CharField | Choices: `flat`, `percentage`, default: `flat` |
| created_at | DateTimeField | Auto timestamp |
| updated_at | DateTimeField | Auto timestamp |

**Tax Logic:**
- `flat`: `total = amount + tax`
- `percentage`: `total = amount + (amount × tax ÷ 100)`

---

## 🔐 Authentication

JWT-based authentication is used.

### Endpoints
```http
POST /api/auth/register/     # Register user
POST /api/auth/login/        # Get access and refresh tokens
POST /api/auth/refresh/      # Refresh access token

GET    /api/expenses/           # List records (paginated)
POST   /api/expenses/           # Create new record
GET    /api/expenses/{id}/      # Retrieve specific record
PUT    /api/expenses/{id}/      # Update record
DELETE /api/expenses/{id}/      # Delete record
```
**Rules:**
- All endpoints require an access token in the header: `Authorization: Bearer <access_token>`
- Access token and Refresh token are provided as response during login process
- Refresh access token through respective endpoint
