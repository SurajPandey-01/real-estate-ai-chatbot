
from app.database.connection import SessionLocal
from app.database.models import PropertyListing
from app.scraper.wasalt_data import WASALT_LISTINGS


def seed_wasalt():
    db = SessionLocal()

    try:
        inserted = 0
        updated = 0

        for listing_data in WASALT_LISTINGS:
            existing = db.query(PropertyListing).filter_by(
                listing_id=listing_data["listing_id"]
            ).first()

            if existing:
                for key, value in listing_data.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                listing = PropertyListing(**listing_data)
                db.add(listing)
                inserted += 1

        db.commit()

        print("Wasalt database seeding completed!")
        print(f"New listings inserted: {inserted}")
        print(f"Existing listings updated: {updated}")

    except Exception as error:
        db.rollback()
        print("Error:", error)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_wasalt()
