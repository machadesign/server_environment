#!/usr/bin/env python
from sqlalchemy import create_engine

# pool_pre_ping
# /Users/matthewchadwell/server_environment/project_files/db_engine.py
engine = create_engine('sqlite:///server_environment.db', echo=True, pool_pre_ping=True)

