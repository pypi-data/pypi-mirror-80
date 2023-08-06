# coding: utf-8
import redis
from rj_utils.utils_file import file2dict


class RedisUtils(object):
    """
    Redis操作类
    配置文件格式：
        {
            "redisip": "127.0.0.1",
            "redisport": "6379",
            "passwd": "redis123",
            "db": 0
        }
    """

    def __init__(self, conf_path):
        """
        :param conf_path: 配置文件路径 ../redis.conf
        """
        self.config = file2dict(conf_path)
        if self.config['passwd'] is None:
            self.r = redis.Redis(host=self.config['redisip'], port=self.config['redisport'], db=self.config['db'])
        else:
            self.r = redis.Redis(host=self.config['redisip'], port=self.config['redisport'], db=self.config['db'],
                                 password=self.config['passwd'])

    def cleanup(self):
        # 清理Redis当前数据库
        self.r.flushdb()

    def lookup_redist_info(self):
        # 查询Redis配置
        info = self.r.info()
        return info

    def set_key_value(self, key, value):
        # 设置键值对key<-->value
        return self.r.set(key, value)

    def get_key_value(self, key):
        # 查询键值对
        return self.r.get(key)

    def set_hkey_value(self, name, key, value):
        # 设置哈希键值对key<-->value
        return self.r.hset(name, key, value)

    def get_hkey_value(self, name, key):
        # 设置哈希键值对key<-->value
        return self.r.hget(name, key)

    def save(self):
        # 强行保存数据到硬盘
        return self.r.save()

    def get_keys(self):
        # 获取当前数据库里面所有键值
        return self.r.keys()

    def delete_key(self, key):
        # 删除某个键
        return self.r.delete(key)

    def push_list_value(self, listname, value):
        # 推入到队列
        return self.r.lpush(listname, value)

    def pull_list_range(self, listname, starpos=0, endpos=-1):
        # 获取队列某个连续片段
        return self.r.lrange(listname, starpos, endpos)

    def get_list_len(self, listname):
        # 获取队列长度
        return self.r.llen(listname)


def main():
    ri = RedisUtils('../redis.conf')
    ri.lookup_redist_info()
    ri.set_key_value('test1', 1)
    ri.push_list_value('test2', 1)
    ri.push_list_value('test2', 2)


if __name__ == '__main__':
    main()
