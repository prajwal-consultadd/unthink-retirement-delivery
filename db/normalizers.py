import math

def clean_null(v):
    """
    Converts:
    - 'null' (string) -> None
    - NaN -> None
    - empty string -> None
    """
    if v is None:
        return None

    if isinstance(v, float) and math.isnan(v):
        return None

    if isinstance(v, str):
        s = v.strip().lower()
        if s in {"", "null", "#error!"}:
            return None

    return v


def clean_int(v):
    """
    Converts:
    - '348,660' -> 348660
    - '123' -> 123
    - invalid -> None
    """
    v = clean_null(v)
    if v is None:
        return None

    if isinstance(v, int):
        return v

    if isinstance(v, str):
        v = v.replace(",", "").strip()
        if v.isdigit():
            return int(v)

    return None


def clean_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.lower() == "true"
    return False


def clean_json(v):
    """
    JSONB must receive:
    - dict
    - list
    - None
    """
    v = clean_null(v)
    if v is None:
        return None

    if isinstance(v, (dict, list)):
        return v

    return None
