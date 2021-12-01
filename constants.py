def expansions():
    return {
        '2a03',
        'fds',
        'mmc5',
        'vrc6',
        'vrc7',
        'n163'
    }

def globalExpansions():
    return [
        '2a03'
    ]

def columns(expansion=''):
    mapping = {
        '2a03': (5, ['pulse1', 'pulse2', 'triangle', 'noise', 'dpcm'])
    }

    try:
        mapping_data = mapping[expansion]

        return mapping_data
    except IndexError as ex:
        return []
    except Exception as ex:
        return []
