import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext(undefined);

const MOCK_USERS = {
  employee: {
    userId: 'emp-001',
    name: 'John Doe'
  },
  manager: {
    userId: 'mgr-001',
    name: 'Sarah Manager',
    teamIds: ['John Doe', 'Jane Smith', 'Bob Johnson']
  },
  hr_admin: {
    userId: 'hr-001',
    name: 'HR Admin'
  }
};

export function UserProvider({ children }) {
  const [role, setRoleState] = useState(null);

  const setRole = (newRole) => {
    setRoleState(newRole);
  };

  const clearRole = () => {
    setRoleState(null);
  };

  const mockUserData = role ? MOCK_USERS[role] : null;

  const value = {
    role,
    mockUserData,
    setRole,
    clearRole
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}

// Written by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards
