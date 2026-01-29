// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import React from 'react';
import { formatDate, getDaysUntilText } from '../../utils/dateFormatter';
import './AlertBanner.css';

const AlertBanner = ({ compliance, onAction }) => {
  if (!compliance || !compliance.at_risk) {
    return null;
  }

  const getRiskColor = (level) => {
    const colors = {
      high: '#dc2626',
      medium: '#f59e0b',
      low: '#3b82f6',
    };
    return colors[level] || '#6b7280';
  };

  const getRiskIcon = (level) => {
    if (level === 'high') return '🚨';
    if (level === 'medium') return '⚠️';
    return 'ℹ️';
  };

  const messages = [];

  if (compliance.days_until_certification_deadline < 0) {
    messages.push(
      `Certification deadline OVERDUE by ${Math.abs(compliance.days_until_certification_deadline)} days`
    );
  } else if (compliance.days_until_certification_deadline <= 3) {
    messages.push(
      `Certification due in ${compliance.days_until_certification_deadline} days (${formatDate(compliance.certification_deadline)})`
    );
  }

  if (compliance.in_cure_window) {
    messages.push(
      `In 7-day cure window - ends ${formatDate(compliance.cure_window_end)}`
    );
  }

  if (compliance.compliance_issues.length > 0) {
    messages.push(
      `Missing: ${compliance.compliance_issues.join(', ')}`
    );
  }

  return (
    <div
      className="alert-banner"
      style={{ backgroundColor: getRiskColor(compliance.risk_level) }}
    >
      <div className="alert-icon">{getRiskIcon(compliance.risk_level)}</div>
      <div className="alert-content">
        <div className="alert-title">
          {compliance.risk_level === 'high' ? 'URGENT ACTION REQUIRED' : 'Attention Needed'}
        </div>
        <div className="alert-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className="alert-message">
              • {msg}
            </div>
          ))}
        </div>
      </div>
      {onAction && (
        <button className="alert-action-btn" onClick={onAction}>
          View Details
        </button>
      )}
    </div>
  );
};

export default AlertBanner;
