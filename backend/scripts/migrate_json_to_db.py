"""
Migrate existing JSON data to database.

This script loads data from leave_requests.json and notifications.json
and inserts it into the SQLite/PostgreSQL database.

Run once after database initialization.

Written by Claude Code on 2026-01-30
User prompt: Database Integration - Add SQLAlchemy with PostgreSQL/MySQL
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, date
from app.db.database import SessionLocal, init_db
from app.db.models import LeaveRequestDB, NotificationDB
from app.storage.json_storage import JSONStorage


def migrate_data():
    """Migrate data from JSON files to database."""
    print("=" * 70)
    print("FMLA Tracker: JSON to Database Migration")
    print("=" * 70)
    print()

    # Initialize database tables
    print("Step 1: Creating database tables...")
    init_db()
    print("[OK] Database tables created successfully")
    print()

    # Load JSON data
    print("Step 2: Loading JSON data...")
    json_storage = JSONStorage()
    leave_requests = json_storage.get_all_leave_requests()
    notifications = json_storage.get_all_notifications()

    print(f"  Found {len(leave_requests)} leave requests")
    print(f"  Found {len(notifications)} notifications")
    print()

    # Create database session
    db = SessionLocal()

    try:
        # Migrate leave requests
        print("Step 3: Migrating leave requests...")
        for i, lr_data in enumerate(leave_requests, 1):
            # Convert date strings to date objects if needed
            if isinstance(lr_data.get('notice_date'), str):
                try:
                    lr_data['notice_date'] = datetime.fromisoformat(
                        lr_data['notice_date'].replace('Z', '+00:00')
                    ).date()
                except:
                    lr_data['notice_date'] = None

            if isinstance(lr_data.get('created_at'), str):
                try:
                    lr_data['created_at'] = datetime.fromisoformat(
                        lr_data['created_at'].replace('Z', '+00:00')
                    ).date()
                except:
                    lr_data['created_at'] = date.today()

            # Create ORM object
            db_request = LeaveRequestDB(**lr_data)
            db.add(db_request)

            if i % 5 == 0 or i == len(leave_requests):
                print(f"  Migrated {i}/{len(leave_requests)} requests...", end='\r')

        db.commit()
        print(f"\n[OK] Successfully migrated {len(leave_requests)} leave requests")
        print()

        # Migrate notifications
        print("Step 4: Migrating notifications...")
        for i, notif_data in enumerate(notifications, 1):
            # Convert datetime strings
            if isinstance(notif_data.get('created_at'), str):
                try:
                    notif_data['created_at'] = datetime.fromisoformat(
                        notif_data['created_at'].replace('Z', '+00:00')
                    )
                except:
                    notif_data['created_at'] = datetime.utcnow()

            # Create ORM object
            db_notification = NotificationDB(**notif_data)
            db.add(db_notification)

            if i % 5 == 0 or i == len(notifications):
                print(f"  Migrated {i}/{len(notifications)} notifications...", end='\r')

        db.commit()
        print(f"\n[OK] Successfully migrated {len(notifications)} notifications")
        print()

        # Verify migration
        print("Step 5: Verifying migration...")
        db_requests_count = db.query(LeaveRequestDB).count()
        db_notifications_count = db.query(NotificationDB).count()

        print(f"  Leave requests in database: {db_requests_count}")
        print(f"  Notifications in database: {db_notifications_count}")

        if db_requests_count == len(leave_requests) and db_notifications_count == len(notifications):
            print("[OK] Verification successful - all data migrated")
        else:
            print("[WARNING] Row count mismatch detected")

        print()
        print("=" * 70)
        print("[SUCCESS] Migration completed successfully!")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  * {len(leave_requests)} leave requests migrated")
        print(f"  * {len(notifications)} notifications migrated")
        print()
        print("Next steps:")
        print("  1. Backup JSON files: cp data/*.json data/*.json.backup")
        print("  2. Update .env: USE_DATABASE=true")
        print("  3. Restart backend: uvicorn app.main:app --reload")
        print()

    except Exception as e:
        print()
        print("=" * 70)
        print("[ERROR] Migration failed!")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        print("Rolling back database changes...")
        db.rollback()
        print("Database rolled back successfully")
        print()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    migrate_data()
