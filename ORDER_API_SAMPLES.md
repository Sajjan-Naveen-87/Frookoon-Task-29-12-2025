# Order API - Sample Requests & Responses

This document provides concrete examples of API requests and their expected responses.

---

## Base URL
```
http://localhost:8000/api/v1/
```

---

## 1. Create Order (POST /api/v1/orders/)

### Valid Request

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [
      {
        "product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
        "quantity": 2
      },
      {
        "product_id": "p2b3c4d5-e6f7-8901-2345-67890abcdef",
        "quantity": 1
      }
    ],
    "delivery_fee": "5.00"
  }'
```

**Response (201 Created):**
```json
{
    "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
    "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "vendor": null,
    "address": {
        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "latitude": "34.0522000",
        "longitude": "-118.2437000",
        "address_line": "123 Main Street, Apt 4B",
        "city": "Los Angeles",
        "pincode": "90001",
        "is_default": true
    },
    "delivery_partner": null,
    "status": "PENDING",
    "total_amount": "10.47",
    "delivery_fee": "5.00",
    "created_at": "2026-01-07T10:30:00.123456Z",
    "items": [
        {
            "id": "oi1a2b3c4-d5e6-f789-0123-456789abcdef",
            "product": {
                "id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
                "name": "Organic Apples (1kg)",
                "category": "Fruits",
                "price": "2.99",
                "stock": {
                    "quantity": 48,
                    "updated_at": "2026-01-07T10:30:00Z"
                },
                "is_available": true,
                "vendor": {
                    "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                    "name": "Fresh Farms Co.",
                    "city": "Green Valley",
                    "latitude": "34.0522000",
                    "longitude": "-118.2437000",
                    "is_active": true
                }
            },
            "quantity": 2,
            "price_at_time": "2.99"
        },
        {
            "id": "oi2b3c4d5-e6f7-8901-2345-67890abcdef",
            "product": {
                "id": "p2b3c4d5-e6f7-8901-2345-67890abcdef",
                "name": "Whole Wheat Bread",
                "category": "Bakery",
                "price": "4.49",
                "stock": {
                    "quantity": 49,
                    "updated_at": "2026-01-07T10:30:00Z"
                },
                "is_available": true,
                "vendor": {
                    "id": "v2b3c4d5-e6f7-8901-2345-67890abcdef",
                    "name": "Happy Bakers",
                    "city": "Green Valley",
                    "latitude": "34.0522000",
                    "longitude": "-118.2437000",
                    "is_active": true
                }
            },
            "quantity": 1,
            "price_at_time": "4.49"
        }
    ],
    "message": "Order created successfully"
}
```

---

## 2. List Orders (GET /api/v1/orders/)

### Request (All Orders)
```bash
curl http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "o3c4d5e6-f7a8-9012-3456-7890abcdef12",
            "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "vendor": {
                "id": "v3c4d5e6-f7a8-9012-3456-7890abcdef1",
                "name": "Tech Gadgets Inc.",
                "city": "San Francisco",
                "latitude": "37.7749000",
                "longitude": "-122.4194000",
                "is_active": true
            },
            "vendor_name": "Tech Gadgets Inc.",
            "address": {
                "id": "a3c4d5e6-f7a8-9012-3456-7890abcdef1",
                "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "latitude": "37.7749000",
                "longitude": "-122.4194000",
                "address_line": "789 Market St",
                "city": "San Francisco",
                "pincode": "94102",
                "is_default": false
            },
            "status": "SHIPPED",
            "total_amount": "299.99",
            "delivery_fee": "9.99",
            "created_at": "2026-01-05T14:00:00Z",
            "items_count": 1
        },
        {
            "id": "o2b3c4d5-e6f7-8901-2345-67890abcdef",
            "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "vendor": {
                "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                "name": "Fresh Farms Co.",
                "city": "Green Valley",
                "latitude": "34.0522000",
                "longitude": "-118.2437000",
                "is_active": true
            },
            "vendor_name": "Fresh Farms Co.",
            "address": {
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "latitude": "34.0522000",
                "longitude": "-118.2437000",
                "address_line": "123 Main Street, Apt 4B",
                "city": "Los Angeles",
                "pincode": "90001",
                "is_default": true
            },
            "status": "CONFIRMED",
            "total_amount": "25.50",
            "delivery_fee": "5.00",
            "created_at": "2026-01-06T09:15:00Z",
            "items_count": 3
        },
        {
            "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
            "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "vendor": null,
            "vendor_name": null,
            "address": {
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "latitude": "34.0522000",
                "longitude": "-118.2437000",
                "address_line": "123 Main Street, Apt 4B",
                "city": "Los Angeles",
                "pincode": "90001",
                "is_default": true
            },
            "status": "PENDING",
            "total_amount": "10.47",
            "delivery_fee": "5.00",
            "created_at": "2026-01-07T10:30:00Z",
            "items_count": 2
        }
    ]
}
```

### Request (Filtered by Status)
```bash
curl "http://localhost:8000/api/v1/orders/?status=PENDING" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
            "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "vendor": null,
            "vendor_name": null,
            "address": {...},
            "status": "PENDING",
            "total_amount": "10.47",
            "delivery_fee": "5.00",
            "created_at": "2026-01-07T10:30:00Z",
            "items_count": 2
        }
    ]
}
```

---

## 3. Get Order Detail (GET /api/v1/orders/{order_id}/)

### Request
```bash
curl http://localhost:8000/api/v1/orders/o1a2b3c4-d5e6-f789-0123-456789abcdef/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Response (200 OK):**
```json
{
    "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
    "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "vendor": null,
    "address": {
        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "latitude": "34.0522000",
        "longitude": "-118.2437000",
        "address_line": "123 Main Street, Apt 4B",
        "city": "Los Angeles",
        "pincode": "90001",
        "is_default": true
    },
    "delivery_partner": null,
    "status": "PENDING",
    "total_amount": "10.47",
    "delivery_fee": "5.00",
    "created_at": "2026-01-07T10:30:00.123456Z",
    "items": [
        {
            "id": "oi1a2b3c4-d5e6-f789-0123-456789abcdef",
            "product": {
                "id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
                "name": "Organic Apples (1kg)",
                "category": "Fruits",
                "price": "2.99",
                "stock": {
                    "quantity": 48,
                    "updated_at": "2026-01-07T10:30:00Z"
                },
                "is_available": true,
                "vendor": {
                    "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                    "name": "Fresh Farms Co.",
                    "city": "Green Valley",
                    "latitude": "34.0522000",
                    "longitude": "-118.2437000",
                    "is_active": true
                }
            },
            "quantity": 2,
            "price_at_time": "2.99"
        },
        {
            "id": "oi2b3c4d5-e6f7-8901-2345-67890abcdef",
            "product": {
                "id": "p2b3c4d5-e6f7-8901-2345-67890abcdef",
                "name": "Whole Wheat Bread",
                "category": "Bakery",
                "price": "4.49",
                "stock": {
                    "quantity": 49,
                    "updated_at": "2026-01-07T10:30:00Z"
                },
                "is_available": true,
                "vendor": {
                    "id": "v2b3c4d5-e6f7-8901-2345-67890abcdef",
                    "name": "Happy Bakers",
                    "city": "Green Valley",
                    "latitude": "34.0522000",
                    "longitude": "-118.2437000",
                    "is_active": true
                }
            },
            "quantity": 1,
            "price_at_time": "4.49"
        }
    ]
}
```

---

## Error Responses

### 400 Bad Request - Missing Required Fields

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_fee": "5.00"
  }'
```

**Response:**
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "address": ["This field is required."],
        "items": ["Order must contain at least one item."]
    }
}
```

### 400 Bad Request - Out of Stock

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [
      {
        "product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
        "quantity": 100
      }
    ],
    "delivery_fee": "5.00"
  }'
```

**Response:**
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "product_id": ["Not enough stock for 'Organic Apples (1kg)'. Requested: 100, Available: 48"]
    }
}
```

### 400 Bad Request - Invalid Product

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [
      {
        "product_id": "99999999-9999-9999-9999-999999999999",
        "quantity": 1
      }
    ],
    "delivery_fee": "5.00"
  }'
```

**Response:**
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "product_id": ["Product with id 99999999-9999-9999-9999-999999999999 does not exist."]
    }
}
```

### 401 Unauthorized - Missing Token

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{"address": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}'
```

**Response:**
```json
{
    "error": "authentication_error",
    "message": "Authentication required",
    "details": {
        "detail": "Authentication credentials were not provided."
    }
}
```

### 401 Unauthorized - Invalid Token

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token invalidtoken123" \
  -H "Content-Type: application/json" \
  -d '{"address": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}'
```

**Response:**
```json
{
    "error": "authentication_error",
    "message": "Invalid authentication token",
    "details": {
        "detail": "Invalid token."
    }
}
```

### 403 Forbidden - Accessing Another User's Order

**Request:**
```bash
curl http://localhost:8000/api/v1/orders/o1a2b3c4-d5e6-f789-0123-456789abcdef/ \
  -H "Authorization: Token differentusertoken123"
```

**Response:**
```json
{
    "error": "permission_error",
    "message": "Access denied",
    "details": {
        "detail": "You do not have permission to access this order."
    }
}
```

### 404 Not Found - Order Does Not Exist

**Request:**
```bash
curl http://localhost:8000/api/v1/orders/99999999-9999-9999-9999-999999999999/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Response:**
```json
{
    "error": "not_found",
    "message": "Order not found",
    "details": {
        "detail": "Order with id 99999999-9999-9999-9999-999999999999 does not exist."
    }
}
```

### 400 Bad Request - Quantity Less Than 1

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [
      {
        "product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
        "quantity": 0
      }
    ],
    "delivery_fee": "5.00"
  }'
```

**Response:**
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "quantity": ["Quantity must be at least 1."]
    }
}
```

### 400 Bad Request - Product Not Available

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [
      {
        "product_id": "p5e6f7a8-b9c0-d123-4567-890abcdef123",
        "quantity": 1
      }
    ],
    "delivery_fee": "5.00"
  }'
```

**Response:**
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "product_id": ["Product 'Discontinued Item' is not available."]
    }
}
```

### 400 Bad Request - Invalid Address

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "99999999-9999-9999-9999-999999999999",
    "items": [
      {
        "product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
        "quantity": 1
      }
    ],
    "delivery_fee": "5.00"
  }'
```

**Response:**
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "address": ["Address not found or does not belong to user."]
    }
}
```

---

## Testing the API

### Step-by-Step Test

```bash
# 1. First, get an auth token
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpassword123"}'

# Store the token
TOKEN="your_token_here"

# 2. Create an order
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "your_address_uuid",
    "items": [
      {"product_id": "product_uuid_1", "quantity": 2},
      {"product_id": "product_uuid_2", "quantity": 1}
    ],
    "delivery_fee": "5.00"
  }'

# 3. List your orders
curl http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token $TOKEN"

# 4. Get specific order details
curl http://localhost:8000/api/v1/orders/order_uuid/ \
  -H "Authorization: Token $TOKEN"
```

---

## Status Codes Summary

| Code | Meaning | Typical Use |
|------|---------|-------------|
| 200 | OK | Successful GET requests |
| 201 | Created | Successful POST (resource created) |
| 400 | Bad Request | Validation errors, invalid data |
| 401 | Unauthorized | Missing or invalid auth token |
| 403 | Forbidden | Access denied (not your order) |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Unexpected server error |

