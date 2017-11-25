import json
import csv
from flask import Flask

from cors import crossdomain


app = Flask(__name__)


@app.route("/angular_velocity.csv", )
@crossdomain(origin='*')
def angular_velocity():
    with open('data/angular_velocity.csv', 'r') as csvfile:
        data = csvfile.read()
    return data


if __name__ == '__main__':
    app.run(port=8000)

