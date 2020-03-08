from validate import validate

ignored = ["id", "created_at", "nodes"]

template = {
    "name": "Elämänpuu",
}

validate("New goal tree nodes", ignored, template)
