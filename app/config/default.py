import os
from neomodel import config

config.DATABASE_URL = os.getenv('NEO4j_DATABASE_URL','bolt://neo4j:password@neo4j:7687')
