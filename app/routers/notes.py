from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
import re

from app.database.database import get_db
from app.models import models
from app.schemas.note_schema import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["Notes"])


# =========================
# CREATE NOTE + AUTO LINK
# =========================
@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):

    # ❌ prevent duplicate title
    existing = db.query(models.Note).filter(models.Note.title == note.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Note with this title already exists")

    # ✅ create note
    new_note = models.Note(
        title=note.title,
        content=note.content
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    # =========================
    # TAG HANDLING
    # =========================
    tag_objects = []
    for tag_name in note.tags:
        tag_name = tag_name.lower().strip()

        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)

        tag_objects.append(tag)

    new_note.tags = tag_objects
    db.commit()

    # =========================
    # 🔥 AUTO LINK PARSING [[...]]
    # =========================
    pattern = r"\[\[(.*?)\]\]"
    matches = re.findall(pattern, note.content or "")

    for title in matches:
        title = title.strip()

        target = db.query(models.Note).filter(models.Note.title == title).first()

        if target and target.id != new_note.id:
            if target not in new_note.linked_notes:
                new_note.linked_notes.append(target)

    db.commit()
    db.refresh(new_note)

    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content,
        "tags": [t.name for t in new_note.tags]
    }


# =========================
# MANUAL LINK API
# =========================
@router.patch("/{note_id}/link")
def link_notes(note_id: int, target_id: int, db: Session = Depends(get_db)):

    if note_id == target_id:
        raise HTTPException(status_code=400, detail="Cannot link note to itself")

    source = db.query(models.Note).filter(models.Note.id == note_id).first()
    target = db.query(models.Note).filter(models.Note.id == target_id).first()

    if not source or not target:
        raise HTTPException(status_code=404, detail="Note not found")

    if target in source.linked_notes:
        raise HTTPException(status_code=400, detail="Link already exists")

    source.linked_notes.append(target)
    db.commit()

    return {"message": "Link created successfully"}


# =========================
# GET NOTES
# =========================
@router.get("/", response_model=list[NoteResponse])
def get_notes(tag: str = None, search: str = None, db: Session = Depends(get_db)):

    query = db.query(models.Note)

    if search:
        query = query.filter(
            or_(
                models.Note.title.contains(search),
                models.Note.content.contains(search)
            )
        )

    notes = query.all()

    if tag:
        tag = tag.lower().strip()
        notes = [
            note for note in notes
            if any(t.name == tag for t in note.tags)
        ]

    return [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": [t.name for t in note.tags]
        }
        for note in notes
    ]


# =========================
# GET SINGLE NOTE
# =========================
@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": [t.name for t in note.tags]
    }


# =========================
# GRAPH API
# =========================
@router.get("/graph/")
def get_graph(db: Session = Depends(get_db)):

    notes = db.query(models.Note).all()

    nodes = []
    edges = []

    for note in notes:
        nodes.append({
            "id": note.id,
            "title": note.title
        })

        for linked in note.linked_notes:
            edges.append({
                "source": note.id,
                "target": linked.id
            })

    adjacency = {
        note.id: [n.id for n in note.linked_notes]
        for note in notes
    }

    return {
        "nodes": nodes,
        "edges": edges,
        "adjacency_list": adjacency
    }