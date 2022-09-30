## VENDING API

### Intro
This is an example vending machine api __(coding challenge, not a real vending machine!)__

### Credits to
Github user [Karek](https://github.com/karec) for his [Flask API cookiecutter](https://github.com/karec/cookiecutter-flask-restful/blob/master/README.md)

### Install project requirements

Install pip requirements:
```bash
cd vending_api
pip install -r requirements.txt
pip install -e .
```


Initiate the app:
```bash
flask db init
flask db migrate
flask db upgrade
flask init  # creates buyer, seller users and some products
```

Run the app:

```bash
flask run
```

More options:
```bash
flask --help
```

### Test the project

* You can test it with swagger-ui. First make sure that you are running the app
`flask run`. After that go to [http://127.0.0.1:5000/swagger-ui](http://127.0.0.1:5000/swagger-ui)

* Run `pytest` tests with:

```bash
tox -e test
```

* Lint python code:

```bash
tox -e lint
```

* Fix those linting issues that can be solved automatically:

```bash
tox -e fix-lint
```

### Exercise Brief
[Exercise Brief](EXERSICE.MD)