from fastapi import FastAPI, HTTPException

from secure_database import get_user_by_username, init_db

init_db()

app = FastAPI(title="Samplepython5 Secure")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users/{username}")
def get_user(username: str):
    user = get_user_by_username(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/")
def read_root():
    return {"message": "SQL Injection을 방어한 secure 버전입니다."}
