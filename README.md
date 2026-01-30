# FMLA Deadline & Timeline Tracker - Hack-A-Thing 2

**Written by Claude Code on 2026-01-29**
**Database Integration Added: 2026-01-30**

A prototype system demonstrating FMLA (Family and Medical Leave Act) compliance tracking through automated deadline calculations, visual timelines, and email notification previews.

**Version 0.2.0** introduces SQLAlchemy-based database persistence with SQLite for development and PostgreSQL support for production.

## 🎯 Project Goal

Answer the critical question: **Can we correctly model FMLA compliance logic?**

This prototype proves that complex FMLA deadline rules can be accurately implemented in software, with comprehensive test coverage validating correctness.

## ✨ Key Features

### 1. **Accurate Deadline Calculations**
- 15-day certification deadline (calendar days)
- 7-day cure window for incomplete documentation
- Recertification timelines (30 days or 6 months)
- **24 passing unit tests** validating edge cases

### 2. **Visual Timeline**
- Interactive horizontal timeline showing all FMLA events
- Color-coded status indicators:
  - 🔵 Blue = Upcoming
  - 🟡 Yellow = Today
  - 🔴 Red = Overdue
  - 🟢 Green = Completed
- Hover tooltips with event details


### 3. **Compliance Alerts**
- Real-time at-risk detection
- Risk levels: High / Medium / Low
- Banner alerts for approaching/overdue deadlines
- Missing documentation warnings

### 4. **Email Notification Previews**
- In-app notification display (prototype - not actually sent)
- 5 notification types:
  - Certification deadline approaching
  - Cure window opened
  - Recertification due
  - Approval/Denial notices
  - Missing documentation alerts
- Full email formatting (subject, to/from, body)


### 5. Details
- Showcases leave status, start, and return date
- Displays FMLA eligibility
- Features state that the employee is from
- Status color, showing if the employee has been approved, denied, waiting for documents, or pending approval

### 6. **Database Persistence** 🆕
- SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- ACID transactions for data integrity
- Foreign key relationships with cascade delete
- Indexes on frequently queried fields for performance
- JSON columns for embedded objects (employee, leave, medical_provider)
- Feature flag for safe rollback to JSON storage
- Connection pooling support for production

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm

### 1. Start Backend (Terminal 1)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Database (First Time Only)

```bash
# Copy environment configuration
cp .env.example .env

# Run database migration (if you have existing JSON data)
python scripts/migrate_json_to_db.py
```

#### Start Server

```bash
uvicorn app.main:app --reload
# or: python -m uvicorn app.main:app --reload
```

Backend runs at: **http://localhost:8000**

The database is automatically initialized on startup. By default, uses SQLite at `backend/data/fmla_tracker.db`.

### 2. Verify Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/test_deadline_calculator.py -v
```

Expected: **✅ 24 tests passed**

### 3. Start Frontend (Terminal 2)

```bash
cd frontend
npm install
npm start
```

Frontend opens at: **http://localhost:3000**

## 📖 Usage Guide

### Creating Your First Leave Request

1. Click **"+ New"** button in the sidebar
2. Click **"Load Sample Data"** to populate example JSON
3. Click **"Create Leave Request"**
4. The request appears in the sidebar with timeline

### Exploring the Timeline

1. Select a leave request from the sidebar
2. View the **Timeline** tab showing:
   - Leave duration (horizontal bar)
   - Event markers positioned by date
   - Color-coded status
3. Hover over markers for details

### Generating Notifications

1. On the Timeline tab, find **"Send Test Notifications"**
2. Click any notification type button:
   - Certification Due
   - Cure Window
   - Recertification
   - Approval
   - Missing Docs
3. Switch to **Notifications** tab to view the email preview

### Filtering Notifications

1. Go to **Notifications** tab
2. Use filter buttons:
   - All
   - Unread
   - Certification
   - Cure Window
   - Recertification
3. Click **"Mark as Read"** on any notification

## 🏗️ Architecture

```
Frontend (React)          Backend (FastAPI)              Database
    │                          │                            │
    ├─ Dashboard ──────────────┼─ Leave Requests API ──────┼─ leave_requests (table)
    ├─ Timeline ───────────────┼─ Timeline API ─────────────┤
    ├─ Notifications ──────────┼─ Notifications API ───────┼─ notifications (table)
    └─ Alerts ─────────────────┼─ Compliance Checker ──────┘
                               │
                               ├─ Storage Layer:            SQLite (dev)
                               │  • DBStorage ⭐             PostgreSQL (prod)
                               │  • StorageFactory
                               │  • JSONStorage (fallback)
                               │
                               └─ Services:
                                  • DeadlineCalculator ⭐
                                  • TimelineGenerator
                                  • ComplianceChecker
                                  • NotificationService
```

### Critical Components

**Backend (`backend/app/services/deadline_calculator.py`)**
- Core FMLA compliance logic
- All calculations use **calendar days** (not business days)
- Handles edge cases: month-end, weekends, leap years
- Fully tested (24 unit tests)

**Frontend (`frontend/src/components/Timeline/Timeline.jsx`)**
- Visual timeline rendering
- Dynamic event positioning
- Color-coded status system
- Responsive hover interactions

**Notifications (`frontend/src/components/Notifications/`)**
- Email-style notification cards
- Filtering by type/read status
- In-app display (prototype - not sent)

## 📊 API Endpoints

### Leave Requests
- `POST /api/leave-requests/` - Create new request
- `GET /api/leave-requests/` - List all (supports filters)
- `GET /api/leave-requests/{id}` - Get specific request
- `PATCH /api/leave-requests/{id}` - Update request
- `DELETE /api/leave-requests/{id}` - Delete request

### Timeline & Compliance
- `GET /api/timeline/{id}` - Get timeline events
- `GET /api/timeline/{id}/compliance` - Get compliance status
- `GET /api/timeline/alerts/all` - Get all at-risk alerts

### Notifications
- `POST /api/notifications/` - Create notification
- `GET /api/notifications/{request_id}` - Get notifications for request
- `GET /api/notifications/` - Get all notifications
- `PATCH /api/notifications/{id}` - Update read status

Interactive API docs: **http://localhost:8000/docs**

## 🧪 Testing

### Backend Unit Tests

```bash
cd backend
source venv/bin/activate
pytest tests/test_deadline_calculator.py -v
```

**Test Coverage:**
- ✅ Basic certification deadline
- ✅ Certification capped at leave start
- ✅ 7-day cure window
- ✅ 30-day recertification (serious)
- ✅ 6-month recertification (chronic)
- ✅ Month-end edge cases
- ✅ Leap year handling
- ✅ Weekend deadlines NOT adjusted
- ✅ Year boundary crossing
- ✅ Approaching/overdue detection
- **...and 14 more tests**

### API Integration Test

```bash
chmod +x test_api.sh
./test_api.sh
```

Tests:
1. Create leave request
2. Fetch timeline
3. Check compliance status
4. Generate notification

## 📋 FMLA Rules Implemented

### Certification Deadline
```
Employee has 15 calendar days from notice date
BUT certification must be received by leave start date
Deadline = min(notice_date + 15 days, leave_start_date)
```

### Cure Window
```
If certification incomplete:
  - Employer provides written notice
  - Employee has 7 calendar days to fix issues
  - Window starts day after certification deadline
```

### Recertification
```
Serious condition: Every 30 days minimum
Chronic condition: Every 6 months
```

### Key Principle
**All deadlines use CALENDAR DAYS** - weekends and holidays do NOT extend deadlines!

## 🎨 Sample Data

```json
{
  "employee": {
    "name": "Jane Doe",
    "ssn_last4": "1234",
    "phone": "5555555555",
    "email": "jane.doe@example.com"
  },
  "leave": {
    "start_date": "2025-02-01",
    "end_date": "2025-04-01",
    "intermittent": false,
    "condition_type": "serious"
  },
  "medical_provider": {
    "name": "Dr. John Smith",
    "signature_present": true,
    "date_signed": "2025-01-20"
  },
  "compliance_flags": ["missing_physician_phone"]
}
```

## ✅ Success Criteria Met

- ✅ Deadline calculator produces correct dates (24/24 tests passing)
- ✅ Timeline shows all events with accurate status colors
- ✅ At-risk alerts appear for approaching/overdue deadlines
- ✅ Notifications display correct content for all scenarios
- ✅ API returns accurate compliance status
- ✅ All critical business logic is tested

## 🔮 Future Enhancements

**For Production:**
- ~~PostgreSQL database (replace JSON files)~~ ✅ **Implemented in v0.2.0**
- User authentication & authorization
- Actual email sending (SMTP/SendGrid)
- Document upload with OCR
- Admin dashboard for HR
- Automated background jobs for notifications
- Integration with HRIS systems
- Audit logging for compliance
- Mobile-responsive improvements
- Bulk operations & reporting

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11+, FastAPI, Pydantic |
| Frontend | React 19, Axios, date-fns |
| Database | SQLAlchemy 2.0, SQLite (dev), PostgreSQL (prod) |
| Storage | DBStorage with JSON fallback |
| Migrations | Alembic (optional) |
| Testing | pytest |
| API Docs | Swagger/OpenAPI (built-in) |

## 📁 Project Structure

```
Hack-A-Thing-2/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Configuration 🆕
│   │   ├── models/                    # Pydantic models
│   │   ├── db/                        # Database (SQLAlchemy) 🆕
│   │   │   ├── database.py           # Engine & session
│   │   │   └── models.py             # ORM models
│   │   ├── services/                  # Business logic ⭐
│   │   ├── api/routes/                # REST endpoints
│   │   ├── storage/                   # Storage layer 🆕
│   │   │   ├── db_storage.py         # Database storage
│   │   │   ├── json_storage.py       # JSON fallback
│   │   │   └── storage_factory.py    # Factory pattern
│   │   └── utils/                     # Date utilities
│   ├── scripts/                       # Utility scripts 🆕
│   │   ├── migrate_json_to_db.py     # Data migration
│   │   └── test_database.py          # DB integration tests
│   ├── tests/                         # Unit tests ⭐
│   ├── data/                          # Database & JSON files
│   │   └── fmla_tracker.db           # SQLite database 🆕
│   ├── .env.example                   # Config template 🆕
│   └── .env                           # Local config (gitignored)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Timeline/              # Visual timeline ⭐
│   │   │   ├── Notifications/         # Email previews ⭐
│   │   │   ├── Alerts/                # Compliance alerts
│   │   │   ├── Dashboard/             # Main view
│   │   │   └── LeaveRequest/          # Create form
│   │   ├── services/                  # API client
│   │   └── utils/                     # Date formatting
│   └── package.json
│
├── README.md                          # This file
├── PROJECT_README.md                  # Detailed documentation
└── test_api.sh                        # API integration test
```

## 🗄️ Database Configuration

### Default Setup (SQLite)

The system uses SQLite by default, which requires no additional setup. The database file is automatically created at `backend/data/fmla_tracker.db`.

### Environment Variables

Configure database settings in `backend/.env`:

```bash
# Database URL (SQLite - default)
DATABASE_URL=sqlite:///./data/fmla_tracker.db

# For PostgreSQL (production)
# DATABASE_URL=postgresql://user:password@localhost:5432/fmla_tracker

# Feature flag (toggle between database and JSON files)
USE_DATABASE=true

# Environment
ENVIRONMENT=development
DEBUG=true
```

### PostgreSQL Setup (Production)

1. **Create database:**
   ```sql
   CREATE DATABASE fmla_tracker;
   CREATE USER fmla_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE fmla_tracker TO fmla_user;
   ```

2. **Install PostgreSQL driver:**
   ```bash
   pip install psycopg2-binary
   ```

3. **Update `.env`:**
   ```bash
   DATABASE_URL=postgresql://fmla_user:secure_password@localhost:5432/fmla_tracker
   ```

4. **Restart backend** - tables are created automatically

### Migration from JSON

If you have existing JSON data:

```bash
cd backend
python scripts/migrate_json_to_db.py
```

This migrates all leave requests and notifications from JSON files to the database.

### Rollback to JSON Storage

To disable database and use JSON files:

```bash
# In backend/.env
USE_DATABASE=false
```

Restart the backend - it will use `leave_requests.json` and `notifications.json`.

## 🗃️ Database Schema

### Tables

**leave_requests**
- Stores FMLA leave requests
- JSON columns for employee, leave, medical_provider (embedded objects)
- Indexes on: id, status, created_at
- Enum constraints for status values

**notifications**
- Email notifications linked to leave requests
- Foreign key to leave_requests with CASCADE DELETE
- Indexes on: id, request_id, type, read_status, created_at

### Key Features

- ✅ ACID transactions for data integrity
- ✅ Foreign key relationships (cascade delete)
- ✅ Optimized indexes for query performance
- ✅ JSON columns for flexible embedded objects
- ✅ Automatic timestamps (created_at, updated_at)
- ✅ Connection pooling for PostgreSQL

## 🐛 Known Limitations (Prototype)

- No user authentication
- ~~JSON file storage only (no database)~~ ✅ **Database integration added in v0.2.0**
- Notifications displayed in UI (not sent)
- No document upload (JSON input only)
- Single-user system (but supports concurrent access with database)
- No production error handling
- No audit logging

## 📝 License

Educational prototype for CS98 Hack-A-Thing 2.

## 🤝 Contributing

This is a prototype for demonstration purposes. For questions or improvements, please contact the development team.

---

**Built with ❤️ by Claude Code**

*Demonstrating that complex compliance logic can be modeled correctly in software.*
