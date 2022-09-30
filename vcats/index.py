#!/usr/bin/env python
from typing import Set
from json import dumps
from subprocess import Popen, PIPE
from flask import Flask, request

# number of basket positions to emulate
NUM_BASKETS = 29

PAGE_TEMPLATE = """
<html>
<body>
<form method='post'>
  {form_body}
  <input type='submit' name='submit' value='submit'/>
</form>
</body>
</html>
"""
app = Flask(__name__)

CassettesPresent: Set[int] = set()
CatsProcess = None


def _basket_positions():
    for n in range(1, NUM_BASKETS + 1):
        yield n


def _push_cassettes_present():
    global CassettesPresent
    global CatsProcess

    json_str = dumps(list(CassettesPresent))
    CatsProcess.stdin.write(f"{json_str}\n".encode())
    CatsProcess.stdin.flush()


@app.route("/", methods=["GET"])
def index_get():
    form_body = ""
    for pos in _basket_positions():
        basket = f"basket{pos}"

        checked = "checked" if pos in CassettesPresent else ""

        form_body += (
            f"<div><input type='checkbox' id={basket} name='{basket}' {checked}/>"
            f"<label for='{basket}'>Basket position {pos}<label></div>"
        )

    return PAGE_TEMPLATE.format(form_body=form_body)


@app.route("/", methods=["POST"])
def index_post():
    new_cassettes_present = set()
    form = request.form

    for pos in _basket_positions():
        basket = f"basket{pos}"
        if basket in form:
            new_cassettes_present.add(pos)

    global CassettesPresent
    CassettesPresent = new_cassettes_present

    _push_cassettes_present()

    return index_get()


if __name__ == "__main__":
    CatsProcess = Popen(["./cats.py", "1", "b311a-e/ctl/cats-01"], stdin=PIPE)
    app.run(
        host="0.0.0.0",
        # run in single thread, as we relay on global CassettesPresent variable
        threaded=False,
    )
