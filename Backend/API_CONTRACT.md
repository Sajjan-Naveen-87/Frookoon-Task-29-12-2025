# API Contract

This document outlines the API contract for the Frookoon backend.

## 1. Get Products

*   **Endpoint:** `GET /api/products/`
*   **Description:** Retrieves a list of available products.
*   **Request:**
    *   No request body required.
*   **Response (200 OK):**

    ```json
    [
        {
            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
            "name": "Organic Apples",
            "category": "Fruits",
            "price": "2.99",
            "stock_quantity": 100,
            "is_available": true,
            "vendor": {
                "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                "name": "Fresh Farms",
                "city": "Green Valley",
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "commission_percentage": "10.00",
                "is_active": true
            }
        },
        {
            "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
            "name": "Whole Wheat Bread",
            "category": "Bakery",
            "price": "4.49",
            "stock_quantity": 50,
            "is_available": true,
            "vendor": {
                "id": "v2b3c4d5-e6f7-8901-2345-67890abcdefg",
                "name": "Happy Bakers",
                "city": "Green Valley",
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "commission_percentage": "12.50",
                "is_active": true
            }
        }
    ]
    ```

## 2. Create Order

*   **Endpoint:** `POST /api/orders/`
*   **Description:** Creates a new order.
*   **Request:**

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

*   **Response (201 Created):**

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
                    "stock_quantity": 98,
                    "is_available": true,
                    "vendor": {
                        "id": "v1a2b3c4-d5e6-f789-0123-456789abcdef",
                        "name": "Fresh Farms",
                        "city": "Green Valley",
                        "latitude": "34.0522",
                        "longitude": "-118.2437",
                        "commission_percentage": "10.00",
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
                    "stock_quantity": 49,
                    "is_available": true,
                    "vendor": {
                        "id": "v2b3c4d5-e6f7-8901-2345-67890abcdefg",
                        "name": "Happy Bakers",
                        "city": "Green Valley",
                        "latitude": "34.0522",
                        "longitude": "-118.2437",
                        "commission_percentage": "12.50",
                        "is_active": true
                    }
                },
                "quantity": 1,
                "price_at_time": "4.49"
            }
        ]
    }
    ```
