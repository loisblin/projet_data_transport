from backend.database import engine
from backend.models import Base
import logging
def delete_tables():
    
    Base.metadata.drop_all(bind=engine)
     

def create_tables():
    
    Base.metadata.create_all(bind=engine)
   
    

