try:
	from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
except Exception:
	from ..exception import SDKException
	from ..util import APIResponse, CommonAPIHandler, Constants


class LayoutsOperations(object):
	def __init__(self, module):
		"""
		Creates an instance of LayoutsOperations with the given parameters

		Parameters:
			module (string) : A string representing the module
		"""

		if module is not None and not isinstance(module, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module EXPECTED TYPE: str', None, None)
		
		self.__module = module


	def get_layouts(self):
		"""
		The method to get layouts

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/layouts'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.add_param('module', self.__module)
		try:
			from zcrmsdk.src.com.zoho.crm.api.layouts.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def get_layout(self, id):
		"""
		The method to get layout

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
		api_path = api_path + '/crm/v2/settings/layouts/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.add_param('module', self.__module)
		try:
			from zcrmsdk.src.com.zoho.crm.api.layouts.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')
