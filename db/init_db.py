from db.postgres import engine, Base

def init_db():
    # Import models so SQLAlchemy registers them
    from db.models.linkedin_post_model import LinkedInPost
    from db.models.linkedin_potential_user import LinkedInPotentialUser

    Base.metadata.create_all(bind=engine)
