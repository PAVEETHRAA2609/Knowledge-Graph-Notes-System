from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


# =========================
# NOTE - TAGS (Many-to-Many)
# =========================
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)


# =========================
# NOTE - NOTE LINKS (GRAPH EDGES)
# =========================
note_links = Table(
    "links",
    Base.metadata,
    Column("source_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("target_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
)


# =========================
# NOTE MODEL
# =========================
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # -------------------------
    # TAG RELATIONSHIP
    # -------------------------
    tags = relationship(
        "Tag",
        secondary=note_tags,
        back_populates="notes"
    )

    # -------------------------
    # OUTGOING LINKS (A → B)
    # -------------------------
    linked_notes = relationship(
        "Note",
        secondary=note_links,
        primaryjoin=id == note_links.c.source_id,
        secondaryjoin=id == note_links.c.target_id,
        backref="incoming_links"
    )


# =========================
# TAG MODEL
# =========================
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    notes = relationship(
        "Note",
        secondary=note_tags,
        back_populates="tags"
    )