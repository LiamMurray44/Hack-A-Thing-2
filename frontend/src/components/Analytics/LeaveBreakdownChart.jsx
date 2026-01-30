// Written by Claude Code on 2026-01-29
// User prompt: Create pie chart for leave breakdown (pre-leave, on leave, return from leave)

import React, { useMemo } from 'react';
import { parseISO, isAfter, isBefore, startOfToday } from 'date-fns';
import './LeaveBreakdownChart.css';

const LeaveBreakdownChart = ({ leaveRequests = [] }) => {
  const breakdownData = useMemo(() => {
    const today = startOfToday();

    let preLeave = 0;
    let onLeave = 0;
    let returnedFromLeave = 0;

    if (Array.isArray(leaveRequests) && leaveRequests.length > 0) {
      leaveRequests.forEach(req => {
        try {
          if (!req?.leave?.start_date || !req?.leave?.end_date) return;

          const leaveStart = parseISO(req.leave.start_date);
          const leaveEnd = parseISO(req.leave.end_date);

          if (isAfter(leaveStart, today)) {
            // Leave hasn't started yet (strictly in the future)
            preLeave++;
          } else if (isBefore(leaveEnd, today)) {
            // Leave has ended (strictly in the past)
            returnedFromLeave++;
          } else {
            // Currently on leave (includes today if start_date or end_date is today)
            onLeave++;
          }
        } catch (error) {
          console.error('Error parsing leave dates:', req, error);
        }
      });
    }

    const total = preLeave + onLeave + returnedFromLeave;

    return {
      preLeave: { count: preLeave, percentage: total > 0 ? (preLeave / total) * 100 : 0 },
      onLeave: { count: onLeave, percentage: total > 0 ? (onLeave / total) * 100 : 0 },
      returnedFromLeave: { count: returnedFromLeave, percentage: total > 0 ? (returnedFromLeave / total) * 100 : 0 },
      total
    };
  }, [leaveRequests]);

  const { preLeave, onLeave, returnedFromLeave, total } = breakdownData;

  // Calculate pie chart segments
  const radius = 80;
  const circumference = 2 * Math.PI * radius;

  const preLeaveOffset = 0;
  const onLeaveOffset = (preLeave.percentage / 100) * circumference;
  const returnedOffset = ((preLeave.percentage + onLeave.percentage) / 100) * circumference;

  if (total === 0) {
    return (
      <div className="breakdown-chart-container">
        <div className="breakdown-header">
          <h3>Leave Status Breakdown</h3>
          <p className="breakdown-subtitle">Current leave status distribution</p>
        </div>
        <div className="breakdown-empty">
          <div className="empty-icon">📊</div>
          <p>No leave requests to display</p>
        </div>
      </div>
    );
  }

  return (
    <div className="breakdown-chart-container">
      <div className="breakdown-header">
        <h3>Leave Status Breakdown</h3>
        <p className="breakdown-subtitle">{total} total leave request{total !== 1 ? 's' : ''}</p>
      </div>

      <div className="breakdown-content">
        <div className="pie-chart">
          <svg viewBox="0 0 200 200" className="pie-svg">
            {/* Background circle */}
            <circle
              cx="100"
              cy="100"
              r={radius}
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="40"
            />

            {/* Pre-leave segment (blue) */}
            {preLeave.count > 0 && (
              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="none"
                stroke="#3b82f6"
                strokeWidth="40"
                strokeDasharray={`${(preLeave.percentage / 100) * circumference} ${circumference}`}
                strokeDashoffset={-preLeaveOffset}
                transform="rotate(-90 100 100)"
                className="pie-segment"
              />
            )}

            {/* On leave segment (green) */}
            {onLeave.count > 0 && (
              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="none"
                stroke="#10b981"
                strokeWidth="40"
                strokeDasharray={`${(onLeave.percentage / 100) * circumference} ${circumference}`}
                strokeDashoffset={-onLeaveOffset}
                transform="rotate(-90 100 100)"
                className="pie-segment"
              />
            )}

            {/* Returned from leave segment (gray) */}
            {returnedFromLeave.count > 0 && (
              <circle
                cx="100"
                cy="100"
                r={radius}
                fill="none"
                stroke="#6b7280"
                strokeWidth="40"
                strokeDasharray={`${(returnedFromLeave.percentage / 100) * circumference} ${circumference}`}
                strokeDashoffset={-returnedOffset}
                transform="rotate(-90 100 100)"
                className="pie-segment"
              />
            )}

            {/* Center text */}
            <text
              x="100"
              y="95"
              textAnchor="middle"
              className="pie-center-number"
            >
              {total}
            </text>
            <text
              x="100"
              y="115"
              textAnchor="middle"
              className="pie-center-label"
            >
              Total
            </text>
          </svg>
        </div>

        <div className="breakdown-legend">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#3b82f6' }}></div>
            <div className="legend-details">
              <div className="legend-label">Pre-Leave</div>
              <div className="legend-value">
                {preLeave.count} ({preLeave.percentage.toFixed(0)}%)
              </div>
            </div>
          </div>

          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#10b981' }}></div>
            <div className="legend-details">
              <div className="legend-label">On Leave</div>
              <div className="legend-value">
                {onLeave.count} ({onLeave.percentage.toFixed(0)}%)
              </div>
            </div>
          </div>

          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#6b7280' }}></div>
            <div className="legend-details">
              <div className="legend-label">Returned</div>
              <div className="legend-value">
                {returnedFromLeave.count} ({returnedFromLeave.percentage.toFixed(0)}%)
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeaveBreakdownChart;
