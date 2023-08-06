try:
	from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.parameter_map import ParameterMap
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Utility, Constants
	from zcrmsdk.src.com.zoho.crm.api.param import Param
	from zcrmsdk.src.com.zoho.crm.api.header import Header
	from zcrmsdk.src.com.zoho.crm.api.header_map import HeaderMap
except Exception:
	from ..exception import SDKException
	from ..parameter_map import ParameterMap
	from ..util import APIResponse, CommonAPIHandler, Utility, Constants
	from ..param import Param
	from ..header import Header
	from ..header_map import HeaderMap


class RecordOperations(object):
	def __init__(self):
		"""Creates an instance of RecordOperations"""
		pass

	def get_record(self, param_instance, header_instance, module_api_name, id):
		"""
		The method to get record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			header_instance (HeaderMap) : An instance of HeaderMap
			module_api_name (string) : A string representing the module_api_name
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if header_instance is not None and not isinstance(header_instance, HeaderMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: header_instance EXPECTED TYPE: HeaderMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		handler_instance.header = header_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def update_record(self, request, module_api_name, id):
		"""
		The method to update record

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string representing the module_api_name
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def delete_record(self, param_instance, module_api_name, id):
		"""
		The method to delete record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string representing the module_api_name
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.category_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def get_records(self, param_instance, header_instance, module_api_name):
		"""
		The method to get records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			header_instance (HeaderMap) : An instance of HeaderMap
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if header_instance is not None and not isinstance(header_instance, HeaderMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: header_instance EXPECTED TYPE: HeaderMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		handler_instance.header = header_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def create_records(self, request, module_api_name):
		"""
		The method to create records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def update_records(self, request, module_api_name):
		"""
		The method to update records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def delete_records(self, param_instance, module_api_name):
		"""
		The method to delete records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.category_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def upsert_records(self, request, module_api_name):
		"""
		The method to upsert records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/upsert'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_ACTION
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def get_deleted_records(self, param_instance, header_instance, module_api_name):
		"""
		The method to get deleted records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			header_instance (HeaderMap) : An instance of HeaderMap
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if header_instance is not None and not isinstance(header_instance, HeaderMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: header_instance EXPECTED TYPE: HeaderMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/deleted'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		handler_instance.header = header_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.deleted_records_handler import DeletedRecordsHandler
		except Exception:
			from .deleted_records_handler import DeletedRecordsHandler
		return handler_instance.api_call(DeletedRecordsHandler.__module__, 'application/json')

	def search_records(self, param_instance, module_api_name):
		"""
		The method to search records

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/search'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def convert_lead(self, request, id):
		"""
		The method to convert lead

		Parameters:
			request (ConvertBodyWrapper) : An instance of ConvertBodyWrapper
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.convert_body_wrapper import ConvertBodyWrapper
		except Exception:
			from .convert_body_wrapper import ConvertBodyWrapper

		if request is not None and not isinstance(request, ConvertBodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: ConvertBodyWrapper', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/Leads/'
		api_path = api_path + str(id)
		api_path = api_path + '/actions/convert'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		Utility.get_fields("Deals")
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.convert_action_handler import ConvertActionHandler
		except Exception:
			from .convert_action_handler import ConvertActionHandler
		return handler_instance.api_call(ConvertActionHandler.__module__, 'application/json')

	def get_photo(self, module_api_name, id):
		"""
		The method to get photo

		Parameters:
			module_api_name (string) : A string representing the module_api_name
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(id)
		api_path = api_path + '/photo'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.download_handler import DownloadHandler
		except Exception:
			from .download_handler import DownloadHandler
		return handler_instance.api_call(DownloadHandler.__module__, 'application/x-download')

	def upload_photo(self, request, module_api_name, id):
		"""
		The method to upload photo

		Parameters:
			request (FileBodyWrapper) : An instance of FileBodyWrapper
			module_api_name (string) : A string representing the module_api_name
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.file_body_wrapper import FileBodyWrapper
		except Exception:
			from .file_body_wrapper import FileBodyWrapper

		if request is not None and not isinstance(request, FileBodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: FileBodyWrapper', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(id)
		api_path = api_path + '/photo'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'multipart/form-data'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.file_handler import FileHandler
		except Exception:
			from .file_handler import FileHandler
		return handler_instance.api_call(FileHandler.__module__, 'application/json')

	def delete_photo(self, module_api_name, id):
		"""
		The method to delete photo

		Parameters:
			module_api_name (string) : A string representing the module_api_name
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(id)
		api_path = api_path + '/photo'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.category_method = Constants.REQUEST_METHOD_DELETE
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.file_handler import FileHandler
		except Exception:
			from .file_handler import FileHandler
		return handler_instance.api_call(FileHandler.__module__, 'application/json')

	def mass_update_records(self, request, module_api_name):
		"""
		The method to mass update records

		Parameters:
			request (MassUpdateBodyWrapper) : An instance of MassUpdateBodyWrapper
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.record.mass_update_body_wrapper import MassUpdateBodyWrapper
		except Exception:
			from .mass_update_body_wrapper import MassUpdateBodyWrapper

		if request is not None and not isinstance(request, MassUpdateBodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: MassUpdateBodyWrapper', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/actions/mass_update'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		Utility.get_fields(module_api_name)
		handler_instance.module_api_name = module_api_name
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.mass_update_action_handler import MassUpdateActionHandler
		except Exception:
			from .mass_update_action_handler import MassUpdateActionHandler
		return handler_instance.api_call(MassUpdateActionHandler.__module__, 'application/json')

	def get_mass_update_status(self, param_instance, module_api_name):
		"""
		The method to get mass update status

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string representing the module_api_name

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/actions/mass_update'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.record.mass_update_response_handler import MassUpdateResponseHandler
		except Exception:
			from .mass_update_response_handler import MassUpdateResponseHandler
		return handler_instance.api_call(MassUpdateResponseHandler.__module__, 'application/json')


class GetRecordParam(object):
	approved = Param('approved', 'com.zoho.crm.api.Record.GetRecordParam')
	converted = Param('converted', 'com.zoho.crm.api.Record.GetRecordParam')
	cvid = Param('cvid', 'com.zoho.crm.api.Record.GetRecordParam')
	uid = Param('uid', 'com.zoho.crm.api.Record.GetRecordParam')
	fields = Param('fields', 'com.zoho.crm.api.Record.GetRecordParam')
	startdatetime = Param('startDateTime', 'com.zoho.crm.api.Record.GetRecordParam')
	enddatetime = Param('endDateTime', 'com.zoho.crm.api.Record.GetRecordParam')
	territory_id = Param('territory_id', 'com.zoho.crm.api.Record.GetRecordParam')
	include_child = Param('include_child', 'com.zoho.crm.api.Record.GetRecordParam')


class GetRecordHeader(object):
	if_modified_since = Header('If-Modified-Since', 'com.zoho.crm.api.Record.GetRecordHeader')


class DeleteRecordParam(object):
	wf_trigger = Param('wf_trigger', 'com.zoho.crm.api.Record.DeleteRecordParam')


class GetRecordsParam(object):
	approved = Param('approved', 'com.zoho.crm.api.Record.GetRecordsParam')
	converted = Param('converted', 'com.zoho.crm.api.Record.GetRecordsParam')
	cvid = Param('cvid', 'com.zoho.crm.api.Record.GetRecordsParam')
	ids = Param('ids', 'com.zoho.crm.api.Record.GetRecordsParam')
	uid = Param('uid', 'com.zoho.crm.api.Record.GetRecordsParam')
	fields = Param('fields', 'com.zoho.crm.api.Record.GetRecordsParam')
	sort_by = Param('sort_by', 'com.zoho.crm.api.Record.GetRecordsParam')
	sort_order = Param('sort_order', 'com.zoho.crm.api.Record.GetRecordsParam')
	page = Param('page', 'com.zoho.crm.api.Record.GetRecordsParam')
	per_page = Param('per_page', 'com.zoho.crm.api.Record.GetRecordsParam')
	startdatetime = Param('startDateTime', 'com.zoho.crm.api.Record.GetRecordsParam')
	enddatetime = Param('endDateTime', 'com.zoho.crm.api.Record.GetRecordsParam')
	territory_id = Param('territory_id', 'com.zoho.crm.api.Record.GetRecordsParam')
	include_child = Param('include_child', 'com.zoho.crm.api.Record.GetRecordsParam')


class GetRecordsHeader(object):
	if_modified_since = Header('If-Modified-Since', 'com.zoho.crm.api.Record.GetRecordsHeader')


class DeleteRecordsParam(object):
	ids = Param('ids', 'com.zoho.crm.api.Record.DeleteRecordsParam')
	wf_trigger = Param('wf_trigger', 'com.zoho.crm.api.Record.DeleteRecordsParam')


class GetDeletedRecordsParam(object):
	type = Param('type', 'com.zoho.crm.api.Record.GetDeletedRecordsParam')
	page = Param('page', 'com.zoho.crm.api.Record.GetDeletedRecordsParam')
	per_page = Param('per_page', 'com.zoho.crm.api.Record.GetDeletedRecordsParam')


class GetDeletedRecordsHeader(object):
	if_modified_since = Header('If-Modified-Since', 'com.zoho.crm.api.Record.GetDeletedRecordsHeader')


class SearchRecordsParam(object):
	criteria = Param('criteria', 'com.zoho.crm.api.Record.SearchRecordsParam')
	email = Param('email', 'com.zoho.crm.api.Record.SearchRecordsParam')
	phone = Param('phone', 'com.zoho.crm.api.Record.SearchRecordsParam')
	word = Param('word', 'com.zoho.crm.api.Record.SearchRecordsParam')
	converted = Param('converted', 'com.zoho.crm.api.Record.SearchRecordsParam')
	approved = Param('approved', 'com.zoho.crm.api.Record.SearchRecordsParam')
	page = Param('page', 'com.zoho.crm.api.Record.SearchRecordsParam')
	per_page = Param('per_page', 'com.zoho.crm.api.Record.SearchRecordsParam')


class GetMassUpdateStatusParam(object):
	job_id = Param('job_id', 'com.zoho.crm.api.Record.GetMassUpdateStatusParam')
