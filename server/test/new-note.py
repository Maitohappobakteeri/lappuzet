from validate import validate

ignored = ["id", "created_at", "resolved_at"]

template = {
    "message": "Moikka! Tämä on testi. . . :>",
    "resolved": False
}

validate("New note", ignored, template)
