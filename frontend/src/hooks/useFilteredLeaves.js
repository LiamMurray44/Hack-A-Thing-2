import { useMemo } from 'react';

export function useFilteredLeaves(leaveRequests, role, userData) {
  return useMemo(() => {
    if (!leaveRequests || !role || !userData) {
      return [];
    }

    if (role === 'hr_admin') {
      return leaveRequests;
    }

    if (role === 'employee') {
      // Filter to requests where employee.name matches mock user
      return leaveRequests.filter(req =>
        req.employee?.name === userData.name
      );
    }

    if (role === 'manager') {
      // Filter to requests where employee.name matches team members
      return leaveRequests.filter(req =>
        userData.teamIds?.includes(req.employee?.name)
      );
    }

    return [];
  }, [leaveRequests, role, userData]);
}

// Written by Claude Code on 2026-02-04
// User prompt: Implement the following plan: Role-Based Dashboards
