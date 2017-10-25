#!/usr/bin/env python3

import datetime
import os
import requests
import dateutil.parser as dateparser

import singer
from singer import utils

LOGGER = singer.get_logger()
SESSION = requests.Session()
REQUIRED_CONFIG_KEYS = [
    "apikey",
    "store",
    "start_date",
]

CONFIG = {}
STATE = {}
BASE_URL = "https://api.reviews.co.uk/export/{}?store={}&apikey={}&min_rating=1&max_rating=5&include_additional_ratings=1&min_date={}"

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def load_schema(entity):
    return utils.load_json(get_abs_path("schemas/{}.json".format(entity)))

def get_start(key):
    if key not in STATE:
        STATE[key] = CONFIG['start_date']

    return dateparser.parse(STATE[key])

def get_url(endpoint, start):
    return BASE_URL.format(endpoint, CONFIG['store'], CONFIG['apikey'], start)

def sync_type(type, endpoint, replicationKey):
    schema = load_schema(type)
    singer.write_schema(type, schema, [replicationKey])

    url = get_url(endpoint, get_start(type).strftime("%Y-%m-%d"))

    req = requests.Request("GET", url=url).prepare()
    resp = SESSION.send(req)
    resp.raise_for_status()

    finalRow = None
    for row in resp.json():
        finalRow = row
        if row.get("date"):
            row["date"] = dateparser.parse(row["date"]).isoformat() + "Z";
        if row.get("rating"):
            row["rating"] = int(row["rating"])
        singer.write_record(type, row)

    if finalRow != None:
        utils.update_state(STATE, type, finalRow['date'])

def do_sync():
    LOGGER.info("Starting sync")

    sync_type("merchant_reviews", "merchant.json", "date")
    # TODO: the schema for theis needs determining:
    #sync_type("product_reviews", "product.json", "date", ["date"])

    singer.write_state(STATE)
    LOGGER.info("Sync complete")

def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    CONFIG.update(args.config)
    STATE.update(args.state)
    do_sync()


if __name__ == "__main__":
    main()
