# Frookoon Backend Review & Analysis

## 1. Potential Issues Identified

### Issue 1: Missing CORS Configuration (Security)
**File**: `Backend/frookoonBackend/settings.py`

**Problem**: The Django backend lacks CORS (Cross-Origin Resource Sharing) middleware. When the frontend (served from a different origin) tries to communicate with the backend API, browsers will block the requests due to CORS policy.

**Impact**:
- Frontend cannot make authenticated requests to the backend
- Development and production deployments will fail to integrate
- Security risk of overly restrictive or missing CORS policies

**Fix Required**:
```python
# Install: pip install django-cors-headers
# Add to INSTALLED_APPS: 'corsheaders',
# Add to MIDDLEWARE: 'corsheaders.middleware.CorsMiddleware',
# Add CORS settings:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]
```

---

### Issue 2: Race Condition in Stock Management (Performance/Scalability)
**File**: `Backend/api/serializers.py` - `OrderSerializer.create()`

**Problem**: Stock decrementation is performed without database-level locking. When multiple users order the same product simultaneously, race conditions can occur:

```
Time T1: User A reads stock = 10
Time T2: User B reads stock = 10
Time T3: User A decrements to 9, saves
Time T4: User B decrements to 9, saves
Result: Stock = 9 (should be 8)
```

**Impact**:
- Overselling products (stock goes negative)
- Customer dissatisfaction when orders are cancelled due to actual stock depletion
- Revenue loss from cancelled orders

**Fix Required**:
```python
from django.db import transaction
from django.db.models import F

# Use F expressions and select_for_update for atomic operations
with transaction.atomic():
    stock = Stock.objects.select_for_update().get(product=product)
    stock.quantity = F('quantity') - item_data['quantity']
    stock.save()
```

---

## 2. Order Lifecycle Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ORDER LIFECYCLE FLOW                             │
└─────────────────────────────────────────────────────────────────────────┘

   ┌──────────┐     ┌───────────┐     ┌───────────┐     ┌──────────────┐
   │  CREATE  │────▶│  CONFIRM  │────▶│  PACKING  │────▶│ SHIPPED      │
   │  PENDING │     │           │     │           │     │ (Out for     │
   │          │     │           │     │           │     │  Delivery)   │
   └──────────┘     └───────────┘     └───────────┘     └──────────────┘
        │                                                      │
        │                   CANCELLATION FLOW                  │
        │                   =================                  │
        │                                                      │
        ▼                                                      ▼
   ┌──────────┐                                          ┌──────────┐
   │CANCELLED │◀─────────────────────────────────────────│DELIVERED │
   │(Payment  │                                          │          │
   │ Failed/  │                                          │          │
   │ User     │                                          │          │
   │ Cancelled│                                          │          │
   └──────────┘                                          └──────────┘


TRANSITION RULES:
=================

CREATE → CONFIRM:
  - Payment successfully processed
  - Inventory locked (stock decremented)
  - Vendor notified

CONFIRM → PACKING:
  - Vendor acknowledged order
  - Items being prepared
  - Picklist generated

PACKING → SHIPPED:
  - Items packed
  - Handover to delivery partner
  - Tracking number assigned

SHIPPED → DELIVERED:
  - Delivery confirmed by partner
  - OTP verified (if applicable)
  - Payment released to vendor

ANY STATE → CANCELLED:
  - Payment failure (before CONFIRM)
  - User cancellation (before SHIPPED)
  - Vendor unable to fulfill
  - Stock restored on cancellation
```

---

## 3. Database Schema Improvement

### Proposed Addition: OrderStatusHistory Table

**Current Issue**: The `Order` model only stores current status. There's no audit trail of status changes.

**Proposed Improvement**:

```python
class OrderStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=30, null=True, blank=True)
    new_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(default=timezone.now)
    reason = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['order', 'changed_at']),
        ]

    def __str__(self):
        return f"{self.order.id}: {self.previous_status} → {self.new_status}"
```

**Benefits**:
1. **Audit Trail**: Complete history of order lifecycle for debugging
2. **Analytics**: Track average time between status changes
3. **Customer Support**: Trace exactly when and why orders were cancelled
4. **Fraud Prevention**: Detect unusual status change patterns

**API Enhancement**: Add endpoint `GET /api/v1/orders/{id}/history/` for customers to track their order journey.

---

## 4. Error Handling Approach - Order Creation API

### Critical API: `POST /api/v1/orders/`

The order creation API handles multiple failure scenarios. Here's the error handling approach:

```python
# Error Response Format (RFC 7807 Problem Details)
{
    "type": "https://api.frookoon.com/errors/order-creation-failed",
    "title": "Order Creation Failed",
    "status": 400,
    "detail": "Unable to create order due to validation errors",
    "instance": "/api/v1/orders/",
    "errors": [
        {
            "field": "address",
            "message": "Address is required for an order."
        }
    ],
    "request_id": "req_a1b2c3d4e5f6",
    "timestamp": "2026-01-07T10:00:00Z"
}
```

### Error Scenarios & Handling

| Scenario | HTTP Status | Error Code | User Message |
|----------|-------------|------------|--------------|
| Missing address | 400 | `ORDER_ADDRESS_REQUIRED` | Please provide a delivery address |
| Product not found | 400 | `PRODUCT_NOT_FOUND` | One or more products are unavailable |
| Insufficient stock | 400 | `INSUFFICIENT_STOCK` | Not enough stock for "{product_name}" |
| User not authenticated | 401 | `UNAUTHORIZED` | Please login to place an order |
| Database deadlock | 409 | `CONCURRENT_ORDER_CONFLICT` | High demand! Someone just ordered the last item. Please try again. |
| Invalid UUID format | 400 | `INVALID_UUID` | Invalid format for {field_name} |

### Implementation Pattern

```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

class OrderCreationError(Exception):
    def __init__(self, message, error_code, field=None):
        self.message = message
        self.error_code = error_code
        self.field = field
        super().__init__(message)

def custom_exception_handler(exc, context):
    if isinstance(exc, OrderCreationError):
        error_response = {
            'type': 'https://api.frookoon.com/errors/order-creation-failed',
            'title': 'Order Creation Failed',
            'status': 400,
            'detail': exc.message,
            'error_code': exc.error_code,
            'field': exc.field
        }
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    return exception_handler(exc, context)
```

### Logging Strategy

```python
import logging
logger = logging.getLogger(__name__)

def create(self, validated_data):
    try:
        # Order creation logic
        ...
    except OrderCreationError as e:
        logger.warning(
            f"Order creation failed: {e.error_code} - {e.message}",
            extra={
                'user_id': str(validated_data.get('user')),
                'error_code': e.error_code,
                'field': e.field,
            }
        )
        raise
    except Exception as e:
        logger.error(
            f"Unexpected error during order creation: {str(e)}",
            exc_info=True,
            extra={'user_id': str(validated_data.get('user'))}
        )
        raise OrderCreationError(
            "An unexpected error occurred. Please try again later.",
            error_code='INTERNAL_ERROR'
        )
```

---

## Assumptions Made

1. **UUID Primary Keys**: Assumed UUIDs are acceptable for all models - suitable for distributed systems but has storage/performance overhead vs auto-increment integers.

2. **Token Authentication**: Using DRF's TokenAuthentication. Would suggest JWT for mobile apps in production.

3. **Stock is Mandatory**: Assumed all products must have a Stock record before being orderable.

4. **Address is Required**: The API requires an address for order creation - correct for e-commerce.

5. **Synchronous Order Creation**: Current implementation is synchronous. For high scale, recommend async processing with message queue.

---

## Summary

| Item | Status |
|------|--------|
| Backend Code Issues Fixed | ✅ CheckConstraint, Duplicate views |
| CORS Configuration | ⚠️ Needs implementation |
| Race Condition | ⚠️ Needs database locking |
| Order Flow Design | ✅ Documented |
| Schema Improvement | ✅ OrderStatusHistory proposed |
| Error Handling | ✅ Documented |

