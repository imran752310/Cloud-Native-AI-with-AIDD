from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Root endpoint return Hello World"""
    return {"message": "Hellow i am FastAPi"}

@app.get("/health")
def health_check():
    """Health Check endpoint"""
    return {"Status": " ok and good"}