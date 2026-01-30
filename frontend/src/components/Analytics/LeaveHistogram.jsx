// Written by Claude Code on 2026-01-29
// User prompt: Create histogram showing upcoming leaves by month (all 12 months)

import React, { useMemo } from 'react';
import { format, parseISO, isAfter, isSameDay, startOfToday, addMonths, startOfMonth } from 'date-fns';
import './LeaveHistogram.css';

const LeaveHistogram = ({ leaveRequests = [] }) => {
  const histogramData = useMemo(() => {
    if (!Array.isArray(leaveRequests) || leaveRequests.length === 0) {
      // Return empty histogram data if no requests
      const today = startOfToday();
      const currentMonthStart = startOfMonth(today);
      const allMonths = [];
      for (let i = 0; i < 12; i++) {
        const monthDate = addMonths(currentMonthStart, i);
        allMonths.push({
          monthKey: format(monthDate, 'yyyy-MM'),
          label: format(monthDate, 'MMM yyyy'),
          count: 0,
          leaves: []
        });
      }
      return allMonths;
    }

    const today = startOfToday();
    const currentMonthStart = startOfMonth(today);

    // Generate all 12 months starting from current month
    const allMonths = [];
    for (let i = 0; i < 12; i++) {
      const monthDate = addMonths(currentMonthStart, i);
      const monthKey = format(monthDate, 'yyyy-MM');
      const monthLabel = format(monthDate, 'MMM yyyy');

      allMonths.push({
        monthKey,
        label: monthLabel,
        count: 0,
        leaves: []
      });
    }

    // Filter for upcoming leaves only (start date is today or in the future)
    const upcomingLeaves = leaveRequests.filter(req => {
      try {
        if (!req?.leave?.start_date) return false;
        const leaveStart = parseISO(req.leave.start_date);
        // Include leaves starting today OR after today
        return isAfter(leaveStart, today) || isSameDay(leaveStart, today);
      } catch (error) {
        console.error('Error parsing date:', req?.leave?.start_date, error);
        return false;
      }
    });

    // Populate counts for months that have leaves
    upcomingLeaves.forEach(req => {
      try {
        const leaveStart = parseISO(req.leave.start_date);
        const monthKey = format(leaveStart, 'yyyy-MM');

        const monthData = allMonths.find(m => m.monthKey === monthKey);
        if (monthData) {
          monthData.count += 1;
          monthData.leaves.push(req);
        }
      } catch (error) {
        console.error('Error processing leave:', req, error);
      }
    });

    return allMonths;
  }, [leaveRequests]);

  const maxCount = Math.max(...histogramData.map(d => d.count), 1);
  const totalUpcoming = histogramData.reduce((sum, d) => sum + d.count, 0);

  // Generate y-axis labels (going up by 1)
  const yAxisLabels = [];
  for (let i = maxCount; i >= 0; i--) {
    yAxisLabels.push(i);
  }

  return (
    <div className="histogram-container">
      <div className="histogram-header">
        <h3>Upcoming Leaves - Next 12 Months</h3>
        <p className="histogram-subtitle">
          {totalUpcoming > 0
            ? `${totalUpcoming} upcoming leave${totalUpcoming !== 1 ? 's' : ''} scheduled`
            : 'No upcoming leaves scheduled'}
        </p>
      </div>

      <div className="histogram-chart">
        <div className="histogram-y-axis">
          {yAxisLabels.map((label, idx) => (
            <div key={idx} className="y-axis-label">{label}</div>
          ))}
        </div>

        <div className="histogram-bars">
          {histogramData.map((data, index) => {
            const heightPercent = data.count > 0 ? (data.count / maxCount) * 100 : 0;
            const hasLeaves = data.count > 0;

            return (
              <div key={data.monthKey} className="histogram-bar-container">
                <div className="bar-wrapper">
                  <div
                    className={`histogram-bar ${!hasLeaves ? 'empty-bar' : ''}`}
                    style={{
                      height: hasLeaves ? `${heightPercent}%` : '8px',
                      animationDelay: `${index * 0.05}s`
                    }}
                  >
                    {hasLeaves && (
                      <>
                        <div className="bar-value-top">{data.count}</div>
                        <div className="bar-fill"></div>
                      </>
                    )}
                  </div>
                </div>
                <div className="bar-label">{data.label}</div>

                {/* Show employee names on hover (only if there are leaves) */}
                {hasLeaves && (
                  <div className="bar-tooltip">
                    <div className="tooltip-header">{data.label}</div>
                    <div className="tooltip-count">{data.count} leave{data.count !== 1 ? 's' : ''}</div>
                    <div className="tooltip-employees">
                      {data.leaves.map((leave, idx) => (
                        <div key={idx} className="tooltip-employee">
                          • {leave.employee.name}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <div className="histogram-legend">
        <div className="legend-item">
          <div className="legend-icon">📅</div>
          <span>Each bar represents leave requests starting in that month</span>
        </div>
        <div className="legend-item">
          <div className="legend-icon">👥</div>
          <span>Hover over bars to see employee details</span>
        </div>
      </div>
    </div>
  );
};

export default LeaveHistogram;
