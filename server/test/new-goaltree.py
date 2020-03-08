from validate import validate

ignored = ["id", "created_at"]

template = {
    "name": "Elämänpuu",
}

validate("New goal tree", ignored, template)
