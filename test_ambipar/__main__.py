from fastapi import FastAPI, Depends
from dotenv import load_dotenv
import routes

load_dotenv()
app = FastAPI()

app.mount("/",routes)
