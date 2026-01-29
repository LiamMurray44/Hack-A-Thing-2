// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import React, { useState } from 'react';
import { leaveRequestsAPI } from '../../services/api';
import './LeaveRequestForm.css';

const LeaveRequestForm = ({ onSuccess }) => {
  const [jsonInput, setJsonInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sampleJSON = {
    employee: {
      name: 'Jane Doe',
      ssn_last4: '1234',
      phone: '(555) 555-5555',
      email: 'jane.doe@example.com',
    },
    leave: {
      start_date: '2025-02-01',
      end_date: '2025-04-01',
      intermittent: false,
      condition_type: 'serious',
    },
    medical_provider: {
      name: 'Dr. John Smith',
      signature_present: true,
      date_signed: '2025-01-20',
    },
    compliance_flags: ['missing_physician_phone'],
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = JSON.parse(jsonInput);
      const response = await leaveRequestsAPI.create(data);
      setJsonInput('');
      if (onSuccess) {
        onSuccess(response.data);
      }
    } catch (err) {
      console.error('Error creating leave request:', err);
      if (err instanceof SyntaxError) {
        setError('Invalid JSON format. Please check your input.');
      } else {
        setError(err.response?.data?.detail || 'Failed to create leave request');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadSampleData = () => {
    setJsonInput(JSON.stringify(sampleJSON, null, 2));
    setError(null);
  };

  return (
    <div className="leave-request-form">
      <h3>Create New FMLA Leave Request</h3>
      <p className="form-description">
        Paste JSON data from the PDF field extractor, or use the sample data.
      </p>

      <button
        type="button"
        className="btn-load-sample"
        onClick={loadSampleData}
      >
        Load Sample Data
      </button>

      <form onSubmit={handleSubmit}>
        <textarea
          className="json-input"
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          placeholder="Paste JSON data here..."
          rows={20}
          required
        />

        {error && <div className="form-error">{error}</div>}

        <div className="form-actions">
          <button
            type="submit"
            className="btn-submit"
            disabled={loading || !jsonInput}
          >
            {loading ? 'Creating...' : 'Create Leave Request'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default LeaveRequestForm;
