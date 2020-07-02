import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "bJuLjr[e>b{&725NWK%?Ey^8#gWcEk"
    MONGODB_SETTINGS = {'db': 'HMS'}