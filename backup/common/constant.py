from enum import unique, Enum

from backup.common.util import get_millisecond


@unique
class SignalType(Enum):
    # 信号类型
    COMMON = "common"
    ThreadFinished = "thread finished"


class SignalData:
    def __init__(self, signal_uuid="", signal_type="", data=None, msg="", code=0, timestamp=0):
        """
        统一异步通讯的信号定义格式
        :param signal_uuid:
        :param signal_type:
        :param data:
        :param msg:
        :param code:
        :param timestamp:
        """
        self.signal_uuid = signal_uuid or get_millisecond()  # 信号唯一 id，必选
        self.signal_type = signal_type or SignalType.COMMON.value  # 信号类型，必选
        self.data = data or {}  # 信号数据
        self.msg = msg  # 信号提示信息
        self.code = code  # 信号状态码
        self.timestamp = timestamp or get_millisecond()  # 信号发出时间

    def __str__(self):
        return f"SignalData(signal_uuid={self.signal_uuid}, signal_type={self.signal_type})"


@unique
class ResponseCode(Enum):
    # 通用状态码
    Success = 0
    Failed = 10000

    mapping_code = {
        # 通用状态码
        0: "成功",
        10000: "失败",
    }

    @staticmethod
    def get_mapping_code(code):
        return ResponseCode.mapping_code.value.get(code, "")
