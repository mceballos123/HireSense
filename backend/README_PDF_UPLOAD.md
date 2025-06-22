# PDF Resume Upload System

This system provides PDF-to-text conversion for resume uploads, integrated with the hiring agents system.

## Features

- 📄 **PDF Text Extraction**: Extracts text content from PDF resumes
- 🤖 **AI Analysis**: Uses ASI:One LLM to analyze resume content
- 🚀 **FastAPI Backend**: RESTful API for file uploads
- ⚡ **Real-time Processing**: Immediate analysis results
- 🎨 **Modern UI**: React frontend with file upload interface

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Upload Server

```bash
cd backend
python start_upload_server.py
```

The server will start on `http://localhost:8080`

### 3. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available on `http://localhost:3000`

## Usage

### Frontend Usage

1. Navigate to `/resume-uploads` in your browser
2. Enter the candidate's name
3. Select a PDF file (max 10MB)
4. Click "Upload & Analyze"
5. View the extracted information and AI analysis

### API Usage

**Endpoint**: `POST /upload-resume`

**Parameters**:
- `file`: PDF file (multipart/form-data)
- `candidate_name`: Candidate's name (form field)

**Response**:
```json
{
  "candidate_name": "John Doe",
  "skills": ["Python", "JavaScript", "React"],
  "experience_years": 5,
  "experience_level": "Senior",
  "key_achievements": ["Led development team", "Improved system performance"],
  "analysis": "Experienced software engineer with strong technical skills...",
  "status": "success"
}
```

### Example cURL Request

```bash
curl -X POST "http://localhost:8080/upload-resume" \
  -F "file=@resume.pdf" \
  -F "candidate_name=John Doe"
```

## Testing

### Test PDF Parser

```bash
cd backend
python test_pdf_parser.py
```

### Health Check

```bash
curl http://localhost:8080/health
```

## File Structure

```
backend/
├── hiring_agents/
│   ├── pdf_parser.py          # PDF text extraction utility
│   ├── resume_parser_agent.py # Resume analysis agent
│   └── ...
├── file_upload_server.py      # FastAPI server
├── start_upload_server.py     # Server startup script
├── test_pdf_parser.py         # PDF parser tests
└── requirements.txt           # Dependencies

frontend/
└── src/components/dashboard/
    └── resume-uploads-content.jsx  # Upload UI component
```

## Supported File Types

- ✅ **PDF** (.pdf) - Fully supported
- ⚠️ **DOC/DOCX** (.doc, .docx) - Planned for future implementation

## Configuration

The system uses the following default settings:

- **Upload Server Port**: 8080
- **Max File Size**: 10MB
- **Supported Types**: PDF only (currently)
- **CORS Origins**: `http://localhost:3000`

## Troubleshooting

### Common Issues

1. **"Could not extract text from PDF"**
   - PDF might be image-based (scanned document)
   - Try with a text-based PDF

2. **"Network error: Could not connect to server"**
   - Ensure the upload server is running on port 8080
   - Check CORS configuration

3. **"LLM API error"**
   - Verify ASI:One API key is configured
   - Check internet connection

### Debug Mode

Start the server with debug logging:

```bash
cd backend
python -c "
import uvicorn
uvicorn.run('file_upload_server:app', host='0.0.0.0', port=8080, reload=True, log_level='debug')
"
```

## Integration with Hiring Agents

The PDF upload system integrates with the existing hiring agents by:

1. Extracting text from uploaded PDFs
2. Sending the text to the Resume Parser Agent
3. Using the same LLM analysis pipeline
4. Returning structured candidate data

This allows the full hiring pipeline (job matching, debate system, etc.) to work with uploaded resume files. 