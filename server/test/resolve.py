from validate import validate

ignored = ["id", "created_at", "resolved_at"]

template = {
    "message": "valmis",
    "resolved": True
}

validate("Resolve note", ignored, template)
