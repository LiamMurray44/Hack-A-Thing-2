import React from 'react';
import { useUser } from '../../contexts/UserContext';
import './DashboardHeader.css';

const ROLE_LABELS = {
  employee: 'Employee View',
  manager: 'Manager View',
  hr_admin: 'HR Admin View'
};

function DashboardHeader() {
  const { role, mockUserData, clearRole } = useUser();

  return (
    <div className="dashboard-header">
      <div className="dashboard-header-content">
        <div className="dashboard-header-left">
          <h1 className="dashboard-header-title">FMLA Compliance Tracker</h1>
          {role && (
            <span className={`role-badge role-badge-${role}`}>
              {ROLE_LABELS[role]}
            </span>
          )}
        </div>
        <div className="dashboard-header-right">
          {mockUserData && (
            <span className="user-name">{mockUserData.name}</span>
          )}
          <button
            className="switch-role-button"
            onClick={clearRole}
          >
            Switch Role
          </button>
        </div>
      </div>
    </div>
  );
}

export default DashboardHeader;

// Written by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards
