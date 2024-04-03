## Getting Started!

### Setup db

### Create a virtual environment if you have yet to.

```
python3 -m venv venv
```

### Activate virtual environment

#### MAC users

```
source venv/bin/activate
```

#### Windows users

```
venv\Scripts\activate
```

### Install the latest dependencies used by others

```
pip install -r requirements.txt
```

### Start the server

```
uvicorn app.main:app --reload --port 8080
```

### Install turso CLI

https://docs.turso.tech/quickstart

### Login to turso
```
turso auth logout
turso auth login (make sure u are on the right browser with the right account)
turso org switch ****YOUR USERNAME****
turso db list (u should see the correct db)
```

## Before pushing

### Update requirements.txt with the latest dependencies you installed

```
pip freeze > requirements.txt
```

### Add test cases

Make sure that there is a `__init__.py` file at every level of the test cases

Run the following command at the root of the repository
`pytest`

### Check style

Run the following command at the root of the repository
`black .`
