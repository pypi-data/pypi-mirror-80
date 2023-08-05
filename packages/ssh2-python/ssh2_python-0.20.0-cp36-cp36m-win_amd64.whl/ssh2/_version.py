
import json

version_json = '''
{"date": "2020-09-22T18:40:30.207511", "dirty": false, "error": null, "full-revisionid": "1e57d7e2564e0205f0069a1b3d02009b2fbc84b0", "version": "0.20.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

