// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import React from 'react';
import { formatDate } from '../../utils/dateFormatter';
import './Timeline.css';

const Timeline = ({ events, leaveStartDate, leaveEndDate }) => {
  if (!events || events.length === 0) {
    return <div className="timeline-empty">No timeline events available</div>;
  }

  // Parse dates
  const startDate = new Date(leaveStartDate);
  const endDate = new Date(leaveEndDate);
  const totalDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

  // Calculate position for each event
  const getEventPosition = (eventDate) => {
    const date = new Date(eventDate);
    const daysFromStart = Math.ceil((date - startDate) / (1000 * 60 * 60 * 24));
    return Math.max(0, Math.min(100, (daysFromStart / totalDays) * 100));
  };

  // Get color based on status
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#10b981'; // green
      case 'overdue':
        return '#ef4444'; // red
      case 'today':
        return '#f59e0b'; // amber
      case 'upcoming':
        return '#3b82f6'; // blue
      default:
        return '#6b7280'; // gray
    }
  };

  // Get icon based on event type
  const getEventIcon = (eventType, isCritical) => {
    if (isCritical) return '⚠️';
    switch (eventType) {
      case 'leave_start':
        return '▶️';
      case 'leave_end':
        return '⏹️';
      case 'certification_deadline':
        return '📋';
      case 'cure_window_start':
      case 'cure_window_end':
        return '🔧';
      case 'recertification_due':
        return '🔄';
      default:
        return '📌';
    }
  };

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <div className="timeline-date-label">{formatDate(leaveStartDate)}</div>
        <div className="timeline-date-label">{formatDate(leaveEndDate)}</div>
      </div>

      <div className="timeline-bar-container">
        <div className="timeline-bar" />

        {events.map((event, index) => (
          <div
            key={index}
            className={`timeline-event ${event.status}`}
            style={{
              left: `${getEventPosition(event.event_date)}%`,
              backgroundColor: getStatusColor(event.status),
            }}
            title={`${event.title} - ${formatDate(event.event_date)}\n${event.description}`}
          >
            <div className="timeline-event-marker">
              <span className="timeline-event-icon">{getEventIcon(event.event_type, event.is_critical)}</span>
            </div>
            <div className="timeline-event-label">
              <div className="timeline-event-title">{event.title}</div>
              <div className="timeline-event-date">{formatDate(event.event_date)}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="timeline-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#3b82f6' }}></span>
          <span>Upcoming</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#f59e0b' }}></span>
          <span>Today</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ef4444' }}></span>
          <span>Overdue</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#10b981' }}></span>
          <span>Completed</span>
        </div>
      </div>
    </div>
  );
};

export default Timeline;
