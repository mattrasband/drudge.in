"""
Create snapshot, article, and image tables
"""

from yoyo import step

__depends__ = {'20160524_01_OYDN4-create-base-repository'}

steps = [
    step("""CREATE TABLE articles (
        id BIGSERIAL PRIMARY KEY,
        title VARCHAR(1024) NOT NULL,
        href VARCHAR(2083) NOT NULL UNIQUE,
        image_url VARCHAR(2083) NOT NULL DEFAULT '',
        location e_location_type NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
    );"""),
]
