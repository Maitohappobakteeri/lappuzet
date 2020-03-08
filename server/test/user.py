from validate import validate

ignored = ["id"]

template = {
    "username": "jenna"
}

validate("Current user", ignored, template)
