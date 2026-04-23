import React, { useEffect, useState } from "react";
import axios from "axios";
import GraphView from "./GraphView";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);
  const [search, setSearch] = useState("");
  const [filterTag, setFilterTag] = useState("");
  const [graph, setGraph] = useState(null);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");

  // -------------------------
  // FETCH NOTES
  // -------------------------
  const fetchNotes = async () => {
    const res = await axios.get(`${API}/notes/`);
    setNotes(res.data);
  };

  // -------------------------
  // FETCH GRAPH
  // -------------------------
  const fetchGraph = async () => {
    const res = await axios.get(`${API}/notes/graph/`);
    setGraph(res.data);
  };

  // -------------------------
  // CREATE NOTE
  // -------------------------
  const createNote = async () => {
    await axios.post(`${API}/notes/`, {
      title,
      content,
      tags: tags.split(",").map(t => t.trim())
    });

    setTitle("");
    setContent("");
    setTags("");

    fetchNotes();
    fetchGraph();
  };

  // -------------------------
  // DARK MODE
  // -------------------------
  const toggleDark = () => {
    document.body.classList.toggle("dark");
  };

  // -------------------------
  // LOAD DATA
  // -------------------------
  useEffect(() => {
    fetchNotes();
    fetchGraph();
  }, []);

  return (
    <div className="container">

      <h1>Knowledge Graph Notes</h1>

      <button onClick={toggleDark}>Toggle Dark Mode</button>

      {/* CREATE NOTE */}
      <div className="form-card">
        <h2>Create Note</h2>

        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <input
          placeholder="Tags (comma separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
        />

        <button onClick={createNote}>Create Note</button>
      </div>

      {/* SEARCH */}
      <input
        placeholder="Search notes..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {/* TAG FILTER */}
      <input
        placeholder="Filter by tag..."
        value={filterTag}
        onChange={(e) => setFilterTag(e.target.value)}
      />

      <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>

        {/* SIDEBAR */}
        <div style={{ width: "30%" }}>
          <h2>Notes</h2>

          {notes
            .filter(n =>
              n.title.toLowerCase().includes(search.toLowerCase()) &&
              (filterTag === "" || n.tags.includes(filterTag))
            )
            .map((n) => (
              <div
                key={n.id}
                className="note-card"
                onClick={() => setSelectedNote(n)}
                style={{ cursor: "pointer" }}
              >
                <h4>{n.title}</h4>
              </div>
            ))}
        </div>

        {/* MAIN CONTENT */}
        <div style={{ width: "70%" }}>

          {/* SELECTED NOTE */}
          {selectedNote && (
            <div className="note-card">
              <h2>{selectedNote.title}</h2>
              <p>{selectedNote.content}</p>

              {/* 🔥 LINKED NOTES */}
              <p><b>Linked Notes:</b></p>
<ul>
  {graph?.edges
    ?.filter(e => e.source == selectedNote.id)
    .map((e, i) => {
      const target = notes.find(n => n.id == e.target);
      return (
        <li
          key={i}
          style={{ cursor: "pointer", color: "#007bff" }}
          onClick={() => setSelectedNote(target)}
        >
          {target?.title}
        </li>
      );
    })}
</ul>
            </div>
          )}

          {/* GRAPH */}
          <h2>Graph</h2>
          <div className="graph-box">
            <GraphView
              onNodeClick={(id) => {
                const found = notes.find(n => n.id == id);
                setSelectedNote(found);
              }}
            />
          </div>

        </div>

      </div>
    </div>
  );
}

export default App;