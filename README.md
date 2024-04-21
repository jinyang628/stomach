## Getting Started!

## Set up .env
Make a copy of the `.env.example` file and name it as `.env` in the same directory. Remember to fill in the necessary fields

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
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Install turso CLI

https://docs.turso.tech/quickstart

### For windows users
You will need windows wsl to run the turso CLI. You can follow the instructions here: https://docs.microsoft.com/en-us/windows/wsl/install
Perform the turso installation in the wsl terminal.

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
