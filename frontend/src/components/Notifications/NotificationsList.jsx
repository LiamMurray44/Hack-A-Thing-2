// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import React, { useState, useEffect } from 'react';
import NotificationCard from './NotificationCard';
import { notificationsAPI } from '../../services/api';
import './Notifications.css';

const NotificationsList = ({ requestId }) => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchNotifications();
  }, [requestId]);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const response = await notificationsAPI.getByRequestId(requestId);
      setNotifications(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching notifications:', err);
      setError('Failed to load notifications');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (notificationId) => {
    try {
      await notificationsAPI.update(notificationId, true);
      // Update local state
      setNotifications((prev) =>
        prev.map((n) =>
          n.id === notificationId ? { ...n, read_status: true } : n
        )
      );
    } catch (err) {
      console.error('Error marking notification as read:', err);
    }
  };

  const filteredNotifications = notifications.filter((n) => {
    if (filter === 'all') return true;
    if (filter === 'unread') return !n.read_status;
    return n.type === filter;
  });

  if (loading) {
    return <div className="notifications-loading">Loading notifications...</div>;
  }

  if (error) {
    return <div className="notifications-error">{error}</div>;
  }

  return (
    <div className="notifications-list-container">
      <div className="notifications-header">
        <h3>Email Notifications (Preview)</h3>
        <p className="notifications-subtitle">
          These notifications are displayed in the UI for prototype purposes.
          In production, they would be sent via email.
        </p>
      </div>

      <div className="notifications-filter">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All ({notifications.length})
        </button>
        <button
          className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
          onClick={() => setFilter('unread')}
        >
          Unread ({notifications.filter((n) => !n.read_status).length})
        </button>
        <button
          className={`filter-btn ${filter === 'certification_due' ? 'active' : ''}`}
          onClick={() => setFilter('certification_due')}
        >
          Certification
        </button>
        <button
          className={`filter-btn ${filter === 'cure_window' ? 'active' : ''}`}
          onClick={() => setFilter('cure_window')}
        >
          Cure Window
        </button>
        <button
          className={`filter-btn ${filter === 'recertification_due' ? 'active' : ''}`}
          onClick={() => setFilter('recertification_due')}
        >
          Recertification
        </button>
      </div>

      {filteredNotifications.length === 0 ? (
        <div className="notifications-empty">
          No notifications found for this filter.
        </div>
      ) : (
        <div className="notifications-list">
          {filteredNotifications.map((notification) => (
            <NotificationCard
              key={notification.id}
              notification={notification}
              onMarkAsRead={handleMarkAsRead}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default NotificationsList;
