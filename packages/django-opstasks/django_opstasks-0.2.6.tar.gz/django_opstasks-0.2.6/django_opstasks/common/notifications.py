from json import loads, dumps
from logging import getLogger
from requests import request
from django.conf import settings

LOGGER = getLogger('django')
CONSUL_CONFIGS = settings.CONSUL_CONFIGS
CONSUL_SECRETS = settings.CONSUL_SECRETS


def record(func):
    """ 保存发送通知的记录 """
    def _inner(*args, **kwargs):
        _result = func(*args, **kwargs)
        try:
            send_to = args[1] if args[1] else kwargs['send_to']
            message = args[2] if args[2] else kwargs['message']
        except IndexError:
            send_to = kwargs['send_to']
            message = kwargs['message']
        # TODO: 保存发送通知的记录
        LOGGER.info('给"%s"发送了一条通知, 内容是"%s"', send_to, message)
        return _result
    return _inner


class Notification(object):
    """ Notifications subclass must redefine the send method. """

    def send(self, send_to, message, *args, **kwargs):
        """ 发送消息的具体动作, 子类必须重写 """
        raise NotImplementedError('Notifications subclass must redefine the send method.')

    @record
    def info(self, send_to, message, *args, **kwargs):
        message = '[INFO] ' + message
        self.send(send_to, message, *args, **kwargs)

    @record
    def warning(self, send_to, message, *args, **kwargs):
        message = '[WARN] ' + message
        self.send(send_to, message, *args, **kwargs)

    @record
    def error(self, send_to, message, *args, **kwargs):
        message = '[ERROR] ' + message
        self.send(send_to, message, *args, **kwargs)


class EnterpriseWeXinAgent(Notification):
    def __init__(self, corpid, agentid, corpsecret):
        self.agentid = agentid
        self.get_token_baseurl = CONSUL_CONFIGS.get(
            'WX_TOKEN_BASEURL', 'https://qyapi.weixin.qq.com/cgi-bin/gettoken')
        self.send_message_baseurl = CONSUL_CONFIGS.get(
            'WX_MESSAGE_BASEURL', "https://qyapi.weixin.qq.com/cgi-bin/message/send")
        self._token = self._get_access_token(corpid, corpsecret)

    def _get_access_token(self, corpid, corpsecret):
        url = f"{self.get_token_baseurl}?corpid={corpid}&corpsecret={corpsecret}"
        try:
            response = request('GET', url=url)
            if response.status_code == 200:
                context = loads(response.content)
                if context['errcode'] == 0:
                    LOGGER.info('EnterpriseWeXinAgent, Get the access token is successful')
                    return context.get('access_token', None)
                LOGGER.error('EnterpriseWeXinAgent, Get the access token error, %s', context)
            else:
                LOGGER.error(
                    'EnterpriseWeXinAgent, Get access token error, '
                    'status code is %s', response.status_code)
                return None
        except Exception as error:
            LOGGER.exception('EnterpriseWeXinAgent, Get access token error, %s', error)
            return None

    def send(self, send_to, message, *args, **kwargs):
        try:
            url = f'{self.send_message_baseurl}?access_token={self._token}'
            data = {
                "touser" : send_to, "msgtype" : "text", "agentid" : self.agentid,
                "text" : {"content" : message}, "safe":0, "enable_id_trans": 0,
                "enable_duplicate_check": 0, "duplicate_check_interval": 1800
            }
            kwargs.setdefault('data', data)
            response = request('POST', url=url, data=dumps(kwargs['data']))
            if response.status_code == 200:
                context = loads(response.content)
                if context['errcode'] == 0:
                    LOGGER.info('EnterpriseWeXinAgent, send the notification is successful')
                else:
                    LOGGER.error('EnterpriseWeXinAgent, send the notification error, %s', context)
            else:
                LOGGER.error(
                    'EnterpriseWeXinAgent, Unable to send notification, '
                    'status code is %s', response.status_code)
        except Exception as error:
            LOGGER.exception(error)



class EnterpriseWeXinRobot(Notification):
    def send(self, send_to, message, *args, **kwargs):
        pass


class InfraAlert(Notification):
    def send(self, send_to, message, *args, **kwargs):
        pass
