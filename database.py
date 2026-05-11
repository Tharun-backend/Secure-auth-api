from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:Nuttertools%40123@localhost/auth_db"

engine = create_engine(DATABASE_URL)