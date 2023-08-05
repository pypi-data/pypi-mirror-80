# -*-coding:utf-8-*-
from mobpush.SendRequest import Send


class DeviceV3Client(object):
    baseUrl = "http://api.push.mob.com"
    GET_BY_RID = "/device-v3/getById/"
    GET_DEVICE_DISTRIBUTION = "/device-v3/distribution/"
    GET_BY_ALIAS = "/device-v3/getByAlias/"
    UPDATE_ALIAS = "/device-v3/updateAlias"
    UPDATE_TAGS = "/device-v3/updateTags"
    QUERY_BY_TAGS = "/device-v3/queryByTags"

    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret
        self.send = Send(app_key, app_secret)

    def getByRid(self, registrationId):
        params = {
            "appkey": self.app_key,
            "registrationId": registrationId
        }
        url = self.baseUrl + self.GET_BY_RID + registrationId
        result = self.send.get(
            url=url,
            data=params,
            headers=None
        )
        return result

    def getDeviceDistribution(self):
        params = {
            "appKey": self.app_key
        }
        url = self.baseUrl + self.GET_DEVICE_DISTRIBUTION
        result = self.send.get(
            url=url,
            data=params,
            headers=None
        )
        return result

    def queryByAlias(self, alias):
        params = {
            "appKey": self.app_key,
            "alias": alias
        }
        url = self.baseUrl + self.GET_BY_ALIAS + alias
        result = self.send.get(
            url=url,
            data=params,
            headers=None
        )
        return result

    def queryByTags(self, tags):
        DeviceTagsReq = {
           "appkey": self.app_key,
           "tags": tags
        }
        url = self.baseUrl + self.QUERY_BY_TAGS
        result = self.send.post(
            url=url,
            data=DeviceTagsReq,
            headers=None
        )
        return result

    def updateAlias(self, alias, registrationId):
        DeviceTagsReq = {
            "appkey": self.app_key,
            "alias": alias,
            "registrationId": registrationId,
        }
        url = self.baseUrl + self.UPDATE_ALIAS
        result = self.send.post(
            url=url,
            data=DeviceTagsReq,
            headers=None
        )
        return result

    def updateTags(self, tags, registrationId, opType):
        DeviceTagsReq = {
            "appkey": self.app_key,
            "tags": tags,
            "registrationId": registrationId,
            "opType": opType,
        }
        url = self.baseUrl + self.UPDATE_TAGS
        result = self.send.post(
            url=url,
            data=DeviceTagsReq,
            headers=None
        )
        return result
