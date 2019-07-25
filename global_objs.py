last_send_time = {

}

codes = {

}

last_paint_time = {

}

VARS = {

}


def make_response(ok, result):
    from json import JSONEncoder
    return JSONEncoder().encode({"ok": ok, "result": result})


try:
    import config
except Exception as ex:
    import config_default as config
