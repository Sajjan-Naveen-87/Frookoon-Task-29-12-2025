# Frookoon Order API Documentation

## Base URL
```
http://localhost:8000/api/v1/
```

---

## Order API Overview

The Order API provides endpoints for creating, viewing, and managing orders in the Frookoon platform.

### Key Features:
- **Authentication Required**: All order endpoints require valid authentication token
- **Automatic User Binding**: User is automatically assigned from authenticated token
- **Stock Validation**: Real-time stock check before order creation
- **Atomic Transactions**: Order creation uses database transactions to ensure data integrity

---

## API Endpoints

### 1. POST /api/v1/orders/

**Description**: Creates a new order. Requires authentication.

**Authentication**: Required (Token in Authorization header)

**Request**:
```http
POST /api/v1/orders/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json
```

**Request Body**:
```json
{
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
}
```

**Request Fields**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| address | UUID | Yes | Must exist in Address model | Delivery address ID |
| items | Array | Yes | Min 1 item | List of order items |
| items[].product_id | UUID | Yes | Must exist, have stock | Product ID |
| items[].quantity | Integer | Yes | Min 1, must not exceed stock | Quantity to order |
| delivery_fee | Decimal | Yes | Min 0 | Delivery fee |

---

### 2. GET /api/v1/orders/

**Description**: Retrieves a list of orders for the authenticated user.

**Authentication**: Required (Token in Authorization header)

**Request**:
```http
GET /api/v1/orders/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| status | String | Filter by order status (PENDING, CONFIRMED, etc.) |
| page | Integer | Page number for pagination |

**Response (200 OK)**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
            "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "vendor": {
                "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                "name": "Fresh Farms",
                "city": "Green Valley"
            },
            "address": {
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "address_line": "123 Main St",
                "city": "Los Angeles",
                "pincode": "90001"
            },
            "status": "CONFIRMED",
            "total_amount": "10.47",
            "delivery_fee": "5.00",
            "created_at": "2026-01-07T10:00:00Z",
            "items_count": 2
        },
        {
            "id": "o2b3c4d5-e6f7-8901-2345-67890abcdef",
            "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "vendor": null,
            "address": {
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "address_line": "456 Oak Ave",
                "city": "San Francisco",
                "pincode": "94102"
            },
            "status": "PENDING",
            "total_amount": "25.99",
            "delivery_fee": "7.50",
            "created_at": "2026-01-06T14:30:00Z",
            "items_count": 3
        }
    ]
}
```

---

### 3. GET /api/v1/orders/{order_id}/

**Description**: Retrieves detailed information about a specific order.

**Authentication**: Required (Token in Authorization header)

**Request**:
```http
GET /api/v1/orders/o1a2b3c4-d5e6-f789-0123-456789abcdef/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK)**:
```json
{
    "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
    "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "vendor": {
        "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
        "name": "Fresh Farms",
        "city": "Green Valley",
        "latitude": "34.0522",
        "longitude": "-118.2437"
    },
    "address": {
        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "latitude": "34.0522",
        "longitude": "-118.2437",
        "address_line": "123 Main St",
        "city": "Los Angeles",
        "pincode": "90001",
        "is_default": true
    },
    "delivery_partner": null,
    "status": "CONFIRMED",
    "total_amount": "10.47",
    "delivery_fee": "5.00",
    "created_at": "2026-01-07T10:00:00Z",
    "items": [
        {
            "id": "oi1a2b3c4-d5e6-f789-0123-456789abcdef",
            "product": {
                "id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
                "name": "Organic Apples",
                "category": "Fruits",
                "price": "2.99",
                "is_available": true,
                "vendor": {
                    "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                    "name": "Fresh Farms"
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
                "is_available": true,
                "vendor": {
                    "id": "v2b3c4d5-e6f7-8901-2345-67890abcdef",
                    "name": "Happy Bakers"
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

### 400 Bad Request - Validation Error (Missing Fields)
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "address": ["This field is required."],
        "items": ["This field is required."]
    }
}
```

### 400 Bad Request - Out of Stock
```json
{
    "error": "stock_error",
    "message": "Insufficient stock for one or more items",
    "details": [
        {
            "product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
            "product_name": "Organic Apples",
            "requested_quantity": 100,
            "available_quantity": 50
        }
    ]
}
```

### 400 Bad Request - Invalid Product
```json
{
    "error": "validation_error",
    "message": "Invalid product ID",
    "details": {
        "product_id": ["Product with id p1a2b3c4-d5e6-7890-1234-567890abcdef does not exist."]
    }
}
```

### 400 Bad Request - Product Unavailable
```json
{
    "error": "availability_error",
    "message": "One or more products are not available",
    "details": [
        {
            "product_id": "p3c4d5e6-f7a8-9012-3456-7890abcdef1",
            "product_name": "Organic Bananas",
            "is_available": false
        }
    ]
}
```

### 400 Bad Request - Invalid Address
```json
{
    "error": "validation_error",
    "message": "Invalid address",
    "details": {
        "address": ["Address not found or does not belong to user."]
    }
}
```

### 400 Bad Request - Empty Items
```json
{
    "error": "validation_error",
    "message": "Order must contain at least one item",
    "details": {
        "items": ["Items list cannot be empty."]
    }
}
```

### 400 Bad Request - Invalid Quantity
```json
{
    "error": "validation_error",
    "message": "Invalid quantity",
    "details": {
        "quantity": ["Quantity must be at least 1."]
    }
}
```

### 401 Unauthorized - Missing Token
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
```json
{
    "error": "authentication_error",
    "message": "Invalid authentication token",
    "details": {
        "detail": "Invalid token."
    }
}
```

### 403 Forbidden - Access Denied
```json
{
    "error": "permission_error",
    "message": "You do not have permission to access this order",
    "details": {
        "detail": "You are not authorized to view this order."
    }
}
```

### 404 Not Found - Order Not Found
```json
{
    "error": "not_found",
    "message": "Order not found",
    "details": {
        "detail": "Order with id o1a2b3c4-d5e6-f789-0123-456789abcdef does not exist."
    }
}
```

### 500 Internal Server Error
```json
{
    "error": "server_error",
    "message": "An unexpected error occurred",
    "details": {
        "detail": "Please try again later or contact support."
    }
}
```

---

## Order Status Flow

```
┌─────────┐     ┌─────────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│ PENDING │────▶│ CONFIRMED   │────▶│ PACKING │────▶│ SHIPPED │────▶│DELIVERED │
└─────────┘     └─────────────┘     └─────────┘     └─────────┘     └──────────┘
      │                                    │
      │                                    ▼
      │                              ┌──────────┐
      └─────────────────────────────▶│ CANCELLED│
                                     └──────────┘
```

**Status Values**:

| Status | Description |
|--------|-------------|
| PENDING | Order created, awaiting payment |
| CONFIRMED | Payment received, inventory locked |
| PACKING | Order being prepared |
| SHIPPED | Out for delivery |
| DELIVERED | Successfully delivered |
| CANCELLED | Order cancelled (by user or system) |
| FAILED | Payment failed |

---

## Sample Request Sequence

### Step 1: User Authentication (Get Token)
```http
POST /api/v1/auth/token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Response**:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

### Step 2: Create Order
```http
POST /api/v1/orders/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [
        {
            "product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
            "quantity": 2
        }
    ],
    "delivery_fee": "5.00"
}
```

**Response (201 Created)**:
```json
{
    "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
    "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "status": "PENDING",
    "total_amount": "10.98",
    "delivery_fee": "5.00",
    "created_at": "2026-01-07T10:00:00Z",
    "items": [
        {
            "id": "oi1a2b3c4-d5e6-f789-0123-456789abcdef",
            "product": {
                "id": "p1a2b3c4-d5e6-7890-1234-567890abcdef",
                "name": "Organic Apples",
                "price": "2.99"
            },
            "quantity": 2,
            "price_at_time": "2.99"
        }
    ],
    "message": "Order created successfully"
}
```

### Step 3: Get Order Details
```http
GET /api/v1/orders/o1a2b3c4-d5e6-f789-0123-456789abcdef/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK)**:
```json
{
    "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
    "status": "CONFIRMED",
    "total_amount": "10.98",
    "delivery_fee": "5.00",
    "items": [...],
    "message": "Order confirmed successfully"
}
```

### Step 4: List User Orders
```http
GET /api/v1/orders/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK)**:
```json
{
    "count": 1,
    "results": [
        {
            "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
            "status": "CONFIRMED",
            "total_amount": "10.98",
            "created_at": "2026-01-07T10:00:00Z",
            "items_count": 1
        }
    ]
}
```

---

## Running the Backend

```bash
# Navigate to backend directory
cd Backend

# Install dependencies (if needed)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

---

## Testing with curl

```bash
# Create an order
curl -X POST http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items": [{"product_id": "p1a2b3c4-d5e6-7890-1234-567890abcdef", "quantity": 2}],
    "delivery_fee": "5.00"
  }'

# List orders
curl http://localhost:8000/api/v1/orders/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"

# Get order detail
curl http://localhost:8000/api/v1/orders/o1a2b3c4-d5e6-f789-0123-456789abcdef/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

