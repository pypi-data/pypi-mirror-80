try:
	from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.parameter_map import ParameterMap
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
	from zcrmsdk.src.com.zoho.crm.api.param import Param
except Exception:
	from ..exception import SDKException
	from ..parameter_map import ParameterMap
	from ..util import APIResponse, CommonAPIHandler, Constants
	from ..param import Param


class FieldsOperations(object):
	def __init__(self, module):
		"""
		Creates an instance of FieldsOperations with the given parameters

		Parameters:
			module (string) : A string representing the module
		"""

		if module is not None and not isinstance(module, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module EXPECTED TYPE: str', None, None)
		
		self.__module = module


	def get_fields(self, param_instance):
		"""
		The method to get fields

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/fields'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		handler_instance.add_param('module', self.__module)
		try:
			from zcrmsdk.src.com.zoho.crm.api.fields.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def get_field(self, id):
		"""
		The method to get field

		Parameters:
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/fields/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.add_param('module', self.__module)
		try:
			from zcrmsdk.src.com.zoho.crm.api.fields.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')


class GetFieldsParam(object):
	type = Param('type', 'com.zoho.crm.api.Fields.GetFieldsParam')
