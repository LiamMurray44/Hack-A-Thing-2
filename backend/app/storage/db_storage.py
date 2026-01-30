"""
Database storage implementation using SQLAlchemy.

This module provides a database-backed storage layer that matches
the interface of JSONStorage for backward compatibility. All methods
return dictionaries to match the existing API contract.

Written by Claude Code on 2026-01-30
User prompt: Database Integration - Add SQLAlchemy with PostgreSQL/MySQL
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..db.models import LeaveRequestDB, NotificationDB
from ..models.leave_request import LeaveStatus
from ..models.notification import NotificationType


class DBStorage:
    """
    Database storage implementation matching JSONStorage interface.

    All methods accept and return dictionaries (not ORM objects) to maintain
    compatibility with existing route handlers and business logic.
    """

    def __init__(self, db: Session):
        """
        Initialize with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    # === Leave Request Operations ===

    def get_all_leave_requests(self) -> list[dict]:
        """
        Get all leave requests.

        Returns:
            list[dict]: List of leave request dictionaries
        """
        requests = self.db.query(LeaveRequestDB).all()
        return [req.to_dict() for req in requests]

    def get_leave_request_by_id(self, request_id: str) -> dict | None:
        """
        Get a specific leave request by ID.

        Args:
            request_id: Unique identifier for the leave request

        Returns:
            dict | None: Leave request dictionary or None if not found
        """
        request = self.db.query(LeaveRequestDB).filter(
            LeaveRequestDB.id == request_id
        ).first()
        return request.to_dict() if request else None

    def create_leave_request(self, request_data: dict) -> dict:
        """
        Create a new leave request.

        Args:
            request_data: Dictionary containing leave request data

        Returns:
            dict: Created leave request dictionary
        """
        db_request = LeaveRequestDB(**request_data)
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        return db_request.to_dict()

    def update_leave_request(self, request_id: str, updates: dict) -> dict | None:
        """
        Update an existing leave request.

        Args:
            request_id: Unique identifier for the leave request
            updates: Dictionary of fields to update

        Returns:
            dict | None: Updated leave request dictionary or None if not found
        """
        request = self.db.query(LeaveRequestDB).filter(
            LeaveRequestDB.id == request_id
        ).first()

        if not request:
            return None

        # Apply updates to ORM object
        for key, value in updates.items():
            if hasattr(request, key):
                setattr(request, key, value)

        self.db.commit()
        self.db.refresh(request)
        return request.to_dict()

    def delete_leave_request(self, request_id: str) -> bool:
        """
        Delete a leave request.

        Due to cascade delete, this will also delete all associated notifications.

        Args:
            request_id: Unique identifier for the leave request

        Returns:
            bool: True if deleted, False if not found
        """
        request = self.db.query(LeaveRequestDB).filter(
            LeaveRequestDB.id == request_id
        ).first()

        if not request:
            return False

        self.db.delete(request)
        self.db.commit()
        return True

    # === Notification Operations ===

    def get_all_notifications(self) -> list[dict]:
        """
        Get all notifications.

        Returns:
            list[dict]: List of notification dictionaries
        """
        notifications = self.db.query(NotificationDB).all()
        return [notif.to_dict() for notif in notifications]

    def get_notifications_by_request_id(self, request_id: str) -> list[dict]:
        """
        Get all notifications for a specific leave request.

        Args:
            request_id: Leave request identifier

        Returns:
            list[dict]: List of notification dictionaries for the request
        """
        notifications = self.db.query(NotificationDB).filter(
            NotificationDB.request_id == request_id
        ).all()
        return [notif.to_dict() for notif in notifications]

    def get_notification_by_id(self, notification_id: str) -> dict | None:
        """
        Get a specific notification by ID.

        Args:
            notification_id: Unique notification identifier

        Returns:
            dict | None: Notification dictionary or None if not found
        """
        notification = self.db.query(NotificationDB).filter(
            NotificationDB.id == notification_id
        ).first()
        return notification.to_dict() if notification else None

    def create_notification(self, notification_data: dict) -> dict:
        """
        Create a new notification.

        Args:
            notification_data: Dictionary containing notification data

        Returns:
            dict: Created notification dictionary
        """
        db_notification = NotificationDB(**notification_data)
        self.db.add(db_notification)
        self.db.commit()
        self.db.refresh(db_notification)
        return db_notification.to_dict()

    def update_notification(self, notification_id: str, updates: dict) -> dict | None:
        """
        Update an existing notification.

        Args:
            notification_id: Unique notification identifier
            updates: Dictionary of fields to update

        Returns:
            dict | None: Updated notification dictionary or None if not found
        """
        notification = self.db.query(NotificationDB).filter(
            NotificationDB.id == notification_id
        ).first()

        if not notification:
            return None

        # Apply updates to ORM object
        for key, value in updates.items():
            if hasattr(notification, key):
                setattr(notification, key, value)

        self.db.commit()
        self.db.refresh(notification)
        return notification.to_dict()

    def delete_notification(self, notification_id: str) -> bool:
        """
        Delete a notification.

        Args:
            notification_id: Unique notification identifier

        Returns:
            bool: True if deleted, False if not found
        """
        notification = self.db.query(NotificationDB).filter(
            NotificationDB.id == notification_id
        ).first()

        if not notification:
            return False

        self.db.delete(notification)
        self.db.commit()
        return True

    def mark_notification_as_read(self, notification_id: str) -> dict | None:
        """
        Mark a notification as read.

        Args:
            notification_id: Unique notification identifier

        Returns:
            dict | None: Updated notification dictionary or None if not found
        """
        return self.update_notification(notification_id, {"read_status": True})

    def mark_notification_as_unread(self, notification_id: str) -> dict | None:
        """
        Mark a notification as unread.

        Args:
            notification_id: Unique notification identifier

        Returns:
            dict | None: Updated notification dictionary or None if not found
        """
        return self.update_notification(notification_id, {"read_status": False})
