import re
import string


def roles_in(user_roles, roles) -> bool:
    if roles in [y.id for y in user_roles]:
        return True
    return False


def check_filter_words(filter_words, message) -> bool:
    separators = string.punctuation + string.digits + string.whitespace
    excluded = string.ascii_letters

    if type(filter_words) is "list":
        word = filter_words
    elif type(filter_words) is "srt":
        word = [filter_words]
    else:
        raise "Filter words not valid"

    formatted_word = f"[{separators}]*".join(list(word))
    regex_true = re.compile(fr"{formatted_word}", re.IGNORECASE)
    regex_false = re.compile(
        fr"([{excluded}]+{word})|({word}[{excluded}]+)", re.IGNORECASE
    )

    profane = False

    result_a = regex_true.search(message)
    result_b = regex_false.search(message)

    print(f"Result A {result_a}")
    print(f"Result B {result_b}")

    if result_a is not None and result_b is None:
        profane = True

    return profane
