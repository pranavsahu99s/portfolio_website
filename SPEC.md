# Application Specifications

## Status: FINALIZED

## Database Models

### Skill
- `id`: Integer (Primary Key)
- `name`: String
- `icon_class`: String (Lucide icon name, e.g., 'code-2')

### Experience
- `id`: Integer (Primary Key)
- `period`: String (e.g., 'July 2025 - Present')
- `title`: String
- `company`: String
- `description`: Text
- `image_path`: String

### Project
- `id`: Integer (Primary Key)
- `title`: String
- `description`: Text
- `tags`: String (Comma-separated or JSON list)
- `image_path`: String
- `github_link`: String
- `external_link`: String

### Education
- `id`: Integer (Primary Key)
- `period`: String
- `degree`: String
- `institution`: String
- `description`: Text

## AI Resume Parser Payload (B.L.A.S.T Data-First Rule)

### Input Payload to API
```json
{
  "resume_text": "string (The extracted text from the uploaded PDF/text file)"
}
```

### Output Payload from API (Gemini Expected Response Shape)
```json
{
  "skills": [
    {
      "name": "string",
      "icon_class": "string (closest lucide icon name)"
    }
  ],
  "experience": [
    {
      "period": "string",
      "title": "string",
      "company": "string",
      "description": "string",
      "image_path": "string (default null or placeholder)"
    }
  ]
}
```