"""
Create base repository
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
    CREATE TYPE e_location_type AS ENUM (
        'TOP_STORY', 'MAIN_HEADLINE', 'COLUMN'
    );"""),
]
