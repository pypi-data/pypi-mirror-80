def get_detail_level(detail_level: str) -> int:
    return {
        "low": 7,
        "medium": 4,
        "high": 2,
        "ultra": 1,
    }.get(detail_level, 4)
