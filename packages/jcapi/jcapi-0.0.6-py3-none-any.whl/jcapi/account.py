"""Authenticates with the Control4 API, retrieves account and registered
controller info, and retrieves a bearer token for connecting to a Control4 Director.
"""
import aiohttp
import async_timeout
import json
import logging
import datetime

from .error_handling import checkResponseForError

AUTHENTICATION_ENDPOINT = "https://c.jia.mn/App/a/frame/login.php"
GET_CONTROLLERS_ENDPOINT = "https://c.jia.mn/App/a/frame/setLogin.php"

_LOGGER = logging.getLogger(__name__)


class C4Account:
    def __init__(
        self, username, password, session: aiohttp.ClientSession = None,
    ):
        """Creates a Control4 account object.

        Parameters:
            `username` - Control4 account username/phone_No.

            `password` - Control4 account password.

            `session` - (Optional) Allows the use of an `aiohttp.ClientSession` object for all network requests. This session will not be closed by the library.
            If not provided, the library will open and close its own `ClientSession`s as needed.
        """
        self.username = username
        self.password = password
        self.session = session

    async def __sendAccountAuthRequest(self):
        """Used internally to retrieve an account bearer token. Returns the entire
        JSON response from the Control4 auth API.
        """
        dataDictionary = {
            "rs": "login",
            "rsargs[0]": self.username,
            "rsargs[1]": self.password
        }

        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(
                        AUTHENTICATION_ENDPOINT, data=dataDictionary
                    ) as resp:
                        await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(
                    AUTHENTICATION_ENDPOINT, data=dataDictionary
                ) as resp:
                    await checkResponseForError(await resp.text())
                    return await resp.text()

    async def __get_director_control_url(self, uri):
        """Used internally to send GET requests to the Control4 API,
        authenticated with the account bearer token. Returns the entire JSON
        response from the Control4 auth API.

        Parameters:
            `uri` - Full URI to send GET request to.
        """
        dataDictionary = {
            "rs": "getdturl"
        }
        # _LOGGER.info("token is %s", self.account_bearer_token)
        try:
            url = uri + "?hictoken=" + self.account_bearer_token
            
        except AttributeError:
            msg = "The account bearer token is missing - was your username/password correct? "
            _LOGGER.error(msg)
            raise
        # _LOGGER.info(url)
        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(url, data=dataDictionary) as resp:
                        await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(url, data=dataDictionary) as resp:
                    # await checkResponseForError(await resp.text())
                    # _LOGGER.info(await resp.text())
                    return await resp.text()

    async def __get_controller_token(self, controller_id):
        """get specified controller token. 获取网关的token
        Parameters:
            `controller_id`: ID of the controller. See `getAccountControllers()` for details.
        """
        try:
            url = AUTHENTICATION_ENDPOINT + "?hictoken=" + self.account_bearer_token
        except AttributeError:
            msg = "The account bearer token is missing - was your username/password correct? "
            _LOGGER.error(msg)
            raise
        json_dict = {
            "rs": "changeHIC",
            "rsargs[]": controller_id
        }
        if self.session is None:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.post(
                        url,
                        data=json_dict,
                    ) as resp:
                        await checkResponseForError(await resp.text())
                        return await resp.text()
        else:
            with async_timeout.timeout(10):
                async with self.session.post(
                    url,
                    data=json_dict,
                ) as resp:
                    await checkResponseForError(await resp.text())
                    return await resp.text()

    async def get_account_token(self):
        """Gets an account bearer token for making Control4 online API requests.
        Returns:
            {
                "login":true,
                "info":"1189120558-1589091143-3386663-d2d60108e2-accad487b8",
                "nohic":false,
                "iswebsocket":true,
                "domain":"c.jia.mn"
            }
        """
        data = await self.__sendAccountAuthRequest()
        json_dict = json.loads(data)
        try:
            self.account_bearer_token = json_dict["info"]
            return self.account_bearer_token
        except KeyError:
            msg = "Did not recieve an account bearer token. Is your username/password correct? "
            _LOGGER.error(msg + data)
            raise

    async def get_controller_url(self):
        """Returns a dictionary of the information for all controllers registered to an account.
        get server address.获取接口请求地址

        Returns:
            ```
            {
                "a": "http://c.jia.mn/App/a",
                "b": "http://182.61.44.102:8381/App/b",
                "c": "http://c.jia.mn/App/c",
                "s": "182.61.44.102:8385",
                "wss": "182.61.44.102:8418",
                "fromdev": "mainapp",
                "on": true
            }
            ```
        """
        data = await self.__get_director_control_url(GET_CONTROLLERS_ENDPOINT)
        json_dict = json.loads(data)
        # _LOGGER.info(json_dict["b"])# print(jsonDictionary["b"])
        return json_dict["b"]

    async def get_director_token(self, controller_id):
        """Returns a dictionary with a director bearer token for making Control4 Director API requests, and its expiry time (generally 86400 seconds after current time)
        returns:
            "1189120558-1589243259-560371073-9a35aa5e49-bdb97068cf"

        Parameters:
            `controller_id`: Common name of the controller. See `getAccountControllers()` for details.
        """
        data = await self.__get_controller_token(controller_id)
        token = json.loads(data)
        token_expiration = datetime.datetime.now() + datetime.timedelta(
            seconds=7776000
        )
        # print(f"{token} and {token_expiration}")
        return {
            "token": token,
            "token_expiration": token_expiration,
        }