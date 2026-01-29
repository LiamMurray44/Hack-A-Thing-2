// Written by Claude Code on 2026-01-29
// User prompt: Create pending leaves table

import React from 'react';
import { formatDate } from '../../utils/dateFormatter';
import './PendingLeavesTable.css';

const PendingLeavesTable = ({ leaveRequests, onSelectRequest }) => {
  // Filter for pending requests only
  const pendingRequests = leaveRequests.filter(req =>
    req.status === 'pending' || req.status === 'awaiting_docs'
  );

  const getStatusBadgeClass = (status) => {
    const classes = {
      pending: 'status-pending',
      awaiting_docs: 'status-awaiting',
    };
    return classes[status] || 'status-pending';
  };

  const getStatusLabel = (status) => {
    const labels = {
      pending: 'Pending',
      awaiting_docs: 'Awaiting Docs',
    };
    return labels[status] || status;
  };

  if (pendingRequests.length === 0) {
    return (
      <div className="pending-table-container">
        <div className="pending-header">
          <h3>Pending Leave Requests</h3>
          <span className="pending-count">0 pending</span>
        </div>
        <div className="pending-empty">
          <div className="empty-icon">✅</div>
          <p>No pending leave requests</p>
          <p className="empty-hint">All requests have been processed</p>
        </div>
      </div>
    );
  }

  return (
    <div className="pending-table-container">
      <div className="pending-header">
        <h3>Pending Leave Requests</h3>
        <span className="pending-count">{pendingRequests.length} pending</span>
      </div>

      <div className="pending-table-wrapper">
        <table className="pending-table">
          <thead>
            <tr>
              <th>Employee Name</th>
              <th>Status</th>
              <th>Leave Date</th>
              <th>Return Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {pendingRequests.map((req) => (
              <tr key={req.id} className="pending-row">
                <td className="employee-cell">
                  <div className="employee-name">{req.employee.name}</div>
                  <div className="employee-details">
                    SSN: ***-**-{req.employee.ssn_last4}
                  </div>
                </td>
                <td>
                  <span className={`status-badge ${getStatusBadgeClass(req.status)}`}>
                    {getStatusLabel(req.status)}
                  </span>
                </td>
                <td className="date-cell">{formatDate(req.leave.start_date)}</td>
                <td className="date-cell">{formatDate(req.leave.end_date)}</td>
                <td>
                  <button
                    className="view-btn"
                    onClick={() => onSelectRequest(req)}
                  >
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PendingLeavesTable;
