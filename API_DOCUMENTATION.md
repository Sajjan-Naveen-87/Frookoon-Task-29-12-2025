# Frookoon API Documentation

## Base URL
```
http://localhost:8000/api/v1/
```

---

## Core Schemas

### User Model
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key, auto-generated |
| username | String(150) | Unique username |
| email | Email | User email address |
| phone | String(15) | Unique phone number |
| password | String | Write-only, hashed |
| date_joined | DateTime | Auto-set on creation |

### Product Model
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key, auto-generated |
| vendor | FK(Vendor) | Associated vendor |
| name | String(150) | Product name |
| category | String(50) | Product category |
| price | Decimal(10,2) | Product price |
| is_available | Boolean | Stock availability status |
| stock | OneToOne(Stock) | Related stock record |

### Order Model
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key, auto-generated |
| user | FK(User) | Customer who placed order |
| vendor | FK(Vendor) | Fulfilling vendor (optional) |
| address | FK(Address) | Delivery address |
| delivery_partner | FK(DeliveryPartner) | Assigned delivery partner |
| status | Enum | PENDING, CONFIRMED, PACKING, SHIPPED, DELIVERED, CANCELLED, FAILED |
| total_amount | Decimal(10,2) | Order total |
| delivery_fee | Decimal(10,2) | Delivery charge |
| created_at | DateTime | Order creation timestamp |

---

## API Endpoints

### 1. GET /api/v1/products/

**Description**: Retrieves a list of all available products with filtering support.

**Request**:
```http
GET /api/v1/products/
GET /api/v1/products/?category=Fruits
GET /api/v1/products/?search=apple
```

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| category | String | Filter by exact category match |
| search | String | Search in product name |

**Response (200 OK)**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "name": "Organic Apples",
            "category": "Fruits",
            "price": "2.99",
            "stock": {
                "quantity": 100,
                "updated_at": "2026-01-07T10:00:00Z"
            },
            "is_available": true,
            "vendor": {
                "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                "name": "Fresh Farms",
                "city": "Green Valley",
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "is_active": true
            }
        },
        {
            "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            "name": "Whole Wheat Bread",
            "category": "Bakery",
            "price": "4.49",
            "stock": {
                "quantity": 50,
                "updated_at": "2026-01-07T10:00:00Z"
            },
            "is_available": true,
            "vendor": {
                "id": "v2b3c4d5-e6f7-8901-2345-67890abcdefg",
                "name": "Happy Bakers",
                "city": "Green Valley",
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "is_active": true
            }
        }
    ]
}
```

---

### 2. POST /api/v1/orders/

**Description**: Creates a new order. Requires authentication.

**Request**:
```http
POST /api/v1/orders/
Authorization: Token <token>
Content-Type: application/json
```

**Request Body**:
```json
{
    "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "address": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "items_write": [
        {
            "product_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "quantity": 2
        },
        {
            "product_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            "quantity": 1
        }
    ],
    "delivery_fee": "5.00"
}
```

**Request Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user | UUID | Yes | User ID |
| address | UUID | Yes | Address ID |
| items_write | Array | Yes | List of order items |
| items_write[].product_id | UUID | Yes | Product ID |
| items_write[].quantity | Integer | Yes | Quantity to order |
| delivery_fee | Decimal | Yes | Delivery fee |

**Response (201 Created)**:
```json
{
    "id": "o1a2b3c4-d5e6-f789-0123-456789abcdef",
    "user": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "vendor": null,
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
    "status": "PENDING",
    "total_amount": "10.47",
    "delivery_fee": "5.00",
    "created_at": "2026-01-07T10:00:00Z",
    "items": [
        {
            "id": "oi1a2b3c4-d5e6-f789-0123-456789abcdef",
            "product": {
                "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "name": "Organic Apples",
                "category": "Fruits",
                "price": "2.99",
                "stock": {
                    "quantity": 98,
                    "updated_at": "2026-01-07T10:00:00Z"
                },
                "is_available": true,
                "vendor": {
                    "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                    "name": "Fresh Farms",
                    "city": "Green Valley",
                    "latitude": "34.0522",
                    "longitude": "-118.2437",
                    "is_active": true
                }
            },
            "quantity": 2,
            "price_at_time": "2.99"
        },
        {
            "id": "oi2b3c4d5-e6f7-8901-2345-67890abcdef",
            "product": {
                "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
                "name": "Whole Wheat Bread",
                "category": "Bakery",
                "price": "4.49",
                "stock": {
                    "quantity": 49,
                    "updated_at": "2026-01-07T10:00:00Z"
                },
                "is_available": true,
                "vendor": {
                    "id": "v2b3c4d5-e6f7-8901-2345-67890abcdefg",
                    "name": "Happy Bakers",
                    "city": "Green Valley",
                    "latitude": "34.0522",
                    "longitude": "-118.2437",
                    "is_active": true
                }
            },
            "quantity": 1,
            "price_at_time": "4.49"
        }
    ]
}
```

**Error Responses**:

400 Bad Request - Validation Error:
```json
{
    "non_field_errors": [
        "Address is required for an order."
    ]
}
```

400 Bad Request - Out of Stock:
```json
{
    "non_field_errors": [
        "Not enough stock for Organic Apples"
    ]
}
```

401 Unauthorized:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### 3. POST /api/v1/auth/signup/ (Additional)

**Description**: Register a new user.

**Request**:
```http
POST /api/v1/auth/signup/
Content-Type: application/json
```

**Request Body**:
```json
{
    "username": "john_doe",
    "phone": "+1234567890",
    "password": "securepassword123"
}
```

**Response (201 Created)**:
```json
{
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "username": "john_doe",
    "phone": "+1234567890"
}
```

---

### 4. POST /api/v1/auth/token/ (Additional)

**Description**: Obtain authentication token.

**Request**:
```http
POST /api/v1/auth/token/
Content-Type: application/json
```

**Request Body**:
```json
{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Response (200 OK)**:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request / Validation Error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

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

