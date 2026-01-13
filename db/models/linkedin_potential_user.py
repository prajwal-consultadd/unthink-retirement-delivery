from sqlalchemy import Column, Integer, String, Float, Text
from db.postgres import Base
from sqlalchemy.dialects.postgresql import JSONB

class LinkedInPotentialUser(Base):
    __tablename__ = "linkedin_potential_users"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(String, index=True)
    post_url = Column(Text)
    post_context = Column(String)

    comment_url = Column(Text)
    comment_text = Column(Text)

    author = Column(JSONB, nullable=True)

    intent = Column(String)
    confidence = Column(Float)
    score = Column(Integer)

    public_id = Column(String, unique=True, index=True, nullable=False)

    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
