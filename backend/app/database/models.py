
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.sql import func

from app.database.connection import Base


class PropertyProject(Base):
    __tablename__ = "property_projects"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(100), nullable=False)
    project_name = Column(String(255), nullable=False, index=True)

    location = Column(String(500))
    property_type = Column(String(150))

    bedrooms = Column(JSON, nullable=True)
    area_min = Column(Float, nullable=True)
    area_max = Column(Float, nullable=True)
    area_unit = Column(String(30), nullable=True)

    completion_status = Column(String(150))
    expected_completion = Column(String(100))

    amenities = Column(JSON, nullable=True)
    description = Column(Text, nullable=True)

    source_url = Column(String(1000), nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class PropertyListing(Base):
    __tablename__ = "property_listings"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(100), nullable=False)
    listing_id = Column(String(100), unique=True, index=True)

    title = Column(String(500))
    property_type = Column(String(150))
    purpose = Column(String(50))

    price = Column(Float, nullable=True)
    currency = Column(String(20))

    city = Column(String(150))
    district = Column(String(150))
    address = Column(String(500))

    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)

    area = Column(Float, nullable=True)
    area_unit = Column(String(30))

    property_age = Column(String(100))
    construction_year = Column(Integer, nullable=True)
    facing = Column(String(200))

    listing_status = Column(String(100))

    description = Column(Text, nullable=True)
    source_url = Column(String(1000), nullable=False, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
