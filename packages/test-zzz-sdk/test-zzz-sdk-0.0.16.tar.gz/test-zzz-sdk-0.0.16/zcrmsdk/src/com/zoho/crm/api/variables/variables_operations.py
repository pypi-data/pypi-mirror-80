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


class VariablesOperations(object):
	def __init__(self):
		"""Creates an instance of VariablesOperations"""
		pass

	def get_variables(self, param_instance):
		"""
		The method to get variables

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
		api_path = api_path + '/crm/v2/settings/variables'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def create_variables(self, request):
		"""
		The method to create variables

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/variables'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def update_variables(self, request):
		"""
		The method to update variables

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/variables'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def delete_variables(self, param_instance):
		"""
		The method to delete variables

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
		api_path = api_path + '/crm/v2/settings/variables'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.category_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def get_variable_by_id(self, param_instance, id):
		"""
		The method to get variable by id

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/variables/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def update_variable_by_id(self, request, id):
		"""
		The method to update variable by id

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/variables/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def delete_variable(self, id):
		"""
		The method to delete variable

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
		api_path = api_path + '/crm/v2/settings/variables/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.category_method = Constants.REQUEST_METHOD_DELETE
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def get_variable_for_api_name(self, param_instance, api_name):
		"""
		The method to get variable for api name

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			api_name (string) : A string representing the api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if api_name is not None and not isinstance(api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/variables/'
		api_path = api_path + str(api_name)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def update_variable_by_api_name(self, request, api_name):
		"""
		The method to update variable by api name

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			api_name (string) : A string representing the api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if api_name is not None and not isinstance(api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/variables/'
		api_path = api_path + str(api_name)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		try:
			from zcrmsdk.src.com.zoho.crm.api.variables.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')


class GetVariablesParam(object):
	group = Param('group', 'com.zoho.crm.api.Variables.GetVariablesParam')


class DeleteVariablesParam(object):
	ids = Param('ids', 'com.zoho.crm.api.Variables.DeleteVariablesParam')


class GetVariableByIDParam(object):
	group = Param('group', 'com.zoho.crm.api.Variables.GetVariableByIDParam')


class GetVariableForAPINameParam(object):
	group = Param('group', 'com.zoho.crm.api.Variables.GetVariableForAPINameParam')
