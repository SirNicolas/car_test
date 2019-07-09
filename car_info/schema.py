BASE_PROPERTIES = {
    "owner_name": {"type": "string"},
    "model_year": {"type": "integer"},
    "code": {"type": "string"},
    "vehicle_code": {"type": "string"},
    "engine": {
        "type": "object",
        "properties": {
            "capacity": {"type": "integer", "minimum": 1},
            "num_cylinders": {"type": "integer", "minimum": 1},
            "max_rpm": {"type": "integer", "minimum": 1},
            "manufacturer_code": {"type": "string"},
        },
        "additionalProperties": False,
    },
    "fuel_figures": {
        "type": "object",
        "properties": {
            "speed": {"type": "integer", "minimum": 1},
            "mpg": {"type": "number", "minimum": 1},
            "usage_description": {"type": "string"},
        },
        "additionalProperties": False,
    },
    "performance_figures": {
        "type": "object",
        "properties": {
            "octane_rating": {"type": "integer"},
            "acceleration": {
                "type": "object",
                "properties": {
                    "mph": {"type": "integer", "minimum": 1},
                    "seconds": {"type": "number", "minimum": 1},
                }
            },
        },
        "additionalProperties": False,
    },
    "manufacturer": {"type": "string"},
    "model": {"type": "string"},
    "activation_code": {"type": "string"},
}

CAR_PATCH_SCHEMA = {
    "type": "object",
    "properties": BASE_PROPERTIES,
    "additionalProperties": False,
}

CAR_POST_SCHEMA = {
    "type": "object",
    "properties": {
        **BASE_PROPERTIES, "serial_number": {"type": "integer", "minimum": 1}
    },
    "required": ["owner_name", "serial_number"],
    "additionalProperties": False,
}
