from fastapi import FastAPI
from app.api.v1.endpoints import ocr, test, translate, ner, admin, auth,profile, feedback_api
#from mvp.backend.app.api.v1.endpoints import ad #, auth, ner, ocr

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#app.include_router(auth.router, prefix="/auth", tags=["auth"])
#app.include_router(ner.router, prefix="/ner", tags=["ner"])
#app.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
#app.include_router(translate.router, prefix="/translate", tags=["translate"])

# app/main.py

app.include_router(ocr.router, prefix="/api/v1/endpoints", tags=["ocr"])
app.include_router(translate.router, prefix="/api/v1/endpoints", tags=["translate"])
app.include_router(ner.router, prefix="/api/v1/endpoints", tags=["ner"])
app.include_router(test.router, prefix="/api/v1/endpoints", tags=["test"])
app.include_router(admin.router, prefix="/api/v1/endpoints", tags=["admin"])
app.include_router(auth.router, prefix="/api/v1/endpoints", tags=["auth"])
app.include_router(profile.router, prefix="/api/v1/endpoints", tags=["auth"])
app.include_router(feedback_api.router, prefix="/api/v1/endpoints", tags=["feedback_api"])
