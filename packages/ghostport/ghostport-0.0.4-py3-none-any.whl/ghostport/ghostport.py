import logging
import requests

GHOSTPORT_API_URL = 'https://api.ghostport.app/v1'


class GhostPort:
    def __init__(self, client_token, api_url=GHOSTPORT_API_URL):
        """
        Initialize GhostPort SDK.

        :param client_token: token obtained from GhostPort
        :param api: (optional) base URL of GhostPort API
        """
        self.client_token = client_token
        self.api_url = api_url

    def get_flag_value(self, key):
        """
        Gets the value of the flag with the specified key

        :param key: the flag key
        :returns: the value, or None
        """
        if not key:
            return None

        all_values = self.get_flag_values()

        if all_values:
            return all_values.get(key)
        else:
            return None

    def get_flag_values(self):
        """
        Gets the value of all flags

        :return: dictionary of the values, or None
        """
        try:
            response = requests.get("{}/evaluate".format(self.api_url),
                                    headers={'X-GhostPort-Client-Token': self.client_token})

            if response.status_code == 200:
                data = response.json()
                if data:
                    return data.get('results')
                else:
                    logger.error("API failed to send results")
                    return None
            else:
                return None

        except Exception as e:
            logger.error("Error loading flag values: %s" % e)
            return None
