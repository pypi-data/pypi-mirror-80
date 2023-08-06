import os

MAX_CONFIRMATIONS = 6

with open(
    os.path.join(os.path.dirname(__file__), "g1_license.html"), "r", encoding="utf-8"
) as stream:
    G1_LICENSE = stream.read()
