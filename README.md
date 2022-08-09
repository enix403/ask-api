# "ASK" API

Django API for ASK app.

# Running

Start by cloning this repository.

Now once ready, it is recommended to create and activate a [virtual environment](https://docs.python.org/3/library/venv.html).

Install the dependencies
```sh
pip install -r requirements.txt
````
Copy the `sample.env` file as `.env` (in the same location, i.e project root) and fill the required variables in it.

Then perform the migrations:

```sh
python manage.py makemigrations
python manage.py migrate
```

Run the application:
```sh
python manage.py runserver 3000
```

The API will be available on [http://localhost:3000/api/v1/](http://localhost:3000/api/v1/)