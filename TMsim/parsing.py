def parse_string(s, par='{}', sep=',', ret=set):
    s = s.strip(par[0]).strip(par[1])
    parts = [item.strip() for item in s.split(sep)]
    return ret(parts)


def parse_text(lines):
    lines = [l.strip('\n').replace(' ', '') for l in lines if l != '\n']
    for line in lines:
        if line.startswith('NUM_TAPES='):
            num_tapes = int(line.strip('NUM_TAPES='))
        elif line.startswith('ALPHABET='):
            alphabet = parse_string(line.strip('ALPHABET='))
        elif line.startswith('STATES='):
            states = parse_string(line.strip('STATES='))
        elif line.startswith('TRANSITION_FUNC='):
            transitions = lines[lines.index(line)+1:]
            break
    return num_tapes, alphabet, states, transitions



def get_delta_dict(transitions, alphabet):
    transitions_list = [
        t.replace('*', s)
        for s in alphabet
        for t in transitions if '*' in t
    ]

    transitions_list.extend([
        t for t in transitions if '*' not in t
    ])

    delta_dict = {}

    for string in transitions_list:
        left, right = string.split('-->', 1)

        key = tuple(
            item.strip()
            for item in left.strip().strip('()').split(',')
        )

        value = tuple(
            item.strip()
            for item in right.strip().strip('()').split(',')
        )

        delta_dict[key] = value

    return delta_dict

