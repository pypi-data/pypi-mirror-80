# -*- coding: utf-8 -*-
'''bot_logging.py'''


def introduce_myself(me):
    print(
        f'''Running as {'bot' if me.bot else 'user'};'''
        f'''name: {me.first_name}{' '+me.last_name if me.last_name else ''}'''
        f'''{'; username: @'+me.username if me.username else ''}'''
    )
