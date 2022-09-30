#!/usr/bin/env python
from time import sleep
from subprocess import run

while True:
    sleep(4)
    print("starting Sardana")
    run(["/opt/conda/bin/Sardana", "area51"])
