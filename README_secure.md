# Secure Sample (추가 소스)

이 프로젝트에는 의도적으로 취약한 데모(`main.py`, `database.py`)가 이미 포함되어 있습니다.

추가로, SQL Injection을 방어한 안전 버전 소스를 아래 파일로 제공합니다:

- `secure_main.py`: FastAPI 앱
- `secure_database.py`: 파라미터 바인딩을 사용하는 안전한 SQLite 쿼리

## 실행

```powershell
py -3.11 -m pip install -r requirements.txt
py -3.11 -m uvicorn secure_main:app --port 8000
```

## 테스트

외부 테스트 의존성 없이 `unittest`로 실행합니다.

```powershell
py -3.11 -m unittest -v
```
