// Written by Claude Code on 2026-01-29
// User prompt: modify the leaves tab, so that in rows it displays the employees name, the stage of their leave, the start and return date and whether or not they are eligible for FMLA and their location(state)

import React, { useMemo } from 'react';
import { parseISO, isAfter, isBefore, startOfToday } from 'date-fns';
import { formatDate } from '../../utils/dateFormatter';
import './LeavesTable.css';

const LeavesTable = ({ leaveRequests = [], onSelectRequest }) => {
  const getLeaveStage = (startDate, endDate) => {
    const today = startOfToday();
    const start = parseISO(startDate);
    const end = parseISO(endDate);

    if (isAfter(start, today)) {
      return { label: 'Pre-Leave', className: 'stage-pre-leave' };
    } else if (isBefore(end, today)) {
      return { label: 'Returned', className: 'stage-returned' };
    } else {
      return { label: 'On Leave', className: 'stage-on-leave' };
    }
  };

  const getStatusBadgeClass = (status) => {
    const classes = {
      pending: 'status-pending',
      approved: 'status-approved',
      denied: 'status-denied',
      awaiting_docs: 'status-awaiting',
    };
    return classes[status] || 'status-pending';
  };

  const enrichedLeaves = useMemo(() => {
    return leaveRequests.map(req => {
      const stage = getLeaveStage(req.leave.start_date, req.leave.end_date);
      return { ...req, stage };
    });
  }, [leaveRequests]);

  if (leaveRequests.length === 0) {
    return (
      <div className="leaves-table-empty">
        <p>No leave requests found</p>
      </div>
    );
  }

  return (
    <div className="leaves-table-container">
      <table className="leaves-table">
        <thead>
          <tr>
            <th>Employee Name</th>
            <th>Leave Stage</th>
            <th>Start Date</th>
            <th>Return Date</th>
            <th>FMLA Eligible</th>
            <th>Location</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {enrichedLeaves.map((req) => (
            <tr key={req.id} className="leaves-table-row">
              <td className="employee-name">{req.employee.name}</td>
              <td>
                <span className={`leave-stage ${req.stage.className}`}>
                  {req.stage.label}
                </span>
              </td>
              <td>{formatDate(req.leave.start_date)}</td>
              <td>{formatDate(req.leave.end_date)}</td>
              <td>
                <span className={`fmla-badge ${req.fmla_eligible ? 'eligible' : 'not-eligible'}`}>
                  {req.fmla_eligible ? 'Yes' : 'No'}
                </span>
              </td>
              <td className="location">{req.employee.state || 'N/A'}</td>
              <td>
                <span className={`request-status ${getStatusBadgeClass(req.status)}`}>
                  {req.status.replace('_', ' ')}
                </span>
              </td>
              <td>
                <button
                  className="btn-view-details"
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
  );
};

export default LeavesTable;
