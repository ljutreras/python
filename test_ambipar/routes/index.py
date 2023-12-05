from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from controller.ambipar.controller_get import get
from classes import algo
load_dotenv()
app = FastAPI()

app.mount("/classes", algo)
app.mount("/ambipar",get)
#app.mount("/ambipar",post)