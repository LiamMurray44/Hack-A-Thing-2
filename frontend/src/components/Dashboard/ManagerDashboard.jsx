import React, { useState, useEffect } from 'react';
import DashboardHeader from '../Shared/DashboardHeader';
import Timeline from '../Timeline/Timeline';
import AlertBanner from '../Alerts/AlertBanner';
import NotificationsList from '../Notifications/NotificationsList';
import LeavesTable from '../Leaves/LeavesTable';
import { useUser } from '../../contexts/UserContext';
import { useFilteredLeaves } from '../../hooks/useFilteredLeaves';
import { leaveRequestsAPI, timelineAPI } from '../../services/api';
import './ManagerDashboard.css';

const ManagerDashboard = () => {
  const { mockUserData } = useUser();
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('timeline');

  const filteredLeaves = useFilteredLeaves(leaveRequests, 'manager', mockUserData);

  useEffect(() => {
    fetchLeaveRequests();
  }, []);

  useEffect(() => {
    if (selectedRequest) {
      fetchTimelineAndCompliance(selectedRequest.id);
    }
  }, [selectedRequest]);

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

  const handleSelectRequest = (request) => {
    setSelectedRequest(request);
    setActiveTab('timeline');
  };

  const handleBackToTable = () => {
    setSelectedRequest(null);
  };

  const pendingCount = filteredLeaves.filter(req => req.status === 'pending').length;

  if (loading) {
    return (
      <div className="manager-dashboard">
        <DashboardHeader />
        <div className="manager-loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="manager-dashboard">
      <DashboardHeader />

      <div className="manager-content">
        {!selectedRequest ? (
          <>
            <div className="manager-overview">
              <h2>Team Overview</h2>
              <div className="overview-cards">
                <div className="overview-card">
                  <div className="card-icon">👥</div>
                  <div className="card-content">
                    <div className="card-value">{mockUserData.teamIds?.length || 0}</div>
                    <div className="card-label">Team Members</div>
                  </div>
                </div>
                <div className="overview-card">
                  <div className="card-icon">📋</div>
                  <div className="card-content">
                    <div className="card-value">{filteredLeaves.length}</div>
                    <div className="card-label">Total Requests</div>
                  </div>
                </div>
                <div className="overview-card">
                  <div className="card-icon">⏳</div>
                  <div className="card-content">
                    <div className="card-value">{pendingCount}</div>
                    <div className="card-label">Pending Requests</div>
                  </div>
                </div>
              </div>
            </div>

            {filteredLeaves.length > 0 ? (
              <div className="manager-table-section">
                <h3>Team Leave Requests</h3>
                <LeavesTable
                  leaveRequests={filteredLeaves}
                  onSelectRequest={handleSelectRequest}
                />
              </div>
            ) : (
              <div className="manager-empty">
                <h3>No Team Requests Found</h3>
                <p>Your team members don't have any leave requests in the system.</p>
              </div>
            )}
          </>
        ) : (
          <div className="manager-detail-view">
            <button className="btn-back" onClick={handleBackToTable}>
              ← Back to Team Requests
            </button>

            <div className="request-details">
              <h2>{selectedRequest.employee.name}</h2>
              <div className="request-meta">
                <span>SSN: ***-**-{selectedRequest.employee.ssn_last4}</span>
                <span>Phone: {selectedRequest.employee.phone}</span>
                {selectedRequest.employee.email && (
                  <span>Email: {selectedRequest.employee.email}</span>
                )}
                <span>Location: {selectedRequest.employee.state}</span>
                <span>FMLA Eligible: {selectedRequest.fmla_eligible ? 'Yes' : 'No'}</span>
              </div>
            </div>

            {compliance && <AlertBanner compliance={compliance} />}

            <div className="manager-tabs">
              <button
                className={`manager-tab ${activeTab === 'timeline' ? 'active' : ''}`}
                onClick={() => setActiveTab('timeline')}
              >
                Timeline
              </button>
              <button
                className={`manager-tab ${activeTab === 'notifications' ? 'active' : ''}`}
                onClick={() => setActiveTab('notifications')}
              >
                Notifications
              </button>
            </div>

            <div className="manager-tab-content">
              {activeTab === 'timeline' && (
                <Timeline
                  events={timeline}
                  leaveStartDate={selectedRequest.leave.start_date}
                  leaveEndDate={selectedRequest.leave.end_date}
                />
              )}

              {activeTab === 'notifications' && (
                <NotificationsList requestId={selectedRequest.id} />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ManagerDashboard;

// Written by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards
