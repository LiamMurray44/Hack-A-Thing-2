# Claude Code Configuration

## Citation Format

All code written by Claude Code should include:

"Written by Claude Code on {date}"
"User prompt: {prompt}"

## Project Context

This is an FMLA Deadline & Timeline Tracker Prototype built with:
- Backend: Python + FastAPI
- Frontend: React
- Storage: JSON files
- Focus: Demonstrating FMLA compliance deadline calculations

## Key Implementation Notes

- All FMLA deadlines use **calendar days** (not business days)
- Certification deadline = min(15 days after notice, leave start date)
- Cure window is always 7 calendar days after certification deadline
- Recertification: 30 days (serious condition) or 6 months (chronic condition)
