def expansions() -> dict:
    """
    Sound sources that can be used
    within FamiTracker itself to
    compose music with.

    Returns:
        dict: Available expansion chips
    """
    return {
        '2a03',
        'fds',
        'mmc5',
        'vrc6',
        'vrc7',
        'n163'
    }

def globalExpansions() -> list:
    """
    A list of valid expansion chips
    that can be parsed by the 
    ft2vis program.

    Returns:
        list: Expansion chips that will successfully provide valid exports.
    """
    return [
        '2a03'
    ]

def columns(expansion='') -> tuple:
    """
    Column information for the parser to
    use when deciding how to split and
    structure the incoming data.

    Returns:
        tuple: Number of channels + column name pairs, otherwise ()
    """
    mapping = {
        '2a03': (5, ['pulse1', 'pulse2', 'triangle', 'noise', 'dpcm'])
    }

    try:
        mapping_data = mapping[expansion]

        return mapping_data
    except IndexError as ex:
        return ()
    except Exception as ex:
        return ()
