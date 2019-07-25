# 最短的发送验证码的间隔
MIN_SENDCODE_INTERVAL = 10
# 验证码过期时间
CODE_TIMEOUT = 120
# 发送验证码的URL
# 发送验证码时将POST此URL，并填写token,target,content
SEND_CODE_URL = "http://localhost:5002/paintboard/send_code"
SEND_CODE_TOKEN = "20w-o2o0"

PORT = 8080
HOST = "0.0.0.0"
DEBUG = False

SESSION_KEY = "jweiojdoijewiu"

# 绘板默认大小(列数,行数)
DEFAULT_SIZE = (200, 200)

# 绘板默认颜色
DEFAULT_COLOR = "#ff3333"
# 存储绘板数据的文件
SAVE_FILE = "boards.data"
# 启用绘板的群(字符串)
ENABLE_GROUPS = {

}
# 自动保存间隔
SAVE_INTERVAL = 20
# 画两个像素的时间间隔
MIN_PAINT_INTERVAL = 5
