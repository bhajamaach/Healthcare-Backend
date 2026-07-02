# Healthcare Backend API

Production-grade Django REST Framework API for healthcare management with patient-doctor relationships.

## Features

- Custom User model with email-based authentication
- JWT authentication (15min access + 7day refresh tokens)
- Patient management with strict user isolation
- Doctor management with specialization filtering
- Patient-doctor mappings with unique constraints
- PostgreSQL database with proper indexing
- Comprehensive validation and error handling
- CORS support for frontend integration

## Setup

### 1. Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip, virtualenv

### 2. Installation

```bash
cd /Users/kanishkadas/Desktop/djangoproj
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. PostgreSQL Setup

```bash
# Create database
createdb healthcare_db

# Create user
psql -U postgres -c "CREATE USER healthcare WITH PASSWORD 'healthcare_password_123';"
psql -U postgres -c "ALTER ROLE healthcare SET client_encoding TO 'utf8';"
psql -U postgres -c "ALTER ROLE healthcare SET default_transaction_isolation TO 'read committed';"
psql -U postgres -c "ALTER ROLE healthcare SET timezone TO 'UTC';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare;"
```

### 4. Environment Configuration

Check `.env` file is in place with your PostgreSQL credentials.

### 5. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access admin at http://localhost:8000/admin

## API Endpoints

### Authentication

| Method | Endpoint | Notes |
|--------|----------|-------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login, returns JWT tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

### Patients

| Method | Endpoint | Notes |
|--------|----------|-------|
| GET | `/api/patients/` | List user's patients (auth required) |
| POST | `/api/patients/` | Create new patient (auth required) |
| GET | `/api/patients/{id}/` | Retrieve patient (auth required) |
| PUT | `/api/patients/{id}/` | Update patient (auth required) |
| DELETE | `/api/patients/{id}/` | Delete patient (auth required) |

### Doctors

| Method | Endpoint | Notes |
|--------|----------|-------|
| GET | `/api/doctors/` | List all doctors (public) |
| POST | `/api/doctors/` | Create doctor (auth required) |
| GET | `/api/doctors/{id}/` | Get doctor details (public) |
| PUT | `/api/doctors/{id}/` | Update doctor (auth required) |
| DELETE | `/api/doctors/{id}/` | Delete doctor (auth required) |

Query: `?specialization=Cardiology`

### Mappings

| Method | Endpoint | Notes |
|--------|----------|-------|
| POST | `/api/mappings/` | Assign doctor to patient (auth required) |
| GET | `/api/mappings/` | List assignments for user's patients |
| GET | `/api/mappings/by_patient/?patient_id=1` | Get doctors for specific patient |
| DELETE | `/api/mappings/{id}/` | Remove assignment (auth required) |

## Request Examples

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@hospital.com",
    "name": "Dr. John Doe",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@hospital.com",
    "password": "SecurePass123"
  }'
```

### Create Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+12345678901",
    "date_of_birth": "1990-05-15",
    "medical_history": "Hypertension"
  }'
```

## Database Schema

**Users**: email (unique), name, created_at, updated_at
**Patients**: user FK (cascade), name, email, phone, DOB, medical_history, unique(user, email)
**Doctors**: name, email (unique), phone, specialization, license_number (unique), indexes on specialization
**PatientDoctorMappings**: patient FK (cascade), doctor FK (protect), assigned_by FK, notes, unique(patient, doctor)

## Password Requirements

- Minimum 8 characters
- At least 1 letter
- At least 1 number

## Error Response Format

```json
{
  "error": "Descriptive error message",
  "details": {},
  "status_code": 400
}
```

## Permissions

- **Anonymous Users**: Can view doctors list only
- **Authenticated**: Can manage own patients, create/update/delete doctors, manage mappings
- **Patient Privacy**: Users only see their own patients (enforced at queryset level)

## License

Proprietary
