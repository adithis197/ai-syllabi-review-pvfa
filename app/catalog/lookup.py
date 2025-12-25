import json

with open("app/catalog/catalog.json") as f:
    CATALOG = json.load(f)

def get_catalog_entry(course_code: str):
    return CATALOG.get(course_code)
