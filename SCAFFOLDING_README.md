# Certify

An FMLA (Family and Medical Leave Act) compliance tracking system featuring automated deadline calculations, interactive visual timelines, and email notification previews. This prototype demonstrates that complex compliance logic can be accurately modeled in software.

![Status: Prototype](https://img.shields.io/badge/Status-Prototype-yellow)
![Version: 0.2.0](https://img.shields.io/badge/Version-0.2.0-blue)

## Architecture

### Overview

Certify is a full-stack web application with a clear separation between frontend presentation, backend business logic, and data persistence.

```
┌─────────────────┐       ┌──────────────────┐       ┌─────────────┐
│  React Frontend │ ◄───► │  FastAPI Backend │ ◄───► │  Database   │
│   (Port 3000)   │       │   (Port 8000)    │       │  (SQLite)   │
└─────────────────┘       └──────────────────┘       └─────────────┘
```

### Tech Stack

**Backend:**
- **Python 3.11+** - Core language
- **FastAPI** - Modern async web framework
- **SQLAlchemy 2.0** - SQL ORM with SQLite/PostgreSQL support
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server
- **pytest** - Testing framework (24 unit tests)

**Frontend:**
- **React 19** - UI library
- **Axios** - HTTP client for API requests
- **date-fns** - Date formatting and manipulation
- **react-scripts** - Build tooling (Create React App)

**Database:**
- **SQLite** - Embedded database (development)
- **PostgreSQL** - Relational database (production-ready)

### Code Organization

```
backend/
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # Configuration management with Pydantic
│   ├── models/                     # Pydantic models (data validation)
│   │   ├── employee.py
│   │   ├── leave_request.py
│   │   ├── notification.py
│   │   ├── timeline_event.py
│   │   └── compliance.py
│   ├── db/                         # Database layer (SQLAlchemy)
│   │   ├── database.py             # Engine, session management
│   │   └── models.py               # ORM models (tables)
│   ├── services/                   # Business logic (core algorithms)
│   │   ├── deadline_calculator.py  # ⭐ FMLA deadline rules
│   │   ├── timeline_generator.py   # Timeline event creation
│   │   ├── compliance_checker.py   # At-risk detection
│   │   └── notification_service.py # Notification generation
│   ├── api/routes/                 # REST API endpoints
│   │   ├── leave_requests.py       # CRUD operations
│   │   ├── timeline.py             # Timeline/compliance endpoints
│   │   └── notifications.py        # Notification endpoints
│   ├── storage/                    # Data access layer (abstraction)
│   │   ├── storage_factory.py      # Factory pattern for storage selection
│   │   ├── db_storage.py           # Database storage implementation
│   │   └── json_storage.py         # JSON file fallback
│   └── utils/                      # Shared utilities
│       └── date_utils.py           # Date arithmetic helpers
├── tests/                          # Unit tests
│   └── test_deadline_calculator.py # 24 tests validating FMLA rules
├── scripts/                        # Utility scripts
│   ├── migrate_json_to_db.py       # Data migration tool
│   └── test_database.py            # DB integration tests
├── data/                           # Data files
│   ├── fmla_tracker.db             # SQLite database (gitignored)
│   ├── leave_requests.json         # JSON fallback (gitignored)
│   └── notifications.json          # JSON fallback (gitignored)
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment configuration template

frontend/
├── src/
│   ├── App.js                      # Main application component
│   ├── components/                 # React UI components
│   │   ├── Dashboard/              # Main dashboard view
│   │   ├── LeaveRequest/           # Create/edit leave request form
│   │   ├── Timeline/               # ⭐ Interactive timeline visualization
│   │   ├── Notifications/          # ⭐ Email notification previews
│   │   └── Alerts/                 # Compliance alert banners
│   ├── services/                   # API client
│   │   └── api.js                  # Axios HTTP requests
│   └── utils/                      # Frontend utilities
│       └── dateUtils.js            # Date formatting
├── package.json                    # npm dependencies
└── public/                         # Static assets
```

### Key Design Patterns

- **Factory Pattern**: `storage_factory.py` dynamically selects database vs JSON storage
- **Service Layer**: Business logic isolated in `services/` for testability
- **ORM Pattern**: SQLAlchemy models abstract database operations
- **RESTful API**: Clean HTTP endpoints with standard verbs (GET, POST, PATCH, DELETE)

### Critical Components

**🔥 `deadline_calculator.py`** - Core FMLA compliance engine
- All calculations use **calendar days** (not business days)
- Handles certification deadlines, cure windows, recertification
- Edge cases: month-end, weekends, leap years, year boundaries
- 100% test coverage (24 unit tests)

**📊 `Timeline.jsx`** - Visual timeline component
- Dynamic event positioning by date
- Color-coded status indicators (upcoming, today, overdue, completed)
- Responsive hover interactions with tooltips

## Setup

### Prerequisites

- **Python 3.11+** (check: `python3 --version`)
- **Node.js 16+** (check: `node --version`)
- **npm** (usually bundled with Node.js)
- **Git** (for version control)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create Python virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # macOS/Linux:
   source venv/bin/activate

   # Windows:
   venv\Scripts\activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables (first time only):**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` if needed. Default SQLite configuration works out of the box:
   ```bash
   DATABASE_URL=sqlite:///./data/fmla_tracker.db
   USE_DATABASE=true
   ENVIRONMENT=development
   DEBUG=true
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

6. **Start backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend runs at: **http://localhost:8000**

   API documentation: **http://localhost:8000/docs**

### Frontend Setup

1. **Open new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install npm dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

   Frontend opens automatically at: **http://localhost:3000**

### Database Setup

The database is **automatically initialized** on first backend startup. No manual steps required for SQLite.

**Optional: Migrate existing JSON data to database:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python scripts/migrate_json_to_db.py
```

### Verify Installation

1. **Test backend (run from `backend/` directory):**
   ```bash
   pytest tests/test_deadline_calculator.py -v
   ```
   Expected: **✅ 24/24 tests passed**

2. **Test API integration (run from project root):**
   ```bash
   chmod +x test_api.sh
   ./test_api.sh
   ```

3. **Check frontend:** Visit http://localhost:3000 and click "Load Sample Data"

## Deployment

### Production Checklist

Before deploying to production, complete these steps:

**Backend Configuration:**

1. **Set production environment variables:**
   ```bash
   ENVIRONMENT=production
   DEBUG=false
   DATABASE_URL=postgresql://user:password@hostname:5432/fmla_tracker
   CORS_ORIGINS=https://yourdomain.com
   ```

2. **Install PostgreSQL driver:**
   ```bash
   pip install psycopg2-binary
   ```

3. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE fmla_tracker;
   CREATE USER fmla_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE fmla_tracker TO fmla_user;
   ```

4. **Update `.env` with PostgreSQL connection:**
   ```bash
   DATABASE_URL=postgresql://fmla_user:secure_password@localhost:5432/fmla_tracker
   ```

**Frontend Build:**

```bash
cd frontend
npm run build
```

This creates optimized production files in `frontend/build/`.

### Deployment Options

**Option 1: Traditional Server (VPS/Cloud VM)**

- **Backend**: Deploy with Gunicorn + Nginx
  ```bash
  gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```
- **Frontend**: Serve `build/` folder with Nginx or Apache
- **Database**: PostgreSQL on same server or managed service (AWS RDS, DigitalOcean Managed DB)

**Option 2: Platform-as-a-Service (PaaS)**

- **Heroku**: Use Python and Node.js buildpacks
- **Render**: Deploy as web service (backend) + static site (frontend)
- **Railway**: One-click deploy with PostgreSQL addon
- **Fly.io**: Containerized deployment with Dockerfile

**Option 3: Containerized (Docker)**

Create `Dockerfile` for backend and frontend, deploy to:
- AWS ECS/Fargate
- Google Cloud Run
- DigitalOcean App Platform
- Kubernetes cluster

**Option 4: Serverless**

- Backend: AWS Lambda + API Gateway (requires serverless adapter)
- Frontend: AWS S3 + CloudFront, Vercel, or Netlify
- Database: AWS RDS or Aurora Serverless

### Environment Variables for Production

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `ENVIRONMENT=production`
- `DEBUG=false`
- `CORS_ORIGINS` - Allowed frontend domains

**Recommended:**
- Secret management service (AWS Secrets Manager, HashiCorp Vault)
- SSL/TLS certificates (Let's Encrypt)
- Monitoring (Sentry, DataDog, New Relic)
- Backup automation for database

### Security Considerations

- ⚠️ Add user authentication (JWT, OAuth)
- ⚠️ Enable rate limiting
- ⚠️ Implement input sanitization
- ⚠️ Set up HTTPS (SSL/TLS)
- ⚠️ Use environment variables for secrets (never commit `.env`)
- ⚠️ Configure firewall rules
- ⚠️ Enable database backups

**Note:** This is a prototype and does not include production-grade security features.

## Authors

- **Jackson Yassin**
- **Jada Jones**
- **Michael Burns**
- **Basil Lone**
- **Liam Murray**

## Acknowledgments

- **Claude Code** - AI assistant for rapid prototyping and code generation
- **FastAPI** - Excellent documentation and framework design
- **React** - Powerful UI library with great developer experience
- **SQLAlchemy** - Robust ORM that simplifies database operations
- **US Department of Labor** - FMLA regulations documentation

---

**Built for CS98 - Hack-A-Thing 2**

*Demonstrating that complex compliance logic can be modeled correctly in software.*
