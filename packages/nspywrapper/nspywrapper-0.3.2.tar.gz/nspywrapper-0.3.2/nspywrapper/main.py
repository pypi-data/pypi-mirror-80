"""
    Copyright 2020 Andrew Brown (aka SherpDaWerp)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from .parser import *

from xml.parsers.expat import ExpatError
from urllib3 import ProxyManager, PoolManager, make_headers
from time import time, sleep


API_VERSION = "11"


class nsRequests:
    def __init__(self, agent, delay=0, proxy_user=None, proxy_pass=None, proxy_ip=None, proxy_port=None):
        if agent == "":
            raise RuntimeError("UserAgent must be set!")

        self.userAgent = agent + ", using SherpDaWerp's nspy-wrapper tool."
        self.apiNormalDelay = 600 + delay
        self.apiTGDelay = 30000 + delay
        self.apiRecruitDelay = 180000 + delay
        self.lastRequestTime = 0
        # Default authentication array. auth[0] is the password, auth[1] is the X-Autologin and auth[2] is the X-Pin

        if (proxy_user is not None) & (proxy_pass is not None) & (proxy_ip is not None) & (proxy_port is not None):
            proxy_headers = make_headers(proxy_basic_auth=proxy_user+":"+proxy_pass)
            self.request_manager = ProxyManager(proxy_ip+":"+proxy_port, headers=proxy_headers)
        else:
            self.request_manager = PoolManager()

    def make_request(self, url: str, headers: dict, delay: int = None):
        """ makes the request to the API

        :param url: the url to make the request to
        :param headers: the headers to be supplied with the request
        :param delay: the delay before making the request
        :return: the response of the request
        """
        if delay is None:
            delay = self.apiNormalDelay

        url += "&v="+API_VERSION
        
        millis = int(round(time() * 1000))
        # read the current time in milliseconds

        if millis > (self.lastRequestTime + delay):
            # if the current time is more than self.apiDelay milliseconds after the last request, make the request
            response = self.request_manager.request(method="GET", url=url, headers=headers)
            self.lastRequestTime = millis
        else:
            # if the current time is not more than self.apiDelay milliseconds after the last request, wait until it is
            time_dif = delay - (millis - self.lastRequestTime)
            # work out how much more time the program needs to wait to fulfil the apiDelay, then wait that long
            sleep(time_dif / 1000)

            # make the request, then reset lastRequestTime
            response = self.request_manager.request(method="GET", url=url, headers=headers)

            self.lastRequestTime = millis + delay

        return response

    def world(self, shards: str or list, parameters: dict = None):
        """ Makes a request to the NationStates API of a World shard

        :param shards: The shards to be requested
        :param parameters: The parameters for the shards

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?"
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        if shards:
            # if shards were given
            url += "q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key+"="+parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers)
        return nsResponse(data, url)

    def nation(self, nation: str, shards: str or list = None, parameters: dict = None, auth: tuple = ("", "", "")):
        """ Makes a request to the NationStates API of a Nation shard

        :param nation: The nation to be requested
        :param shards: The shards to be requested
        :param parameters: The parameters for the shards
        :param auth: optional authentication for private commands

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?nation="
        # sets the base URL

        nation_url = nation.replace(" ", "_")
        url += nation_url+"&"

        if auth[0] != "":
            headers = {'User-Agent': self.userAgent,
                       'X-Password': auth[0],
                       'X-Autologin': auth[1],
                       'X-Pin': auth[2]}
        else:
            headers = {'User-Agent': self.userAgent}

        if shards:
            # if shards were given
            url += "q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers)
        return nsResponse(data, url)

    def telegram(self, client: str, tgid: str, key: str, recipient: str, recruitment: bool = False):
        """ Makes a request to the NationStates API to send a Telegram

        :param client: the API client key
        :param tgid: the ID of the telegram to be sent
        :param key: the Key of the telegram to be sent
        :param recipient: the nation to send the Telegram to
        :param recruitment: whether the TG is recruitment or not. Defaults to False.

        :return tuple: the response data from the api
        """

        url = "https://www.nationstates.net/cgi-bin/api.cgi?"
        headers = {'User-Agent': self.userAgent}

        nation_url = recipient.replace(" ", "_")

        url = url + "a=sendTG&client=" + client + "&tgid=" + tgid + "&key=" + key + "&to=" + nation_url

        if recruitment:
            data = self.make_request(url, headers, self.apiRecruitDelay)
        else:
            data = self.make_request(url, headers, self.apiTGDelay)

        response = nsResponse(data, url)
        return response

    def command(self, nation: str, command: str, parameters: dict, auth: tuple = ("", "", "")):
        """ Sends a command to the NS Api

        :param nation: the nation that the command is executed on
        :param command: the command to be issued to the API
        :param parameters: the shards issued alongside said command
        :param auth: authentication for the nation that the command is executed onn

        :return tuple: the response data from the api
        """
        nation_url = nation.replace(" ", "_")
        url = "https://www.nationstates.net/cgi-bin/api.cgi?nation=" + nation_url

        if auth[0] != "":
            headers = {'User-Agent': self.userAgent,
                       'X-Password': auth[0],
                       'X-Autologin': auth[1],
                       'X-Pin': auth[2]}
        else:
            headers = {'User-Agent': self.userAgent}

        url = url + "&c=" + command

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += "&"
            for param in param_list:
                url += param + "&"
            url = url[:-1]

        data = self.make_request(url, headers)
        return nsResponse(data, url)

    def region(self, region: str, shards: str or list = None, parameters: dict = None):
        """ Makes a request to the NationStates API of a Region shard

            :param region: the region to be requested
            :param shards: The shards to be requested
            :param parameters: The parameters for the shards

            :return: the response data from the api
        """
        region_url = region.replace(" ", "_")
        url = "https://www.nationstates.net/cgi-bin/api.cgi?region="+region_url+"&"
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        if shards:
            # if shards were given
            url += "q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers)
        return nsResponse(data, url)

    def world_assembly(self, council: int = 1, shards: str or list = None, parameters: dict = None):
        """ Makes a request to the NationStates API of a World shard

        :param council: the id of the council to ask about (1 is ga or 2 is sc)
        :param shards: the shards to ask about
        :param parameters: the parameters of the resolution to ask about

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?wa="+str(council)
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        if shards is not None:
            # if shards were given
            url += "&q="

            if isinstance(shards, list):
                # if shards is an array of multiple elements, then put the full list of shards in the url
                for shard in shards:
                    url += shard + "+"
                url = url[:-1]
            else:
                # if shards is not an array, or if shards has only one element, then put the single shard in the url
                url += shards

        if parameters:
            # if parameters were given
            param_list = [key + "=" + parameters[key] for key in parameters]
            url += ";"
            for param in param_list:
                url += param + ";"
            url = url[:-1]

        data = self.make_request(url, headers)
        return nsResponse(data, url)

    def verify(self, nation: str, checksum: str, token: str or list = ""):
        """ Makes an authentication request to the NS API with the given token.
            Note the "verbose" flag - this allows the user to see all headers instead of just the success header.
        
        :param nation: the nation being verified
        :param checksum: the checksum provided by the user
        :param token: optional site-specific token for verification

        :return: the response data from the api
        """
        url = "https://www.nationstates.net/cgi-bin/api.cgi?a=verify&nation="
        headers = {'User-Agent': self.userAgent}
        # sets the base URL, and sets the useragent in the headers

        url += nation + "&checksum=" + checksum

        if token != "":
            url += "&token="+token

        data = self.make_request(url, headers)
        return nsResponse(data, url)


class nsResponse:
    def __init__(self, response, url):
        self.original_response = response

        self.status = response.status
        self.headers = response.headers

        self._url = url

        if response.status == 200:
            try:
                self.data = nsParser.data_to_dict(response.data)
            except ExpatError:
                raise MalformedXML("Malformed XML returned when accessing page.", data=response, url=url)
        else:
            self.data = response.data

    def request_url(self):
        return self._url

    def get_auth(self):
        try:
            xautologin = self.headers["X-autologin"]
            xpin = self.headers["X-pin"]

            returned_auth = [xautologin, xpin]

            return returned_auth
        except KeyError:
            raise MissingHeaders("X-Autologin or X-Pin unavailable in API request headers.")
