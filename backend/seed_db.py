
from app.database.connection import SessionLocal
from app.database.models import PropertyProject
from app.scraper.darglobal_data import DARGLOBAL_PROJECTS


def seed_database():
    db = SessionLocal()

    try:
        inserted = 0
        updated = 0

        for project_data in DARGLOBAL_PROJECTS:
            existing = db.query(PropertyProject).filter_by(
                source_url=project_data["source_url"]
            ).first()

            if existing:
                for key, value in project_data.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                project = PropertyProject(**project_data)
                db.add(project)
                inserted += 1

        db.commit()

        print("Database seeding completed!")
        print(f"New projects inserted: {inserted}")
        print(f"Existing projects updated: {updated}")

    except Exception as error:
        db.rollback()
        print("Error:", error)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
