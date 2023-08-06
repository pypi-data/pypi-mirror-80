from rediscluster import RedisCluster


class ConnectionFactory(object):
    def __init__(self, options):
        self.options = options

    def make_connection_params_from_url(self, url):
        """
        参数扩展的代码
        """
        params = dict(url=url, decode_responses=False)
        return params

    def make_connection_params(self, url_list):
        """
        参数扩展的代码
        """
        params = dict(startup_nodes=url_list, decode_responses=False)
        options = self.options.get("OPTIONS", {})
        password = options.get("password", None)
        if password:
            params.update(password=password)
        ssl = options.get("ssl", False)
        if ssl:
            params.update(ssl=True)
        return params

    def connect(self, url_list):
        """
        连接 rediscluster客户端
        """
        if isinstance(url_list[0], str):
            params = self.make_connection_params_from_url(url_list[0])
            connection = self.get_connection_from_url(**params)
        else:
            params = self.make_connection_params(url_list)
            connection = self.get_connection(**params)
        return connection

    def get_connection_from_url(self, **kwargs):
        return RedisCluster.from_url(**kwargs)

    def get_connection(self, **kwargs):
        return RedisCluster(**kwargs)
