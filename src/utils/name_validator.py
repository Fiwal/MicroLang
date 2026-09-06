from .constants import KEYWORDS

def is_valid_name(name):
    return False if isinstance(name, int) or name in KEYWORDS or not name.isidentifier() else True
