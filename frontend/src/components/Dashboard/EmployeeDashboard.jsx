import React, { useState, useEffect } from 'react';
import DashboardHeader from '../Shared/DashboardHeader';
import Timeline from '../Timeline/Timeline';
import AlertBanner from '../Alerts/AlertBanner';
import NotificationsList from '../Notifications/NotificationsList';
import { useUser } from '../../contexts/UserContext';
import { useFilteredLeaves } from '../../hooks/useFilteredLeaves';
import { leaveRequestsAPI, timelineAPI } from '../../services/api';
import './EmployeeDashboard.css';

const EmployeeDashboard = () => {
  const { mockUserData } = useUser();
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('timeline');

  const filteredLeaves = useFilteredLeaves(leaveRequests, 'employee', mockUserData);
  const myRequest = filteredLeaves.length > 0 ? filteredLeaves[0] : null;

  useEffect(() => {
    fetchLeaveRequests();
  }, []);

  useEffect(() => {
    if (myRequest) {
      fetchTimelineAndCompliance(myRequest.id);
    }
  }, [myRequest]);

  const fetchLeaveRequests = async () => {
    try {
      setLoading(true);
      const response = await leaveRequestsAPI.getAll();
      setLeaveRequests(response.data);
    } catch (err) {
      console.error('Error fetching leave requests:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTimelineAndCompliance = async (requestId) => {
    try {
      const [timelineRes, complianceRes] = await Promise.all([
        timelineAPI.getTimeline(requestId),
        timelineAPI.getCompliance(requestId),
      ]);
      setTimeline(timelineRes.data);
      setCompliance(complianceRes.data);
    } catch (err) {
      console.error('Error fetching timeline/compliance:', err);
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

  if (loading) {
    return (
      <div className="employee-dashboard">
        <DashboardHeader />
        <div className="employee-loading">Loading...</div>
      </div>
    );
  }

  if (!myRequest) {
    return (
      <div className="employee-dashboard">
        <DashboardHeader />
        <div className="employee-empty">
          <h2>No Leave Request Found</h2>
          <p>You don't have any leave requests in the system.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="employee-dashboard">
      <DashboardHeader />

      <div className="employee-content">
        <div className="employee-info-card">
          <h2>Your Leave Request</h2>
          <div className="employee-details">
            <div className="detail-row">
              <span className="detail-label">Name:</span>
              <span className="detail-value">{myRequest.employee.name}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">SSN:</span>
              <span className="detail-value">***-**-{myRequest.employee.ssn_last4}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Location:</span>
              <span className="detail-value">{myRequest.employee.state}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Status:</span>
              <span className={`status-badge ${getStatusBadgeClass(myRequest.status)}`}>
                {myRequest.status}
              </span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Leave Dates:</span>
              <span className="detail-value">
                {new Date(myRequest.leave.start_date).toLocaleDateString()} - {new Date(myRequest.leave.end_date).toLocaleDateString()}
              </span>
            </div>
            <div className="detail-row">
              <span className="detail-label">FMLA Eligible:</span>
              <span className="detail-value">{myRequest.fmla_eligible ? 'Yes' : 'No'}</span>
            </div>
          </div>
        </div>

        {compliance && (
          <div className="employee-compliance">
            <AlertBanner compliance={compliance} />
          </div>
        )}

        <div className="employee-tabs">
          <button
            className={`employee-tab ${activeTab === 'timeline' ? 'active' : ''}`}
            onClick={() => setActiveTab('timeline')}
          >
            Timeline
          </button>
          <button
            className={`employee-tab ${activeTab === 'notifications' ? 'active' : ''}`}
            onClick={() => setActiveTab('notifications')}
          >
            Notifications
          </button>
        </div>

        <div className="employee-tab-content">
          {activeTab === 'timeline' && (
            <Timeline
              events={timeline}
              leaveStartDate={myRequest.leave.start_date}
              leaveEndDate={myRequest.leave.end_date}
            />
          )}

          {activeTab === 'notifications' && (
            <NotificationsList requestId={myRequest.id} />
          )}
        </div>
      </div>
    </div>
  );
};

export default EmployeeDashboard;

// Written by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards
