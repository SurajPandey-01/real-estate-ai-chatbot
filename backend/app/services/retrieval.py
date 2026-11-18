
import re

from sqlalchemy.orm import Session
from app.database.models import PropertyProject, PropertyListing


STOP_WORDS = {
    "which", "what", "where", "when", "who", "how",
    "the", "and", "for", "are", "is", "in", "on",
    "of", "with", "available", "show", "find", "tell",
    "me", "about", "please", "can", "you", "there",
    "property", "properties", "project", "projects",
}

PROPERTY_TYPES = {
    "villa", "villas",
    "apartment", "apartments",
    "penthouse", "penthouses",
    "tower", "towers",
}


def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
    return [
        word for word in words
        if len(word) > 1 and word not in STOP_WORDS
    ]


def search_properties(db: Session, question: str):
    query_words = set(tokenize(question))

    if not query_words:
        return []

    lower_question = (question or "").lower()

    # Identify whether the user explicitly requested a data source
    requested_source = None

    if "wasalt" in lower_question:
        requested_source = "Wasalt"
    elif "darglobal" in lower_question or "dar global" in lower_question:
        requested_source = "DarGlobal"

    requested_types = {
        word.rstrip("s")
        for word in query_words
        if word in PROPERTY_TYPES
    }

    projects = db.query(PropertyProject).all()
    listings = db.query(PropertyListing).all()

    results = []

    # Search DarGlobal projects unless Wasalt was explicitly requested
    if requested_source != "Wasalt":
        for project in projects:
            searchable_text = " ".join([
                project.project_name or "",
                project.location or "",
                project.property_type or "",
                project.completion_status or "",
                project.description or "",
                " ".join(project.amenities or []),
            ])

            property_words = set(tokenize(searchable_text))

            project_types = {
                word.rstrip("s")
                for word in tokenize(project.property_type)
            }

            if requested_types and not requested_types.intersection(project_types):
                continue

            matched_words = query_words.intersection(property_words)

            if not matched_words:
                continue

            score = len(matched_words) / len(query_words)

            if score < 0.25:
                continue

            results.append({
                "source": project.source,
                "name": project.project_name,
                "location": project.location,
                "property_type": project.property_type,
                "bedrooms": project.bedrooms,
                "area": project.area_min,
                "area_max": project.area_max,
                "area_unit": project.area_unit,
                "price": None,
                "currency": None,
                "status": project.completion_status,
                "amenities": project.amenities,
                "url": project.source_url,
                "_score": score,
            })

    # Search Wasalt listings unless DarGlobal was explicitly requested
    if requested_source != "DarGlobal":
        for listing in listings:
            searchable_text = " ".join([
                listing.title or "",
                listing.city or "",
                listing.district or "",
                listing.address or "",
                listing.property_type or "",
                listing.purpose or "",
            ])

            property_words = set(tokenize(searchable_text))

            listing_types = {
                word.rstrip("s")
                for word in tokenize(listing.property_type)
            }

            if requested_types and not requested_types.intersection(listing_types):
                continue

            matched_words = query_words.intersection(property_words)

            if not matched_words:
                continue

            score = len(matched_words) / len(query_words)

            if score < 0.25:
                continue

            results.append({
                "source": listing.source,
                "name": listing.title,
                "location": f"{listing.district or ''}, {listing.city or ''}",
                "property_type": listing.property_type,
                "bedrooms": listing.bedrooms,
                "area": listing.area,
                "area_max": listing.area,
                "area_unit": listing.area_unit,
                "price": listing.price,
                "currency": listing.currency,
                "status": listing.listing_status,
                "amenities": [],
                "url": listing.source_url,
                "_score": score,
            })

    # Sort by relevance
    results.sort(
        key=lambda item: item["_score"],
        reverse=True
    )

    # Remove internal scoring information
    for item in results:
        item.pop("_score", None)

    return results[:5]
