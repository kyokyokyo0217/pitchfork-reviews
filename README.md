# pitchfork-reviews
a simple python script that scrapes pitchfork's album review page and notify new ones to your own slack channels.

# Installation
```pipenv sync```

# Usage
```pipenv run python3 main.py```

you have to create a ```.env``` file as this script needs [python-dotenv](https://pypi.org/project/python-dotenv/) to read environment variables such as slack urls.

you can refer to ```.env_ex``` in this repository.
