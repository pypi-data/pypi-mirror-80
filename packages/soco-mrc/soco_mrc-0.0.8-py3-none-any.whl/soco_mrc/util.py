from typing import Any, Callable, Dict, Generator, Sequence


def chunks(l: Sequence, n: int = 5) -> Generator[Sequence, None, None]:
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_ans_span(res):
    if not res:
        return ""

    for i, t in enumerate(res):
        if t.startswith("##"):
            res[i - 1] += t[2:]
            res[i] = ""

    value = " ".join([x for x in res if x != ""])
    return value

def is_whitespace(c):
    if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
        return True
    return False

def token2char(orig_str, tokens):
    norm_tokens = [t.replace('##', '') for t in tokens]

    token_id = 0
    token_char_id = 0
    token2char_map = {}  # token_id -> [start, end]

    token2char_map[token_id] = [0, None]
    for c_id, c in enumerate(orig_str):
        if is_whitespace(c):
            token2char_map[token_id][1] = c_id
            token_id += 1
            token_char_id = 0
            token2char_map[token_id] = [c_id+1, None]
            continue

        if token_char_id < len(norm_tokens[token_id]) and c == norm_tokens[token_id][token_char_id]:
            token_char_id += 1
        else:
            token2char_map[token_id][1] = c_id
            token_id += 1
            token_char_id = 0
            token2char_map[token_id] = [c_id, None]

            if c == norm_tokens[token_id][token_char_id]:
                token_char_id += 1

    token2char_map[token_id][1] = c_id+1
    # print(token2char_map)
    return token2char_map

