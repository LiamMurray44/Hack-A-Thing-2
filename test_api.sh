#!/bin/bash
# Written by Claude Code on 2026-01-29
# User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

echo "Testing FMLA API..."
echo ""

# Test 1: Create a leave request
echo "1. Creating leave request..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/leave-requests/ \
  -H "Content-Type: application/json" \
  -d '{
    "employee": {
      "name": "Jane Doe",
      "ssn_last4": "1234",
      "phone": "5555555555",
      "email": "jane.doe@example.com"
    },
    "leave": {
      "start_date": "2025-02-20",
      "end_date": "2025-04-01",
      "intermittent": false,
      "condition_type": "serious"
    },
    "medical_provider": {
      "name": "Dr. John Smith",
      "signature_present": false,
      "date_signed": null
    },
    "compliance_flags": ["missing_physician_phone", "missing_signature"]
  }')

REQUEST_ID=$(echo $RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Created request with ID: $REQUEST_ID"
echo ""

# Test 2: Get timeline
echo "2. Getting timeline..."
curl -s http://localhost:8000/api/timeline/$REQUEST_ID | jq -r '.[] | "\(.title) - \(.event_date) (\(.status))"'
echo ""

# Test 3: Get compliance status
echo "3. Getting compliance status..."
curl -s http://localhost:8000/api/timeline/$REQUEST_ID/compliance | jq '{is_compliant, at_risk, risk_level, days_until_certification_deadline}'
echo ""

# Test 4: Create notification
echo "4. Creating certification due notification..."
curl -s -X POST "http://localhost:8000/api/notifications/?request_id=$REQUEST_ID&notification_type=certification_due" | jq '{id, type, subject}'
echo ""

echo "✅ API tests complete!"
