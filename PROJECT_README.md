# FMLA Deadline & Timeline Tracker Prototype

Written by Claude Code on 2026-01-29
Database Integration Added: 2026-01-30
User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

## Overview

This prototype demonstrates FMLA (Family and Medical Leave Act) compliance tracking by calculating key deadlines, generating visual timelines, and displaying automated email notifications in the UI.

**Core Question Answered**: Can we model FMLA compliance logic correctly?

**Version 0.2.0** adds SQLAlchemy-based database persistence with SQLite for development and PostgreSQL support for production.

## Technology Stack

- **Backend**: Python 3.11+ + FastAPI + Pydantic
- **Frontend**: React 19
- **Database**: SQLAlchemy 2.0 + SQLite (dev) / PostgreSQL (prod) 🆕
- **Data Storage**: Database with JSON fallback option
- **Email**: In-app notification preview (notifications displayed in UI, not actually sent)

## Features

### 1. Deadline Calculations (FMLA Compliance Rules)

The system correctly calculates:

- **15-day certification deadline**: Employee has 15 calendar days from notice date OR leave start date (whichever is earlier)
- **7-day cure window**: If certification is incomplete, employee has 7 calendar days to fix issues
- **Recertification timeline**: 30 days for serious conditions, 6 months for chronic conditions

All deadlines use **CALENDAR DAYS** (not business days).

### 2. Timeline Visualization

Visual timeline showing:
- Leave start and end dates
- Certification deadlines
- Cure window periods
- Recertification dates
- Color-coded event status:
  - **Blue**: Upcoming events
  - **Yellow**: Events happening today
  - **Red**: Overdue events
  - **Green**: Completed events

### 3. At-Risk Alerts

Visual indicators when:
- Deadlines are approaching (within 3 days)
- Deadlines are overdue
- Documentation is missing
- In cure window

Risk levels:
- **High**: Overdue or in cure window
- **Medium**: Deadline within 3 days and incomplete
- **Low**: Deadline within 7 days and incomplete
- **None**: Compliant

### 4. Email Notification Previews

Notifications displayed in UI for:
- Certification deadline approaching (3 days before)
- Cure window opened (incomplete documentation)
- Recertification reminder (7 days before)
- Leave approval/denial
- Missing documentation alerts

## Project Structure

```
Hack-A-Thing-2/
├── backend/
│   ├── app/
│   │   ├── main.py                           # FastAPI entry point
│   │   ├── config.py                         # 🆕 Configuration management
│   │   ├── models/                           # Pydantic data models (API layer)
│   │   │   ├── employee.py
│   │   │   ├── leave_request.py
│   │   │   ├── timeline_event.py
│   │   │   ├── compliance.py
│   │   │   └── notification.py
│   │   ├── db/                               # 🆕 Database layer (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── database.py                   # Engine, session, Base
│   │   │   └── models.py                     # ORM models
│   │   ├── services/                         # Business logic
│   │   │   ├── deadline_calculator.py        # ⭐ Core deadline calculations
│   │   │   ├── timeline_generator.py
│   │   │   ├── compliance_checker.py
│   │   │   └── notification_service.py
│   │   ├── api/routes/                       # REST API endpoints
│   │   │   ├── leave_requests.py
│   │   │   ├── timeline.py
│   │   │   └── notifications.py
│   │   ├── storage/                          # Storage layer
│   │   │   ├── db_storage.py                 # 🆕 Database storage
│   │   │   ├── json_storage.py               # JSON fallback
│   │   │   └── storage_factory.py            # 🆕 Storage factory
│   │   └── utils/
│   │       └── date_utils.py
│   ├── scripts/                              # 🆕 Utility scripts
│   │   ├── migrate_json_to_db.py             # Data migration
│   │   └── test_database.py                  # DB integration tests
│   ├── tests/
│   │   └── test_deadline_calculator.py       # ⭐ 24 passing tests
│   ├── data/                                 # Database & JSON files
│   │   ├── fmla_tracker.db                   # 🆕 SQLite database
│   │   ├── leave_requests.json               # JSON fallback
│   │   └── notifications.json                # JSON fallback
│   ├── .env.example                          # 🆕 Config template
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── Timeline/
│   │   │   │   ├── Timeline.jsx              # ⭐ Visual timeline
│   │   │   │   └── Timeline.css
│   │   │   ├── Alerts/
│   │   │   │   ├── AlertBanner.jsx
│   │   │   │   └── AlertBanner.css
│   │   │   ├── LeaveRequest/
│   │   │   │   ├── LeaveRequestForm.jsx
│   │   │   │   └── LeaveRequestForm.css
│   │   │   ├── Notifications/
│   │   │   │   ├── NotificationsList.jsx     # ⭐ Email previews
│   │   │   │   ├── NotificationCard.jsx
│   │   │   │   └── Notifications.css
│   │   │   └── Dashboard/
│   │   │       ├── Dashboard.jsx
│   │   │       └── Dashboard.css
│   │   ├── services/
│   │   │   └── api.js
│   │   └── utils/
│   │       └── dateFormatter.js
│   └── package.json
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 16+
- npm

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt python-dateutil
   ```

4. Run tests (verify everything works):
   ```bash
   pytest tests/test_deadline_calculator.py -v
   ```
   Expected: **24 tests passing**

5. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Server runs at: http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   App opens at: http://localhost:3000

## Usage

### Creating a Leave Request

1. Click the "+ New" button in the sidebar
2. Click "Load Sample Data" to populate the form with example JSON
3. Or paste your own JSON data from the PDF field extractor
4. Click "Create Leave Request"

**Sample JSON Format:**
```json
{
  "employee": {
    "name": "Jane Doe",
    "ssn_last4": "1234",
    "phone": "(555) 555-5555",
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

### Viewing Timeline

1. Select a leave request from the sidebar
2. The timeline tab shows all events on a visual timeline
3. Hover over event markers to see details
4. Color indicates status (upcoming, overdue, completed)

### Generating Notifications

1. Go to the Timeline tab
2. Click one of the "Send Test Notifications" buttons:
   - Certification Due
   - Cure Window
   - Recertification
   - Approval
   - Missing Docs
3. Switch to the Notifications tab to view the generated email preview

### Viewing Notifications

1. Select a leave request
2. Click the "Notifications" tab
3. Use filters to view specific notification types
4. Click "Mark as Read" to update read status

## API Endpoints

### Leave Requests

- `POST /api/leave-requests/` - Create new leave request
- `GET /api/leave-requests/` - List all requests (supports filters)
- `GET /api/leave-requests/{id}` - Get specific request
- `PATCH /api/leave-requests/{id}` - Update request
- `DELETE /api/leave-requests/{id}` - Delete request

### Timeline

- `GET /api/timeline/{id}` - Get timeline for request
- `GET /api/timeline/{id}/compliance` - Get compliance status
- `GET /api/timeline/alerts/all` - Get all at-risk alerts

### Notifications

- `POST /api/notifications/` - Create notification
- `GET /api/notifications/{request_id}` - Get notifications for request
- `GET /api/notifications/` - Get all notifications (supports filters)
- `PATCH /api/notifications/{notification_id}` - Update read status
- `DELETE /api/notifications/{notification_id}` - Delete notification

API Documentation: http://localhost:8000/docs (when backend is running)

## FMLA Compliance Rules Implemented

### Certification Deadline
- Employee has 15 calendar days from when notice is given
- **BUT** certification must be received by the time leave begins
- Deadline = min(notice_date + 15 days, leave_start_date)

### Cure Window
- If certification is incomplete/insufficient, employer provides written notice
- Employee has 7 calendar days to cure deficiencies
- Cure window starts day after certification deadline
- Cure window = (cert_deadline + 1 day, cert_deadline + 7 days)

### Recertification
- **Serious health condition**: Minimum 30 calendar days
- **Chronic condition**: Every 6 months
- Can also be as specified by medical provider (not implemented in prototype)

### Key Principles
- All deadlines use **CALENDAR DAYS** (not business days)
- Weekends and holidays do NOT extend deadlines
- Deadlines are strict compliance requirements

## Test Coverage

The deadline calculator has comprehensive test coverage (24 tests):

✅ Basic certification deadline calculation
✅ Certification deadline capped at leave start
✅ Default notice date to today
✅ Same-day notice and leave start
✅ 7-day cure window calculation
✅ Cure window crossing month boundary
✅ 30-day recertification (serious condition)
✅ 6-month recertification (chronic condition)
✅ Month-end edge cases (Jan 31 → Jul 31)
✅ February edge cases (leap year handling)
✅ Deadline approaching detection
✅ Overdue detection
✅ Days until calculation
✅ Year boundary crossing
✅ Weekend deadlines NOT adjusted

Run tests:
```bash
cd backend
source venv/bin/activate
pytest tests/test_deadline_calculator.py -v
```

## Success Criteria

The prototype successfully demonstrates FMLA compliance tracking:

✅ Deadline calculator produces correct dates for all test cases (24/24 passing)
✅ Timeline visualization clearly shows all events with correct status colors
✅ At-risk alerts appear when deadlines approach or pass
✅ Notifications appear in the UI with correct content for all scenarios
✅ Notification types are correctly categorized
✅ API returns accurate compliance status for leave requests
✅ All critical business logic is tested

## Known Limitations (Prototype)

- No user authentication
- No database (JSON file storage only)
- Notifications are displayed in UI, not actually sent via email
- No production error handling or logging
- No data validation beyond Pydantic models
- Single-user system (no multi-tenancy)
- No document upload functionality (JSON input only)

## Future Enhancements (Production)

- PostgreSQL database with proper migrations
- User authentication and authorization
- Actual email sending (SMTP integration)
- Document upload and OCR for PDF processing
- Admin dashboard for HR staff
- Bulk operations and reporting
- Audit log for compliance tracking
- Integration with HR systems
- Mobile responsive design improvements
- Automated deadline notifications (cron jobs)

## License

Prototype for educational/demonstration purposes.

## Contact

For questions about this prototype, please contact the development team.
