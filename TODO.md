# Production-Ready Schema Plan for Frookoon

## Objective
Design and implement production-ready database schema with:
- Proper relationships
- Indexing logic for performance
- Data validation rules

## Current State Analysis
The existing codebase has basic models for:
- User, Address, Vendor, Product, Stock, Commission
- Order, OrderItem, Payment, DeliveryPartner

## Plan

### Phase 1: Enhance Models with Indexes and Constraints

#### 1.1 User Model
- **Index:** `phone` (unique field)
- **Constraint:** Phone format validation (regex)

#### 1.2 Address Model
- **Indexes:** 
  - `user` (FK index)
  - `user + is_default` (composite for finding default address)
- **Constraint:** Latitude/longitude range validation

#### 1.3 Vendor Model
- **Indexes:**
  - `city` (for location-based queries)
  - `is_active` (for filtering active vendors)
- **Constraint:** Commission percentage range (0-100)

#### 1.4 Product Model
- **Indexes:**
  - `vendor` (FK index)
  - `category` (for category filtering)
  - `is_available` (for availability filtering)
  - `vendor + category` (composite for vendor category queries)
- **Constraint:** Price must be positive

#### 1.5 Stock Model
- **Indexes:**
  - `product` (OneToOne index)
- **Constraint:** Quantity non-negative (already exists)

#### 1.6 Order Model
- **Indexes:**
  - `user` (FK index)
  - `status` (for status filtering)
  - `created_at` (for ordering/reporting)
  - `user + status` (composite for user order history)
  - `user + created_at` (composite for user order timeline)
- **Constraints:**
  - Delivery fee non-negative
  - Total amount non-negative

#### 1.7 OrderItem Model
- **Indexes:**
  - `order` (FK index)
  - `product` (FK index)
  - `order + product` (composite for duplicate detection)
- **Constraints:**
  - Quantity must be positive
  - Price at time must be non-negative

#### 1.8 Payment Model
- **Indexes:**
  - `order` (FK index)
  - `transaction_id` (for payment gateway lookups)
  - `status` (for payment filtering)
  - `order + status` (composite)
- **Constraints:**
  - Amount must be positive
  - Status must be from predefined choices

### Phase 2: Create Documentation

#### 2.1 Schema Diagram (for Mermaid/Gemini)
- Create ER diagram description
- Include all entities and relationships
- Include indexes and constraints

#### 2.2 API Contract for Order Creation
- Document endpoint
- Request/response format
- Validation rules
- Error responses

#### 2.3 Database Performance Guide
- Index usage patterns
- Query optimization tips
- Migration strategy

## Implementation Steps

1. **Update models.py** - Add Meta classes with indexes and constraints
2. **Create migrations** - Generate migration file
3. **Update serializers** - Add any new validation
4. **Create documentation** - Schema diagram, API contract

## Files to Modify
- `Backend/api/models.py` - Add indexes and constraints
- `Backend/API_CONTRACT.md` - Update with detailed contract
- Create new schema documentation file

## Expected Output Files
1. `PRODUCTION_SCHEMA.md` - Complete schema documentation
2. `API_CONTRACT_ORDER_CREATION.md` - Order creation API contract
3. `SCHEMA_DIAGRAM_PROMPT.txt` - Gemini prompt for diagram generation

