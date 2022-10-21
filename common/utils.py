#!/usr/bin/env python
# coding=utf-8

# 通用工具方法

import smtplib
from email.mime.text import MIMEText
import random

import arrow

DATE_FMT = "YYYY-MM-DD HH:mm:ss"
TIME_ZONE = 'Asia/Shanghai'
# chinese_to_number, 单位-数字
unit_dict = {"十": 10, "百": 100, "千": 1000, "万": 10000, "亿": 100000000,
             "拾": 10, "佰": 100, "陌": 100, "仟": 1000, "阡": 1000, "萬": 10000, "億": 100000000}
unit_dict_keys = unit_dict.keys()
digit_dict = {"零": 0, "一": 1, "二": 2, "两": 2, "俩": 2, "三": 3,
              "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
              "壹": 1, "贰": 2, "叁": 3, "肆": 4, "伍": 5, "陆": 6, "柒": 7, "捌": 8, "玖": 9, "弌": 1, "弍": 2, "弎": 3,
              "貳": 2, "陸": 6, "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

# number_to_chinese, 单位-数字
num_dict = {0: "零", 1: "一", 2: "二", 3: "三", 4: "四",
            5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
unit_map = [["", "十", "百", "千"], ["万", "十万", "百万", "千万"],
            ["亿", "十亿", "百亿", "千亿"], ["兆", "十兆", "百兆", "千兆"]]
unit_step = ["万", "亿", "兆"]


def get_local_utc():
    return arrow.utcnow().to('local')


def get_datetime():
    """
    获取当前的时间，按照标准时间格式输出
    :return: 
    """
    return arrow.now().format(DATE_FMT)


def red(words):
    return "\033[31m\033[49m%s\033[0m" % words


def get_ip_address(ifname):
    """
    获取当前服务运行主机的IP
    Args:
        ifname: 网卡适配器名称

    Returns: ip地址

    """
    import socket
    import fcntl
    import struct

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])


def send_mail(from_addr, mailto_list, mail_sub, mail_content, mail_host, mail_user, mail_pass, mail_port=0,
              mail_ssl=False, mail_tls=True):
    """
    发送邮件

    :param from_addr:发件人
    :param mailto_list: 收件人列表
    :param mail_sub: 邮件主题
    :param mail_content: 邮件内容
    :param mail_host: 邮件主机
    :param mail_user: 用户名
    :param mail_pass: 密码
    :param mail_port: 主机端口
    :param mail_ssl: 启用SSL安全连接
    :param mail_tls: 启用TLS安全连接
    :return: 成功/失败
    """

    # 这里的displayName可以任意设置，收到信后，将按照设置显示
    # me = "displayName" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
    msg['Subject'] = mail_sub
    msg['From'] = from_addr
    msg['To'] = ";".join(mailto_list)
    try:
        if mail_ssl:
            s = smtplib.SMTP_SSL()
        else:
            s = smtplib.SMTP()
        s.set_debuglevel(1)
        s.connect(mail_host, mail_port)
        if mail_tls:
            s.starttls()
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(from_addr, mailto_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


class NumberToChinese:
    """
       number to chinese convert
    """

    def __init__(self):
        self.result = ""

    def number_to_str_10000(self, data_str):
        """一万以内的数转成大写"""
        res = []
        count = 0
        # 倒转
        str_rev = reversed(data_str)  # seq -- 要转换的序列，可以是 tuple, string, list 或 range。返回一个反转的迭代器。
        for i in str_rev:
            if i != "0":
                count_cos = count // 4  # 行
                count_col = count % 4  # 列
                res.append(unit_map[count_cos][count_col])
                res.append(num_dict[int(i)])
                count += 1
            else:
                count += 1
                if not res:
                    res.append("零")
                elif res[-1] != "零":
                    res.append("零")
        # 再次倒序，这次变为正序了
        res.reverse()
        # 去掉"一十零"这样整数的“零”
        if res[-1] == "零" and len(res) != 1:
            res.pop()

        return "".join(res)

    def number_to_str(self, data):
        """分段转化"""
        assert type(data) == float or int
        data_str = str(data)
        len_data = len(str(data_str))
        count_cos = len_data // 4  # 行
        count_col = len_data - count_cos * 4  # 列
        if count_col > 0: count_cos += 1

        res = ""
        for i in range(count_cos):
            if i == 0:
                data_in = data_str[-4:]
            elif i == count_cos - 1 and count_col > 0:
                data_in = data_str[:count_col]
            else:
                data_in = data_str[-(i + 1) * 4:-(i * 4)]
            res_ = self.number_to_str_10000(data_in)
            if "0000" == data_in: continue  # 防止零万, 零亿的情况出现
            res = res_ + unit_map[i][0] + res
        # if len(res) > 1 and res.endswith("零"): res = res[:-1]
        return res

    def decimal_chinese(self, data):
        assert type(data) == float or int
        data_str = str(data)
        if "." not in data_str:
            res = self.number_to_str(data_str)
        else:
            data_str_split = data_str.split(".")
            if len(data_str_split) == 2:
                res_start = self.number_to_str(data_str_split[0])
                res_end = "".join([num_dict[int(number)] for number in data_str_split[1]])
                res = res_start + random.sample(["点", "."], 1)[0] + res_end
            else:
                res = str(data)
        return res


if __name__ == '__main__':
    ntc = NumberToChinese()
    print(ntc.decimal_chinese(8))