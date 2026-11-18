
from app.database.connection import Base, engine
from app.database.models import PropertyProject, PropertyListing


def init_db():
    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully!")
    print("Tables created:", list(Base.metadata.tables.keys()))


if __name__ == "__main__":
    init_db()
