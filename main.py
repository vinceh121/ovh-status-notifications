import tomllib
import ovh
import apprise
import json
import time

previousStates = {}
config = None

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

apprise = apprise.Apprise()

for url in config["notif"]["urls"]:
    apprise.add(url)

client = ovh.Client(
#    endpoint='ovh-eu',
#    application_key='<application key>',
#    application_secret='<application secret>',
#    consumer_key='<consumer key>',
     **config["auth"]
)

while True:
    for vps in config["vps"]["names"]:
        data = client.get("/vps/" + vps);
        state = data["state"]

        if vps not in previousStates or state != previousStates[vps]:
            previousStates[vps] = state
            apprise.notify(body="VPS now " + state)

    time.sleep(config["general"]["interval"])

