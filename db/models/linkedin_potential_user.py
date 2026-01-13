from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from db.postgres import Base
from sqlalchemy.dialects.postgresql import JSONB

class LinkedInPotentialUser(Base):
    __tablename__ = "linkedin_potential_users"

    post_id = Column(String, index=True)
    post_url = Column(Text)
    post_context = Column(String)

    comment_url = Column(Text)
    comment_text = Column(Text)

    author = Column(JSONB, nullable=True)

    intent = Column(String)
    confidence = Column(Float)
    score = Column(Integer)

    public_id = Column(String, unique=True, index=True, nullable=False, primary_key= True)

    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    soft_delete= Column(Boolean, default= False, nullable=False)
