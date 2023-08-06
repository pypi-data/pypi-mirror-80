try:
    import requests
    import logging
    import json
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants

except Exception:
    from .constants import Constants
    import requests
    import logging
    import json


class APIHTTPConnector(object):
    """
    This module is to make HTTP connections, trigger the requests and receive the response.
    """

    def __init__(self):

        """
        Creates an APIHTTPConnector class instance with the specified parameters.
        """

        self.url = None
        self.headers = dict()
        self.request_method = None
        self.parameters = dict()
        self.request_body = None
        self.file = False
        self.content_type = None

    def add_header(self, header_name, header_value):

        """
        The method to add API request header name and value.

        Parameters:
            header_name (str) : A String containing the API request header name.
            header_value (str) : A String containing the API request header value.
        """

        self.headers[header_name] = header_value

    def add_param(self, param_name, param_value):

        """
        The method to add API request parameter name and value.

        Parameters:
            param_name (str) : A String containing the API request parameter name.
            param_value (str) : A String containing the API request parameter value.
        """

        self.parameters[param_name] = param_value

    def fire_request(self, converter_instance):

        """
        This method makes a request to the Zoho CRM Rest API

        Parameters:
            converter_instance (Converter) : A Converter class instance to call append_to_request method.

        Returns:
            requests.Response : An object of requests.Response
        """

        response = None
        logger = logging.getLogger('SDKLogger')

        if self.content_type is not None:
            self.set_content_type_header()

        logger.info(self.__str__())

        if self.request_method == Constants.REQUEST_METHOD_GET:
            response = requests.get(self.url, headers=self.headers, params=self.parameters, allow_redirects=False)

        elif self.request_method == Constants.REQUEST_METHOD_PUT:
            data = None
            if self.request_body is not None:
                data = converter_instance.append_to_request(self, self.request_body)

            response = requests.put(self.url, data=data, params=self.parameters, headers=self.headers, allow_redirects=False)

        elif self.request_method == Constants.REQUEST_METHOD_POST:
            data = None
            if self.request_body is not None:
                data = converter_instance.append_to_request(self, self.request_body)

            if self.file:
                response = requests.post(self.url, files=data, headers=self.headers, allow_redirects=False, data={})

            else:
                response = requests.post(self.url, data=data, params=self.parameters, headers=self.headers, allow_redirects=False)

        elif self.request_method == Constants.REQUEST_METHOD_DELETE:
            response = requests.delete(self.url, headers=self.headers, params=self.parameters, allow_redirects=False)

        return response

    def __str__(self):
        request_headers = self.headers.copy()
        request_headers[Constants.AUTHORIZATION] = Constants.CANT_DISCLOSE

        return self.request_method + ' - ' + Constants.URL + ' = ' + self.url + ' , ' + Constants.HEADERS + ' = ' + json.dumps(request_headers) \
               + ' , ' + Constants.PARAMS + ' = ' + json.dumps(self.parameters) + '.'

    def set_content_type_header(self):
        for url in Constants.SET_TO_CONTENT_TYPE:
            if url in self.url:
                self.headers[Constants.CONTENT_TYPE_HEADER] = self.content_type
                return
