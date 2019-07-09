import json
import os

f = open(os.path.join(os.getenv('HOME'), 'settings.json'), 'r')
config = json.load(f)
