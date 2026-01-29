// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import React from 'react';
import { formatDateTime } from '../../utils/dateFormatter';
import './Notifications.css';

const NotificationCard = ({ notification, onMarkAsRead }) => {
  const getNotificationTypeLabel = (type) => {
    const labels = {
      certification_due: 'Certification Deadline',
      cure_window: 'Cure Window',
      recertification_due: 'Recertification',
      approval_notice: 'Approval Notice',
      denial_notice: 'Denial Notice',
      missing_docs: 'Missing Documents',
    };
    return labels[type] || type;
  };

  const getNotificationTypeColor = (type) => {
    const colors = {
      certification_due: '#3b82f6',
      cure_window: '#ef4444',
      recertification_due: '#f59e0b',
      approval_notice: '#10b981',
      denial_notice: '#dc2626',
      missing_docs: '#f59e0b',
    };
    return colors[type] || '#6b7280';
  };

  return (
    <div className={`notification-card ${notification.read_status ? 'read' : 'unread'}`}>
      <div className="notification-header">
        <span
          className="notification-type-badge"
          style={{ backgroundColor: getNotificationTypeColor(notification.type) }}
        >
          {getNotificationTypeLabel(notification.type)}
        </span>
        <span className="notification-date">{formatDateTime(notification.created_at)}</span>
      </div>

      <div className="notification-email">
        <div className="email-from">
          <strong>From:</strong> FMLA Compliance Team &lt;noreply@fmla.example.com&gt;
        </div>
        <div className="email-to">
          <strong>To:</strong> {notification.recipient}
        </div>
        <div className="email-subject">
          <strong>Subject:</strong> {notification.subject}
        </div>
      </div>

      <div className="notification-body">
        {notification.body.split('\n').map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>

      <div className="notification-actions">
        {!notification.read_status && (
          <button
            className="btn-mark-read"
            onClick={() => onMarkAsRead(notification.id)}
          >
            Mark as Read
          </button>
        )}
      </div>
    </div>
  );
};

export default NotificationCard;
