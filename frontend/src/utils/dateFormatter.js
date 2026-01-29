// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import { format, parseISO, differenceInDays } from 'date-fns';

export const formatDate = (dateString, formatStr = 'MMM dd, yyyy') => {
  if (!dateString) return '';
  try {
    const date = typeof dateString === 'string' ? parseISO(dateString) : dateString;
    return format(date, formatStr);
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString;
  }
};

export const formatDateTime = (dateString) => {
  return formatDate(dateString, 'MMM dd, yyyy HH:mm');
};

export const getDaysUntil = (dateString) => {
  if (!dateString) return null;
  try {
    const date = typeof dateString === 'string' ? parseISO(dateString) : dateString;
    return differenceInDays(date, new Date());
  } catch (error) {
    console.error('Error calculating days until:', error);
    return null;
  }
};

export const getDaysUntilText = (dateString) => {
  const days = getDaysUntil(dateString);
  if (days === null) return '';
  if (days < 0) return `${Math.abs(days)} days overdue`;
  if (days === 0) return 'Due today';
  if (days === 1) return '1 day remaining';
  return `${days} days remaining`;
};
