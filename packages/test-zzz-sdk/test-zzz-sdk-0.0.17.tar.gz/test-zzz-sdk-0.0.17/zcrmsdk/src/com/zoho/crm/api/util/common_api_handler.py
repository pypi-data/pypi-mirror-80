
try:
    import json
    import platform
    import urllib3
    import logging
    from zcrmsdk.src.com.zoho.crm.api.util.api_http_connector import APIHTTPConnector
    from zcrmsdk.src.com.zoho.crm.api.util.json_converter import JSONConverter
    from zcrmsdk.src.com.zoho.crm.api.util.xml_converter import XMLConverter
    from zcrmsdk.src.com.zoho.crm.api.util.form_data_converter import FormDataConverter
    from zcrmsdk.src.com.zoho.crm.api.util.downloader import Downloader
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants
    from zcrmsdk.src.com.zoho.crm.api.util.api_response import APIResponse
    from zcrmsdk.src.com.zoho.crm.api.header_map import HeaderMap
    from zcrmsdk.src.com.zoho.crm.api.header import Header
    from zcrmsdk.src.com.zoho.crm.api.parameter_map import ParameterMap
    from zcrmsdk.src.com.zoho.crm.api.param import Param
    from zcrmsdk.src.com.zoho.crm.api.exception import SDKException

except Exception:
    import json
    import platform
    import urllib3
    import logging
    from .api_http_connector import APIHTTPConnector
    from .json_converter import JSONConverter
    from .constants import Constants
    from .api_response import APIResponse
    from ..header_map import HeaderMap
    from ..header import Header
    from ..parameter_map import ParameterMap
    from ..param import Param
    from ..exception import SDKException


class CommonAPIHandler(object):

    """
    This class to process the API request and its response.
    Construct the objects that are to be sent as parameters or request body with the API.
    The Request parameter, header and body objects are constructed here.
    Process the response JSON and converts it to relevant objects in the library.
    """
    logger = logging.getLogger('SDKLogger')

    def __init__(self):

        self.api_path = None
        self.header = HeaderMap()
        self.param = ParameterMap()
        self.request = None
        self.http_method = None
        self.module_api_name = None
        self.content_type = None
        self.category_method = None
        self.mandatory_checker = None

    def add_param(self, param_name, param_value):

        """
        The method to add an API request parameter.

        Parameters:
            param_name (str) : A string containing the API request parameter name.
            param_value (object) : An object containing the API request parameter value.
        """

        if self.param is None:
            self.param = ParameterMap()

        self.param.add(Param(param_name), param_value)

    def add_header(self, header_name, header_value):

        """
        The method to add an API request header.

        Parameters:
            header_name (str) : A string containing the API request header name.
            header_value (object) : An object containing the API request header value.
        """

        if self.header is None:
            self.header = HeaderMap()

        self.header.add(Header(header_name), header_value)

    def api_call(self, class_name, encode_type):

        """
        This method of constructing API request and response details. To make the Zoho CRM API calls.
        :param class_name: A str containing the method return type.
        :param encode_type: A str containing the expected API response content type.
        :return:  A APIResponse representing the Zoho CRM API response instance or None.
        :raise: SDKException
        """
        try:
            from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
        except Exception:
            from ..initializer import Initializer

        if Initializer.get_initializer() is None:
            raise SDKException(code=Constants.SDK_UNINITIALIZATION_ERROR, message=Constants.SDK_UNINITIALIZATION_MESSAGE)

        connector = APIHTTPConnector()
        try:
            self.set_api_url(connector)
        except SDKException as e:
            CommonAPIHandler.logger.error(Constants.SET_API_URL_EXCEPTION + e.__str__())
            raise e
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            CommonAPIHandler.logger.error(Constants.SET_API_URL_EXCEPTION + sdk_exception.__str__())
            raise sdk_exception

        connector.request_method = self.http_method
        connector.content_type = self.content_type

        if self.header is not None and len(self.header.header_map) > 0:
            connector.headers = self.header.header_map

        if self.param is not None and len(self.param.parameter_map) > 0:
            connector.parameters = self.param.parameter_map

        try:
            Initializer.get_initializer().token.authenticate(connector)
        except SDKException as e:
            CommonAPIHandler.logger.info(Constants.AUTHENTICATION_EXCEPTION + e.__str__())
            raise e
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            CommonAPIHandler.logger.error(Constants.AUTHENTICATION_EXCEPTION + sdk_exception.__str__())
            raise sdk_exception

        convert_instance = None

        if self.content_type is not None and (self.http_method == Constants.REQUEST_METHOD_POST or self.http_method == Constants.REQUEST_METHOD_PUT or self.http_method == Constants.REQUEST_METHOD_PATCH):
            try:
                convert_instance = self.get_converter_class_instance(self.content_type.lower())
                request = convert_instance.form_request(self.request, self.request.__class__.__module__, 0, None)
            except SDKException as e:
                CommonAPIHandler.logger.info(Constants.FORM_REQUEST_EXCEPTION + e.__str__())
                raise e
            except Exception as e:
                sdk_exception = SDKException(cause=e)
                CommonAPIHandler.logger.error(Constants.FORM_REQUEST_EXCEPTION + sdk_exception.__str__())
                raise sdk_exception

            connector.request_body = request

        try:
            connector.headers[Constants.ZOHO_SDK] = platform.system() + "/" + platform.release() + " python/" + platform.python_version() + ":" + Constants.SDK_VERSION
            response = connector.fire_request(convert_instance)
            return_object = None

            if Constants.CONTENT_TYPE in response.headers:
                content_type = response.headers[Constants.CONTENT_TYPE]

                if ";" in content_type:
                    content_type = content_type.rpartition(";")[0]

                convert_instance = self.get_converter_class_instance(content_type)
                return_object = convert_instance.get_wrapped_response(response, class_name)

            else:
                CommonAPIHandler.logger.info(response.__str__())

            return APIResponse(response.headers, response.status_code, return_object)
        except SDKException as e:
            CommonAPIHandler.logger.info(Constants.API_CALL_EXCEPTION + e.__str__())
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            CommonAPIHandler.logger.error(Constants.API_CALL_EXCEPTION + sdk_exception.__str__())
            raise sdk_exception

    def get_converter_class_instance(self, encode_type):

        """
        This method to get a Converter class instance.
        :param encode_type: A str containing the API response content type.
        :return: A Converter class instance.
        """

        switcher = {

            "application/json": JSONConverter(self),

            "text/plain": JSONConverter(self),

            "text/html": JSONConverter(self),

            "application/xml": XMLConverter(self),

            "text/xml": XMLConverter(self),

            "multipart/form-data": FormDataConverter(self),

            "application/x-download": Downloader(self),

            "image/png": Downloader(self),

            "image/jpeg": Downloader(self),

            "application/zip": Downloader(self),

            "image/gif": Downloader(self),

            "text/csv": Downloader(self),

            "image/tiff": Downloader(self),

            "application/octet-stream": Downloader(self),
        }

        return switcher.get(encode_type, None)

    def set_api_url(self, connector):
        try:
            from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
        except Exception:
            from ..initializer import Initializer

        api_path = ''

        if Constants.HTTP in self.api_path:
            if Constants.CONTENT_API_URL in self.api_path:
                api_path = Initializer.get_initializer().environment.file_upload_url

                try:
                    url_parse = urllib3.util.parse_url(self.api_path)
                    path = url_parse.path
                except Exception as ex:
                    raise SDKException(code=Constants.INVALID_URL_ERROR, cause=ex)

                api_path = api_path + path
            else:
                if str(self.api_path)[:1].__eq__('/'):
                    self.api_path = self.api_path[1:]

                api_path = api_path + self.api_path
        else:
            api_path = Initializer.get_initializer().environment.url
            api_path = api_path + self.api_path

        connector.url = api_path
