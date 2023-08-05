import json
from urllib.parse import urljoin

import requests
from retrylib.network import retry

from activity_client.client.base import get_request


class ActivityClient:
    more_url = '/serials'
    entity_url = '/serial/%(tid)s'
    exchange_url = 'serial/exchange'

    def __init__(self, host):
        self.host = host

    @retry(attempts_number=3, delay=1)
    def exchange_serial(self, **kwargs):
        """序列码对道具的使用.
        """
        request_url = urljoin(self.host, self.exchange_url)
        headers = {'Content-Type': 'application/json'}
        r = requests.post(request_url, data=json.dumps(kwargs), headers=headers, timeout=10)
        r.raise_for_status()
        return r

    @retry(attempts_number=3, delay=1)
    def delete_serial(self, serial_id):
        """删除指定ID的CDKey, 谨慎考虑, 已使用的无法删除, 只对未使用的物理删除.
        因最小节约原则, 以及业务场景生成后不可逆考虑, 不支持批量删除.
        """
        request_url = urljoin(self.host, self.entity_url) % dict(tid=serial_id)
        r = requests.delete(request_url)
        r.raise_for_status()
        return r

    @retry(attempts_number=3, delay=1)
    def get_serials(self, serial=None, **kwargs):
        """管理端接口, 支持直接传入CDKey码的精确查找, 以及复合条件的查找.

            @param serial: 根据序列码的精确查找, 如果此项存在忽略kwargs.
            @param kwargs: 复合条件查询, 支持数据为:

            creator:              序列码生成的操作员UserId.
            status:               序列码的状态.
            start_time, end_time: 序列码的生成的起始时间、截止时间.
            page, limit:          请求页码, 以及每页的数据条数.
        """
        url = urljoin(self.host, self.more_url)

        payload = {'serial': serial} if serial else kwargs
        return get_request(url, payload=payload)

    @retry(attempts_number=3, delay=1)
    def generate_serials(self, quantity, stale_time, category, creator):
        """批量生成指定的序列码，以Excel文件的形式提供下载.

            @type quantity: int     生成序列码数量, 要求大于0且不大于10000的值.
            @type stale_time: int   前端时间戳, 习惯通常单位为微秒, 后端解析时区为 TZ='Asia/Shanghai'.
            @type category: int     道具ID, 标记当前生成序列码的使用范围.
            @type creator: int      当前登陆的操作员的UserId, 标记生成者是谁.
        """
        request_url = urljoin(self.host, self.more_url)

        headers = {'Content-Type': 'application/json'}
        params = dict(quantity=quantity, stale_time=stale_time, category=category, creator=creator)
        r = requests.post(request_url, data=json.dumps(params), headers=headers, timeout=10)
        r.raise_for_status()
        return r
