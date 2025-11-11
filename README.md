# FastAPI Supabase Backend API

A FastAPI backend API integrated with Supabase Python client. Supports CRUD operations, robust error handling, and optimized for serverless environments like Vercel.

## Features

- Async CRUD API for task management with Supabase
- Supabase transaction pooler support (port 6543) with SSL
- Supabase Python client integration for direct API access
- Detailed validation and database error handling
- Ready for Vercel deployment with environment variable management
- Global exception handling for stability

## Setup Instructions

1. Clone repository  
2. Create and activate a virtual environment  
3. Install dependencies:
4. pip install -r requirements.txt

# Setup environment variables:

`SUPABASE_URL=your_supabase_url`
`SUPABASE_ANON_KEY=your_supabase_anon_key`

Run migrations : `Run Alembic migrations `
Start the FastAPI app : `npm run dev`

## API Endpoints

- `GET /tasks` - List all tasks  
- `GET /tasks/{task_id}` - Get a specific task  
- `POST /tasks` - Create a new task  
- `POST /tasks/{task_id}` - Update an existing task  
- `DELETE /tasks/{task_id}` - Delete a task  