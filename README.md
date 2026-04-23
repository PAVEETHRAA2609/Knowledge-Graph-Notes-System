# Knowledge-Graph-Notes-System
A full-stack application that allows users to create notes, connect them using bidirectional links, and visualize relationships as a graph.

Built with FastAPI + SQLite (Backend) and ReactJS (Frontend), with automatic link detection using [[Note Title]] syntax — similar to tools like Obsidian.

 Features
 Notes Management
Create notes with title, content, and tags
Prevent duplicate note titles
Search notes by keyword
Filter notes by tags
Linking System
Manual linking via API
 Auto-link detection using [[Note Title]]
Prevent:
Self-links
Duplicate links
 Bidirectional Relationships
Forward links (A → B)
Backlinks automatically available (B ← A)
Graph Visualization
Interactive graph using Cytoscape
Node click → view note
Hover → highlight connections
Clean layout (COSE algorithm)
 Backend Architecture
FastAPI with OpenAPI (Swagger UI)
SQLite database
SQLAlchemy ORM
Dependency Injection for DB
Proper error handling (4xx / 5xx)
 Tech Stack
Layer	Technology
Backend	FastAPI
Database	SQLite
ORM	SQLAlchemy
Frontend	ReactJS
Graph UI	Cytoscape.js
API Client	Axios
 Project Structure
knowledge-graph-system/
│
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── database/
│
├── frontend/
│   ├── src/
│   ├── public/
│
├── requirements.txt
├── main.py
├── README.md
 Setup Instructions
 1. Clone Repository
git clone <your-repo-url>
cd knowledge-graph-system
 2. Backend Setup (FastAPI)
python -m venv env
env\Scripts\activate   # Windows
# source env/bin/activate (Mac/Linux)

pip install -r requirements.txt
 3. Run Backend
uvicorn main:app --reload

 Open Swagger UI:

http://127.0.0.1:8000/docs
 4. Frontend Setup (React)
cd frontend
npm install
 5. Run Frontend
npm start

 Open:

http://localhost:3000
 API Endpoints
Method	Endpoint	Description
POST	/notes/	Create a note
GET	/notes/	Get all notes (search/filter)
GET	/notes/{id}	Get single note
PATCH	/notes/{id}/link	Manually link notes
GET	/notes/graph/	Get graph data
 Auto-Linking Feature

You can create links automatically using:

[[Note Title]]
Example:
Graph Theory connects to [[Data Structures]]

 Automatically creates:

Graph Theory → Data Structures

 And backlink:

Data Structures ← Graph Theory
 Graph Output Example
{
  "nodes": [
    { "id": 1, "title": "Graph Theory" },
    { "id": 2, "title": "Data Structures" }
  ],
  "edges": [
    { "source": 1, "target": 2 }
  ]
}
**Key Design Decisions
**Used many-to-many relationships for tags and links
Implemented graph structure using adjacency lists
Used regex parsing for auto-link detection
Ensured data integrity rules:
No duplicate notes
No self-links
No duplicate edges
**Testing (Manual)**

Use Swagger UI:

/docs

Steps:

Create notes
Add [[links]] in content
Fetch graph
View in frontend
** Future Improvements**
**Backlinks UI panel
Clickable [[links]] in note content
Real-time updates (WebSockets)
Tag suggestions dropdown
Graph filtering by tag
 Author

Paveethraa

 Final Note

This project demonstrates:

Full-stack development
API design (OpenAPI)
Graph data modeling
Real-world feature implementation
