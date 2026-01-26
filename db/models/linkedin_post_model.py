from sqlalchemy import (
    Column, Text, Integer, Boolean, BigInteger, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class LinkedInPost(Base):
    __tablename__ = "linkedin_posts"

    urn = Column(Text, primary_key=True)

    text = Column(Text)
    url = Column(Text)

    posted_at_timestamp = Column(BigInteger)
    posted_at_iso = Column(TIMESTAMP)

    time_since_posted = Column(Text)
    is_repost = Column(Boolean)

    author_type = Column(Text)
    author_profile_url = Column(Text)
    author_profile_id = Column(Text)
    author_headline = Column(Text)
    author_name = Column(Text)

    type = Column(Text)
    share_urn = Column(Text)

    attributes = Column(JSONB)
    comments = Column(JSONB)
    reactions = Column(JSONB)

    num_shares = Column(Integer)
    num_likes = Column(Integer)
    num_comments = Column(Integer)

    can_react = Column(Boolean)
    can_post_comments = Column(Boolean)
    can_share = Column(Boolean)
    commenting_disabled = Column(Boolean)

    allowed_commenters_scope = Column(Text)
    root_share = Column(Boolean)
    share_audience = Column(Text)

    author = Column(JSONB)
    author_profile_picture = Column(Text)
    author_urn = Column(Text)

    document = Column(JSONB)
    is_activity = Column(Boolean)
    input_url = Column(Text)
    linkedin_video = Column(JSONB)
    author_followers_count = Column(Integer)
    poll = Column(JSONB)
    article = Column(JSONB)
    reshared_post = Column(JSONB)
    activity_description = Column(Text)
    images = Column(JSONB)
    image = Column(JSONB)

    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
