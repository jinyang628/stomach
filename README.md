## Getting Started

```
python3 -m venv venv

pip install -r requirements.txt

MAC: source venv/bin/activate
Windows: venv\Scripts\activate

uvicorn main:app --reload
```

## Before pushing 

```
pip freeze > requirements.txt
```