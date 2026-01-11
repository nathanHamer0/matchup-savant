def snake_to_standard_name(name: str) -> str:
    """Receives a player's name in snake-case as an argument and returns it in standard-name-case.

    Args:
        name (str): Player name in snake-case.

    Returns:
        str: Player name in standard-name-case.
    """
    names = name.split("_")
    return f'{names[0].capitalize()} {names[1].capitalize()}'

def inverted_name_to_standard_name(name: str) -> str:
    """Receives a player's name in inverted-name-case as an argument and returns it in standard-name-case.

    Args:
        name (str): Player name in inverted-name-case.

    Returns:
        str: Player name in standard-name-case.
    """
    names = name.split(", ")
    return f'{names[1].capitalize()} {names[0].capitalize()}'

def snake_to_inverted_name(name: str) -> str:
    """Receives a player's name in snake-case as an argument and returns it in inverted-name-case.

    Args:
        name (str): Player name in snake-case.

    Returns:
        str: Player name in inverted-name-case.
    """
    names = name.split("_")
    return f'{names[1].capitalize()}, {names[0].capitalize()}'

def inverted_name_to_snake(name: str) -> str:
    """Receives a player's name in inverted-name-case as an argument and returns it in snake-case.

    Args:
        name (str): Player name in inverted-name-case.

    Returns:
        str: Player name in snake-case.
    """
    names = name.split(", ")
    return f'{names[1].lower()}_{names[0].lower()}'