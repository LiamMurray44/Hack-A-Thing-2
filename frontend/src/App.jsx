// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype
// Modified by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards

import React from 'react';
import { UserProvider, useUser } from './contexts/UserContext';
import RoleSelector from './components/RoleSelector/RoleSelector';
import EmployeeDashboard from './components/Dashboard/EmployeeDashboard';
import ManagerDashboard from './components/Dashboard/ManagerDashboard';
import HRAdminDashboard from './components/Dashboard/HRAdminDashboard';
import './App.css';

function AppContent() {
  const { role } = useUser();

  if (!role) {
    return <RoleSelector />;
  }

  if (role === 'employee') {
    return <EmployeeDashboard />;
  }

  if (role === 'manager') {
    return <ManagerDashboard />;
  }

  if (role === 'hr_admin') {
    return <HRAdminDashboard />;
  }

  return null;
}

function App() {
  return (
    <UserProvider>
      <div className="App">
        <AppContent />
      </div>
    </UserProvider>
  );
}

export default App;
