#!/usr/bin/env python
from sqlalchemy import create_engine

# pool_pre_ping
engine = create_engine('sqlite:///server_environment.db', echo=True, pool_pre_ping=True)

