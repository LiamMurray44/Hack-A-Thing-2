// Written by Claude Code on 2026-01-29
// User prompt: Restructure with Dashboard and Leaves tabs in left sidebar

import React, { useState, useEffect } from 'react';
import Timeline from '../Timeline/Timeline';
import AlertBanner from '../Alerts/AlertBanner';
import NotificationsList from '../Notifications/NotificationsList';
import LeaveRequestForm from '../LeaveRequest/LeaveRequestForm';
import LeaveHistogram from '../Analytics/LeaveHistogram';
import LeaveBreakdownChart from '../Analytics/LeaveBreakdownChart';
import PendingLeavesTable from '../Analytics/PendingLeavesTable';
import LeavesTable from '../Leaves/LeavesTable';
import { leaveRequestsAPI, timelineAPI, notificationsAPI } from '../../services/api';
import { formatDate } from '../../utils/dateFormatter';
import './Dashboard.css';

const Dashboard = () => {
  const [leaveRequests, setLeaveRequests] = useState([]);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mainView, setMainView] = useState('dashboard'); // 'dashboard' | 'leaves'
  const [leavesTab, setLeavesTab] = useState('timeline'); // 'timeline' | 'notifications'
  const [showForm, setShowForm] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

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
      if (response.data.length > 0 && !selectedRequest) {
        setSelectedRequest(response.data[0]);
      }
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

  const handleCreateSuccess = (newRequest) => {
    setLeaveRequests([...leaveRequests, newRequest]);
    setSelectedRequest(newRequest);
    setShowForm(false);
    setLeavesTab('timeline');
  };

  const handleSendNotification = async (type) => {
    if (!selectedRequest) return;

    try {
      await notificationsAPI.create({
        request_id: selectedRequest.id,
        notification_type: type,
      });
      if (leavesTab === 'notifications') {
        // Refresh will happen automatically in NotificationsList
      } else {
        setLeavesTab('notifications');
      }
    } catch (err) {
      console.error('Error creating notification:', err);
    }
  };

  const handleSelectRequestFromTable = (request) => {
    setSelectedRequest(request);
    setMainView('leaves');
    setLeavesTab('timeline');
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
    return <div className="dashboard-loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>FMLA Compliance Tracker</h1>
        <p>HR Dashboard for Managing Leave Requests</p>
      </header>

      <div className="dashboard-layout">
        {/* Left Navigation Sidebar */}
        <aside className={`dashboard-nav ${sidebarCollapsed ? 'collapsed' : ''}`}>
          <button
            className="nav-collapse-btn"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {sidebarCollapsed ? '→' : '←'}
          </button>
          <button
            className={`nav-item ${mainView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setMainView('dashboard')}
          >
            <span className="nav-icon">📊</span>
            <span className="nav-label">Dashboard</span>
          </button>
          <button
            className={`nav-item ${mainView === 'leaves' ? 'active' : ''}`}
            onClick={() => setMainView('leaves')}
          >
            <span className="nav-icon">📋</span>
            <span className="nav-label">Leaves</span>
          </button>
        </aside>

        {/* Main Content Area */}
        <main className="dashboard-content">
          {mainView === 'dashboard' ? (
            /* Dashboard View */
            <div className="dashboard-view">
              <h2 className="view-title">Dashboard Overview</h2>

              <div className="dashboard-grid">
                {/* Top row: Histogram and Pie Chart */}
                <div className="dashboard-chart-row">
                  <div className="chart-container histogram-container-wrapper">
                    <LeaveHistogram leaveRequests={leaveRequests} />
                  </div>
                  <div className="chart-container breakdown-container-wrapper">
                    <LeaveBreakdownChart leaveRequests={leaveRequests} />
                  </div>
                </div>

                {/* Bottom row: Pending Leaves Table */}
                <div className="dashboard-table-row">
                  <PendingLeavesTable
                    leaveRequests={leaveRequests}
                    onSelectRequest={handleSelectRequestFromTable}
                  />
                </div>
              </div>
            </div>
          ) : (
            /* Leaves View */
            <div className="leaves-view">
              <div className="leaves-header">
                <h2 className="view-title">Leave Management</h2>
                <button
                  className="btn-new-request"
                  onClick={() => setShowForm(!showForm)}
                >
                  {showForm ? '✕ Cancel' : '+ New Leave Request'}
                </button>
              </div>

              {showForm ? (
                <LeaveRequestForm onSuccess={handleCreateSuccess} />
              ) : selectedRequest ? (
                /* Detail View */
                <div className="leaves-detail-view">
                  <button
                    className="btn-back"
                    onClick={() => setSelectedRequest(null)}
                  >
                    ← Back to All Leaves
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

                  <div className="tabs">
                    <button
                      className={`tab ${leavesTab === 'timeline' ? 'active' : ''}`}
                      onClick={() => setLeavesTab('timeline')}
                    >
                      Timeline
                    </button>
                    <button
                      className={`tab ${leavesTab === 'notifications' ? 'active' : ''}`}
                      onClick={() => setLeavesTab('notifications')}
                    >
                      Notifications
                    </button>
                  </div>

                  <div className="tab-content">
                    {leavesTab === 'timeline' && (
                      <div>
                        <Timeline
                          events={timeline}
                          leaveStartDate={selectedRequest.leave.start_date}
                          leaveEndDate={selectedRequest.leave.end_date}
                        />

                        <div className="notification-triggers">
                          <h4>Send Test Notifications</h4>
                          <div className="trigger-buttons">
                            <button onClick={() => handleSendNotification('certification_due')}>
                              Certification Due
                            </button>
                            <button onClick={() => handleSendNotification('cure_window')}>
                              Cure Window
                            </button>
                            <button onClick={() => handleSendNotification('recertification_due')}>
                              Recertification
                            </button>
                            <button onClick={() => handleSendNotification('approval_notice')}>
                              Approval
                            </button>
                            <button onClick={() => handleSendNotification('missing_docs')}>
                              Missing Docs
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    {leavesTab === 'notifications' && (
                      <NotificationsList requestId={selectedRequest.id} />
                    )}
                  </div>
                </div>
              ) : (
                /* Table View */
                <LeavesTable
                  leaveRequests={leaveRequests}
                  onSelectRequest={setSelectedRequest}
                />
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
