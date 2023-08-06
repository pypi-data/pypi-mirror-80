try:
    from zcrmsdk.src.com.zoho.crm.api.util.header_param_validator import HeaderParamValidator
    from zcrmsdk.src.com.zoho.crm.api.param import Param
except Exception:
    from .util import HeaderParamValidator
    from .param import Param


class ParameterMap(object):

    """
    This class represents the HTTP parameter name and value.
    """

    def __init__(self):
        """Creates an instance of ParameterMap Class"""

        self.parameter_map = dict()

    def add(self, param, value):

        """
        The method to add parameter name and value.

        Parameters:
            param (Param): A Param class instance.
            value (object): An object containing the parameter value.
        """

        name = param.name
        class_name = param.class_name

        if class_name is not None:
            value = HeaderParamValidator().validate(param, value)

        if name not in self.parameter_map:
            self.parameter_map[name] = str(value)

        else:
            parameter_value = self.parameter_map[name]
            self.parameter_map[name] = parameter_value + ',' + str(value)
