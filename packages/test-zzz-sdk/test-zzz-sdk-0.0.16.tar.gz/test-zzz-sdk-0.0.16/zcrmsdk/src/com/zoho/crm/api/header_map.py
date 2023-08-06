try:
    from zcrmsdk.src.com.zoho.crm.api.util.header_param_validator import HeaderParamValidator
    from zcrmsdk.src.com.zoho.crm.api.header import Header
except Exception:
    from .util import HeaderParamValidator
    from .header import Header


class HeaderMap(object):

    """
    This class represents the HTTP header name and value.
    """

    def __init__(self):
        """Creates an instance of HeaderMap Class"""

        self.header_map = dict()

    def add(self, header, value):

        """
        The method to add the parameter name and value.

        Parameters:
            header (Header): A Header class instance.
            value (object): An object containing the header value.
        """

        name = header.name
        class_name = header.class_name

        if class_name is not None:
            value = HeaderParamValidator().validate(header, value)

        if name not in self.header_map:
            self.header_map[name] = str(value)

        else:
            header_value = self.header_map[name]
            self.header_map[name] = header_value + ',' + str(value)
