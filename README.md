## Getting Started!

### Create a virtual environment if you have yet to
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
uvicorn main:app --reload
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
