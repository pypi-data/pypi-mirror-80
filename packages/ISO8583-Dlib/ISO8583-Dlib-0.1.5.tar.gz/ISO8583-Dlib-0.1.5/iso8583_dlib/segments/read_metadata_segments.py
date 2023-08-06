"""Read metadata segments"""
import json
import pkg_resources


def read_json_to_dictionary(path):
    try:
        f = open(pkg_resources.resource_filename(__name__, path))
        data = json.load(f)
        f.close()
        return data
    except NameError:
        print("Error: ", NameError)
        return {}
