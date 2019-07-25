from main import app, socket
from flask import session, request
from global_objs import codes, last_send_time, make_response, config
import time
import random
import urllib
import urllib.request
import urllib.parse


@app.context_processor
def consts():
    return {
        "DEBUG": config.DEBUG
    }


@app.route("/api/send_code", methods=["POST"])
def paintboard_send_code():
    if session.get("qq_id"):
        return make_response(False, {"message": "你已经登录！"})
    qqid = request.form.get("qq_id")
    if not qqid:
        return make_response(False, {"message": "请输入QQ号"})
    qqid = str(qqid)
    if str(qqid) in last_send_time and time.time()-last_send_time[str(qqid)] < config.MIN_SENDCODE_INTERVAL:
        return make_response(False, {"message": "间隔过短"})
    last_send_time[qqid] = time.time()
    codes[qqid] = "".join((str(random.randint(0, 9)) for i in range(6)))
    with urllib.request.urlopen(config.SEND_CODE_URL, data=urllib.parse.urlencode({
        "token": config.SEND_CODE_TOKEN,
        "target": qqid,
        "content": "您的验证码为 {} ，请在 {}s 内使用。".format(codes[qqid], config.CODE_TIMEOUT)
    }).encode("utf-8")) as urlf:
        import json
        ret = json.JSONDecoder().decode(urlf.read().decode())
        if not ret["ok"]:
            return make_response(False, {"message": "发送验证码失败! {}".format(ret)})
    return make_response(True, {"message": "您的验证码已经通过群Bot私聊发送给您，如果没有收到请尝试添加群Bot为好友后再次发送。"})


@app.route("/api/login", methods=["POST"])
def paintboard_login():
    if session.get("qq_id"):
        return make_response(False, {"message": "你已经登录！"})
    qqid = request.form.get("qq_id", None)
    code = request.form.get("code", None)
    if not qqid or not code:
        return make_response(False, {"message": "请输入QQ号或验证码"})
    if codes.get(qqid, None) != code:
        return make_response(False, {"message": "验证码错误"})
    elif time.time()-last_send_time[qqid] > config.CODE_TIMEOUT:
        del codes[qqid]
        del last_send_time[qqid]
        return make_response(False, {"message": "验证码已过期"})
    del codes[qqid]
    del last_send_time[qqid]
    session["qq_id"] = qqid
    session.permanment = True
    return make_response(True, {"message": "登录成功"})


@app.route("/api/logout", methods=["POST"])
def paintboard_logout():
    if not session.get("qq_id"):
        return make_response(False, {"message": "你尚未登录！"})
    session.pop(session.get("qq_id"))
    return make_response(True, {"message": "登出成功"})


@app.route("/api/query_login_state", methods=["POST"])
def paintboard_query_login_state():
    return make_response(True, {"isLogin": bool(session.get("qq_id")), "QQID": session.get("qq_id", None)})


@app.route("/api/get_board_data", methods=["POST"])
def paintboard_get_board_data():
    """
    获取绘板数据(像素点)
    """
    group_id = request.form.get("group_id", None)

    if group_id not in config.ENABLE_GROUPS:
        return make_response(False, {"message": "该群未启用绘板"})
    import json
    from main import boards
    return make_response(True, boards.get_board(group_id))


@socket.on("init", namespace="/ws/paintboard")
def handle_paintboard(data):
    from flask_socketio import join_room
    join_room(data["group"])


@app.route("/api/get_enabled_groups", methods=["POST"])
def paintboard_get_enabled_groups():
    pass
    """
    获取支持的群的列表
    """
    return make_response(True, list(config.ENABLE_GROUPS))


@app.route("/api/draw", methods=["POST"])
def paintboard_draw():
    if not session.get("qq_id", None):
        return make_response(False, {"message": "你尚未登录!"})
    user = session.get("qq_id")
    from global_objs import last_paint_time
    from main import boards
    import time
    if user in last_paint_time and time.time()-last_paint_time[user] < config.MIN_PAINT_INTERVAL:
        return make_response(False, {"message": "尚未到冷却时间"})
    last_paint_time[user] = time.time()
    x, y = int(request.form["x"]), int(request.form["y"])
    color = request.form["color"]
    group = request.form["group_id"]
    boards.get_board(group)[x][y] = color
    from flask_socketio import emit
    emit("draw", {
        "x": x, "y": y, "color": color
    }, room=str(group), namespace="/ws/paintboard")
    return make_response(True, {"message": "绘制成功"})
