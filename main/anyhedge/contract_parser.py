from subprocess import run, PIPE
import sys
import json


def detect_and_parse(raw_tx_hex):
    p = run(
        ['node', '/app/main/anyhedge/contract_parser.js'],
        input=raw_tx_hex,
        capture_output=True,
        text=True
    )
    result = {}
    if p.stdout:
       result = json.loads(p.stdout.decode('utf8'))
    return result
