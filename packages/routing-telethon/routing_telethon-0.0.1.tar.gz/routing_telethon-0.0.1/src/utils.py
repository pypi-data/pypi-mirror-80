from telethon import Button
import json


def wrap_keyboard(texts):
    return __iterate_over_lists(texts, lambda t: Button.text(t, resize=True))


def wrap_inline(buttons):
    return __iterate_over_lists(buttons, __wrap_to_inline_button)


def __wrap_to_inline_button(button):
    payload = {
        'command': button[1],
        'arguments': button[2:] if len(button) > 2 else []
    }
    data = json.dumps(payload)
    return Button.inline(button[0], data=data)


def __iterate_over_lists(iter_list, callback):
    ret = []
    for row in iter_list:
        if type(row) == list:
            ret.append(
                [callback(text) for text in row]
            )
        else:
            ret.append(callback(row))
    return ret
