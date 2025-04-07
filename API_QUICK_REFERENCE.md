# API Quick Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
```
Authorization: Bearer your-api-key
```

## Endpoints

### Start Interview
```
POST /start-interview
```
Start the interview process with all three agents.

**Request Body:**
```json
{
  "cv_url": "string",
  "job_description_url": "string",
  "company_website_url": "string",
  "cv_text": "string (optional)"
}
```

### Upload CV
```
POST /upload-cv
```
Upload a CV file for processing.

**Request:**
- Content-Type: multipart/form-data
- File: PDF file

## Response Codes

| Code | Description |
|------|-------------|
| 200  | Success     |
| 400  | Bad Request |
| 401  | Unauthorized|
| 500  | Server Error|

## Rate Limits
- 100 requests/minute
- 1000 requests/day

## WebSocket Events
```
ws://localhost:8000/api/v1/ws/interview
```
Events:
- interview_started
- agent_response
- interview_completed

## Common Headers
```
Authorization: Bearer your-api-key
Content-Type: application/json
Accept: application/json
```

## Error Response Format
```json
{
  "detail": "Error message"
}
```

## Example cURL Commands

### Start Interview
```bash
curl -X POST http://localhost:8000/api/v1/start-interview \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "cv_url": "https://example.com/cv.pdf",
    "job_description_url": "https://example.com/job",
    "company_website_url": "https://example.com"
  }'
```

### Upload CV
```bash
curl -X POST http://localhost:8000/api/v1/upload-cv \
  -H "Authorization: Bearer your-api-key" \
  -F "file=@/path/to/cv.pdf"
``` 