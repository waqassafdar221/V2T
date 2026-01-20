# Authentication API Quick Reference

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. User Signup
**POST** `/auth/signup`

**Request:**
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "role": "Student",
  "password": "password123"
}
```

**Roles:** `Student`, `Teacher`, `Others`

**Response (201):**
```json
{
  "message": "User registered successfully. Please check your email for OTP verification.",
  "email": "john@example.com",
  "username": "johndoe"
}
```

---

### 2. Verify OTP
**POST** `/auth/verify-otp`

**Request:**
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response (200):**
```json
{
  "message": "Email verified successfully. You can now login.",
  "verified": true
}
```

---

### 3. Login
**POST** `/auth/login`

**Request:**
```json
{
  "username_or_email": "johndoe",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "Student",
    "is_verified": true,
    "created_at": "2026-01-20T10:30:00"
  }
}
```

---

### 4. Resend OTP
**POST** `/auth/resend-otp?email=john@example.com`

**Response (200):**
```json
{
  "message": "OTP has been resent to your email",
  "email": "john@example.com"
}
```

---

## Authentication Flow

1. **Register** → POST `/auth/signup`
2. **Check Console** → Copy OTP from terminal output
3. **Verify** → POST `/auth/verify-otp` with OTP
4. **Login** → POST `/auth/login`
5. **Use Token** → Include in headers: `Authorization: Bearer <token>`

---

## Error Codes

- **400** - Bad Request (invalid data, duplicate user, expired OTP)
- **401** - Unauthorized (wrong credentials)
- **403** - Forbidden (email not verified)
- **404** - Not Found (user doesn't exist)

---

## Development Notes

- **OTP Location:** In development, OTP is printed to the terminal console
- **OTP Expiry:** 10 minutes
- **Token Expiry:** 24 hours
- **Password Requirements:** Minimum 8 characters

---

## Interactive API Docs

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
