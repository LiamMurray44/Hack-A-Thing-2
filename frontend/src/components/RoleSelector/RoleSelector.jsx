import React from 'react';
import { useUser } from '../../contexts/UserContext';
import './RoleSelector.css';

function RoleSelector() {
  const { setRole } = useUser();

  const roles = [
    {
      id: 'employee',
      icon: '👤',
      title: 'Employee',
      description: 'View your leave request and timeline',
      buttonText: 'Sign In as Employee'
    },
    {
      id: 'manager',
      icon: '👥',
      title: 'Manager',
      description: 'View team leave requests',
      buttonText: 'Sign In as Manager'
    },
    {
      id: 'hr_admin',
      icon: '🏢',
      title: 'HR Admin',
      description: 'Full system access with analytics',
      buttonText: 'Sign In as HR Admin'
    }
  ];

  return (
    <div className="role-selector-container">
      <div className="role-selector-header">
        <h1>FMLA Compliance Tracker</h1>
        <p>Select your role to continue</p>
      </div>
      <div className="role-cards">
        {roles.map(role => (
          <div key={role.id} className="role-card">
            <div className="role-icon">{role.icon}</div>
            <h2 className="role-title">{role.title}</h2>
            <p className="role-description">{role.description}</p>
            <button
              className="role-button"
              onClick={() => setRole(role.id)}
            >
              {role.buttonText}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RoleSelector;

// Written by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards
