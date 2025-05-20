from app.db.session import engine, Base
from app.models import alarma   

Base.metadata.create_all(bind=engine)