import hashlib


class HashUtil:
    @staticmethod
    def calculate_md5(text):
        """
        计算文本的 md5 哈希值
        :param text:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(text.encode('utf-8'))
        return md5.hexdigest()
