from sqlalchemy import create_engine

engine = create_engine('sqlite:///DB_file.db', echo=True)