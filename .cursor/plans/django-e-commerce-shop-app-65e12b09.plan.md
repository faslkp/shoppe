<!-- 65e12b09-b6c4-4a70-93e3-2031ba550520 e40b2202-f24c-444a-873b-5f0c02d661cb -->
# Django E-commerce Shop Application - Step-by-Step Implementation Guide

## Overview

Complete step-by-step checklist for building a Django e-commerce application with customer storefront, admin management, and REST APIs.

## Phase 1: Project Setup & Configuration

### Step 1.1: Install Dependencies

- [ ] Create `requirements.txt` file
- [ ] Add `djangorestframework` for API endpoints
- [ ] Add `django-cors-headers` (optional, for CORS if needed)
- [ ] Install dependencies: `pip install -r requirements.txt`

### Step 1.2: Create Django Apps

- [ ] Create `customers` app: `python manage.py startapp customers`
- [ ] Create `shop` app: `python manage.py startapp shop`
- [ ] Create `api` app: `python manage.py startapp api`

### Step 1.3: Update Settings Configuration

- [ ] Add `customers`, `shop`, `api` to `INSTALLED_APPS` in `config/settings.py`
- [ ] Add `rest_framework` to `INSTALLED_APPS`
- [ ] Add `rest_framework.authtoken` to `INSTALLED_APPS` (for token authentication)
- [ ] Configure REST Framework settings (authentication classes, permissions)
- [ ] Set `MEDIA_URL` and `MEDIA_ROOT` for product images
- [ ] Configure `STATIC_URL` and `STATICFILES_DIRS` if needed
- [ ] Add `LOGIN_URL` and `LOGIN_REDIRECT_URL` settings

## Phase 2: Database Models

### Step 2.1: Create Product Model (shop/models.py)

- [ ] Define `Product` model with fields:
  - [ ] `name` (CharField)
  - [ ] `description` (TextField)
  - [ ] `price` (DecimalField)
  - [ ] `image` (ImageField, optional)
  - [ ] `stock_quantity` (IntegerField)
  - [ ] `created_at` (DateTimeField, auto_now_add)
  - [ ] `updated_at` (DateTimeField, auto_now)
- [ ] Add `__str__` method
- [ ] Add `average_rating()` method to calculate average from ProductRating
- [ ] Register model in `shop/admin.py` (optional, for Django admin)

### Step 2.2: Create Customer Models (customers/models.py)

- [ ] Define `Customer` model (extend AbstractUser or create separate model):
  - [ ] `email` (EmailField, unique)
  - [ ] `password` (hashed)
  - [ ] `first_name`, `last_name` (CharField)
  - [ ] `phone` (CharField, optional)
  - [ ] `created_at` (DateTimeField)
- [ ] Or use Django User model with custom manager
- [ ] Define `Address` model:
  - [ ] `customer` (ForeignKey to Customer)
  - [ ] `street_address` (CharField)
  - [ ] `city` (CharField)
  - [ ] `state` (CharField)
  - [ ] `zip_code` (CharField)
  - [ ] `country` (CharField)
  - [ ] `is_default` (BooleanField)
  - [ ] `created_at` (DateTimeField)
- [ ] Define `Cart` model:
  - [ ] `customer` (ForeignKey to Customer)
  - [ ] `product` (ForeignKey to Product)
  - [ ] `quantity` (IntegerField)
  - [ ] `created_at` (DateTimeField)
  - [ ] Add unique constraint on (customer, product)
- [ ] Define `Order` model:
  - [ ] `customer` (ForeignKey to Customer)
  - [ ] `address` (ForeignKey to Address)
  - [ ] `status` (CharField with choices: approved/shipped/delivered)
  - [ ] `total_amount` (DecimalField)
  - [ ] `created_at` (DateTimeField)
  - [ ] `updated_at` (DateTimeField)
- [ ] Define `OrderItem` model:
  - [ ] `order` (ForeignKey to Order)
  - [ ] `product` (ForeignKey to Product)
  - [ ] `quantity` (IntegerField)
  - [ ] `price` (DecimalField - snapshot of price at order time)
- [ ] Define `ProductRating` model:
  - [ ] `customer` (ForeignKey to Customer)
  - [ ] `product` (ForeignKey to Product)
  - [ ] `rating` (IntegerField, 1-5)
  - [ ] `review` (TextField, optional)
  - [ ] `created_at` (DateTimeField)
  - [ ] Add unique constraint on (customer, product)

### Step 2.3: Create Migrations

- [ ] Run `python manage.py makemigrations`
- [ ] Review migration files
- [ ] Run `python manage.py migrate`

## Phase 3: Forms

### Step 3.1: Customer Forms (customers/forms.py)

- [ ] Create `CustomerSignupForm`:
  - [ ] Email, password, password confirmation
  - [ ] First name, last name
  - [ ] Validation for unique email
- [ ] Create `CustomerLoginForm`:
  - [ ] Email, password fields
- [ ] Create `AddressForm`:
  - [ ] All address fields
  - [ ] Checkbox for is_default
- [ ] Create `ProductRatingForm`:
  - [ ] Rating (1-5), review text

### Step 3.2: Shop Forms (shop/forms.py)

- [ ] Create `ProductForm`:
  - [ ] All product fields
  - [ ] Image upload handling

## Phase 4: Customer Views

### Step 4.1: Authentication Views (customers/views.py)

- [ ] `signup_view` - Handle customer registration
  - [ ] POST: Create customer account
  - [ ] GET: Display signup form
  - [ ] Redirect to login after signup
- [ ] `login_view` - Handle customer login
  - [ ] POST: Authenticate and login
  - [ ] GET: Display login form
  - [ ] Redirect to home after login
- [ ] `logout_view` - Handle logout
  - [ ] Logout user and redirect to home

### Step 4.2: Product Views

- [ ] `product_list_view` - Display all products
  - [ ] Show product name, price, image, average rating
  - [ ] Add search/filter functionality (optional)
  - [ ] Pagination (optional)
- [ ] `product_detail_view` - Product details page (optional enhancement)

### Step 4.3: Cart Views

- [ ] `cart_view` - Display cart items
  - [ ] Show all items in customer's cart
  - [ ] Display quantities, prices, totals
  - [ ] Allow quantity updates
- [ ] `add_to_cart_view` - Add product to cart
  - [ ] Check if item exists, update quantity or create new
  - [ ] Handle POST request
  - [ ] Redirect to cart or product list
- [ ] `remove_from_cart_view` - Remove item from cart
  - [ ] Delete cart item
  - [ ] Redirect to cart

### Step 4.4: Checkout Views

- [ ] `checkout_view` - Checkout page
  - [ ] GET: Display address selection form
  - [ ] Show existing addresses
  - [ ] Option to add new address
  - [ ] POST: Create order from cart items
  - [ ] Clear cart after order creation
  - [ ] Redirect to order confirmation

### Step 4.5: Order Views

- [ ] `order_list_view` - Display customer orders
  - [ ] Show all orders for logged-in customer
  - [ ] Display order status, date, total
- [ ] `order_detail_view` - Order details
  - [ ] Show order items, address, status
  - [ ] Display order history

### Step 4.6: Rating Views

- [ ] `rate_product_view` - Rate a product
  - [ ] GET: Display rating form
  - [ ] POST: Save rating
  - [ ] Check if customer already rated (update or create)
  - [ ] Redirect to product page

## Phase 5: Admin/Shop Views

### Step 5.1: Admin Authentication (shop/views.py)

- [ ] `admin_login_view` - Admin login
  - [ ] Use Django User model with is_staff check
  - [ ] POST: Authenticate admin user
  - [ ] GET: Display admin login form
  - [ ] Redirect to admin dashboard after login
- [ ] `admin_logout_view` - Admin logout

### Step 5.2: Customer Management

- [ ] `customer_list_view` - List all customers
  - [ ] Display customer list with pagination
  - [ ] Show customer details (name, email, registration date)

### Step 5.3: Product Management

- [ ] `product_list_view` - List all products
  - [ ] Display products with average rating
  - [ ] Show edit/delete buttons
- [ ] `add_product_view` - Add new product
  - [ ] GET: Display product form
  - [ ] POST: Save new product
- [ ] `edit_product_view` - Edit existing product
  - [ ] GET: Display form with existing data
  - [ ] POST: Update product
- [ ] `delete_product_view` - Delete product
  - [ ] Confirm deletion
  - [ ] Delete product and redirect

### Step 5.4: Order Management

- [ ] `order_list_view` - List all orders
  - [ ] Display all orders with status
  - [ ] Filter by status (optional)
- [ ] `order_detail_view` - Order details and status update
  - [ ] Display order information
  - [ ] Show status dropdown/buttons
  - [ ] POST: Update order status
  - [ ] Save status change

## Phase 6: REST API Implementation

### Step 6.1: Serializers (api/serializers.py)

- [ ] Create `CustomerSerializer` for signup
- [ ] Create `ProductSerializer` for product list
- [ ] Create `OrderSerializer` for order list
- [ ] Include nested relationships where needed

### Step 6.2: API Views (api/views.py)

- [ ] `customer_signup_api` - POST endpoint
  - [ ] Validate data
  - [ ] Create customer account
  - [ ] Return success/error response
- [ ] `customer_login_api` - POST endpoint
  - [ ] Authenticate customer
  - [ ] Generate/return token
  - [ ] Return token and user info
- [ ] `products_list_api` - GET endpoint
  - [ ] Return all products as JSON
  - [ ] Include average rating
  - [ ] No authentication required
- [ ] `orders_list_api` - GET endpoint
  - [ ] Require token authentication
  - [ ] Return orders for authenticated customer only
  - [ ] Include order items

### Step 6.3: API URL Configuration

- [ ] Create `api/urls.py`
- [ ] Map endpoints to views
- [ ] Include in root `urls.py`

## Phase 7: URL Configuration

### Step 7.1: Root URLs (config/urls.py)

- [ ] Import include from django.urls
- [ ] Add path for customers app: `path('', include('customers.urls'))`
- [ ] Add path for shop app: `path('admin/', include('shop.urls'))`
- [ ] Add path for API app: `path('api/', include('api.urls'))`
- [ ] Keep Django admin: `path('django-admin/', admin.site.urls)` (optional)

### Step 7.2: Customer URLs (customers/urls.py)

- [ ] Create `customers/urls.py`
- [ ] Add all customer routes with names
- [ ] Include authentication required decorators where needed

### Step 7.3: Shop URLs (shop/urls.py)

- [ ] Create `shop/urls.py`
- [ ] Add all admin routes with names
- [ ] Include admin authentication required decorators

### Step 7.4: API URLs (api/urls.py)

- [ ] Create `api/urls.py`
- [ ] Add all API routes
- [ ] Apply authentication classes in views

## Phase 8: Templates

### Step 8.1: Base Templates

- [ ] Create `templates/base.html` - Base template with navigation
- [ ] Create `templates/customers/base.html` - Customer base template
- [ ] Create `templates/shop/base.html` - Admin base template
- [ ] Include navigation bars, footer, messages display

### Step 8.2: Customer Templates (templates/customers/)

- [ ] `signup.html` - Signup form
- [ ] `login.html` - Login form
- [ ] `product_list.html` - Product listing with ratings
- [ ] `cart.html` - Shopping cart display
- [ ] `checkout.html` - Checkout with address selection
- [ ] `order_list.html` - Customer orders list
- [ ] `order_detail.html` - Order details
- [ ] `rate_product.html` - Rating form

### Step 8.3: Admin Templates (templates/shop/)

- [ ] `admin_login.html` - Admin login form
- [ ] `customer_list.html` - Customers list
- [ ] `product_list.html` - Products list with average rating
- [ ] `product_form.html` - Add/edit product form
- [ ] `order_list.html` - Orders list
- [ ] `order_detail.html` - Order details with status update

## Phase 9: Authentication & Permissions

### Step 9.1: Authentication Decorators

- [ ] Add `@login_required` to customer views (cart, checkout, orders, rating)
- [ ] Create custom admin decorator `@admin_required` for shop views
- [ ] Handle unauthorized access redirects

### Step 9.2: API Authentication

- [ ] Configure TokenAuthentication in DRF settings
- [ ] Add `@authentication_classes` and `@permission_classes` to API views
- [ ] Generate tokens on customer signup/login

## Phase 10: Testing & Refinement

### Step 10.1: Test Customer Flow

- [ ] Test customer signup
- [ ] Test customer login/logout
- [ ] Test product browsing
- [ ] Test add to cart (multiple items)
- [ ] Test checkout with address creation
- [ ] Test order creation and cart clearing
- [ ] Test order status viewing
- [ ] Test product rating

### Step 10.2: Test Admin Flow

- [ ] Test admin login
- [ ] Test customer list viewing
- [ ] Test product CRUD operations
- [ ] Test order status updates
- [ ] Verify average rating display

### Step 10.3: Test API Endpoints

- [ ] Test customer signup API
- [ ] Test customer login API (token generation)
- [ ] Test products list API
- [ ] Test orders list API (with authentication)
- [ ] Test unauthorized access handling

### Step 10.4: Edge Cases & Validation

- [ ] Handle empty cart scenarios
- [ ] Handle out of stock products
- [ ] Validate rating range (1-5)
- [ ] Handle duplicate ratings (update existing)
- [ ] Validate order status transitions
- [ ] Handle image uploads (if implemented)

## Phase 11: Final Configuration

### Step 11.1: Static Files

- [ ] Collect static files: `python manage.py collectstatic` (if needed)
- [ ] Configure static file serving in development

### Step 11.2: Media Files

- [ ] Configure media file serving in development
- [ ] Handle product image uploads

### Step 11.3: Create Superuser (Optional)

- [ ] Create admin superuser: `python manage.py createsuperuser`
- [ ] Test Django admin access (if keeping it)

## File Structure Reference

```
shoppe/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── customers/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── shop/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── api/
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── templates/
│   ├── base.html
│   ├── customers/
│   └── shop/
├── static/ (if needed)
├── media/ (for product images)
├── manage.py
└── requirements.txt
```

### To-dos

- [ ] Create Django apps: customers, shop, and api. Update INSTALLED_APPS in settings.py
- [ ] Define all models: Customer, Product, Address, Cart, Order, OrderItem, ProductRating
- [ ] Create and run database migrations
- [ ] Implement customer views: signup, login, product list, cart, checkout, orders, rating
- [ ] Implement admin views: login, customer list, product CRUD, order management
- [ ] Implement REST API endpoints with DRF: signup, login, products list, orders list
- [ ] Configure URL patterns for all apps and root URLconf
- [ ] Create HTML templates for customer and admin sections with base templates
- [ ] Add authentication decorators and middleware for protected views