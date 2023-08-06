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


class TagsOperations(object):
	def __init__(self):
		"""Creates an instance of TagsOperations"""
		pass

	def get_tags(self, param_instance):
		"""
		The method to get tags

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
		api_path = api_path + '/crm/v2/settings/tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')

	def create_tags(self, request, param_instance):
		"""
		The method to create tags

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.param = param_instance
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def update_tags(self, request, param_instance):
		"""
		The method to update tags

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			param_instance (ParameterMap) : An instance of ParameterMap

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.param = param_instance
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def update_tag(self, request, param_instance, id):
		"""
		The method to update tag

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper
			param_instance (ParameterMap) : An instance of ParameterMap
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/tags/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_PUT
		handler_instance.category_method = Constants.REQUEST_CATEGORY_UPDATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def delete_tag(self, id):
		"""
		The method to delete tag

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
		api_path = api_path + '/crm/v2/settings/tags/'
		api_path = api_path + str(id)
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_DELETE
		handler_instance.category_method = Constants.REQUEST_METHOD_DELETE
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def merge_tags(self, request, id):
		"""
		The method to merge tags

		Parameters:
			request (MergeWrapper) : An instance of MergeWrapper
			id (int) : An int representing the id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.merge_wrapper import MergeWrapper
		except Exception:
			from .merge_wrapper import MergeWrapper

		if request is not None and not isinstance(request, MergeWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: MergeWrapper', None, None)
		
		if id is not None and not isinstance(id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/settings/tags/'
		api_path = api_path + str(id)
		api_path = api_path + '/actions/merge'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.action_handler import ActionHandler
		except Exception:
			from .action_handler import ActionHandler
		return handler_instance.api_call(ActionHandler.__module__, 'application/json')

	def add_tags_to_record(self, param_instance, module_api_name, record_id):
		"""
		The method to add tags to record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string representing the module_api_name
			record_id (int) : An int representing the record_id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if record_id is not None and not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/actions/add_tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.param = param_instance
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.record_action_handler import RecordActionHandler
		except Exception:
			from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, 'application/json')

	def remove_tags_from_record(self, param_instance, module_api_name, record_id):
		"""
		The method to remove tags from record

		Parameters:
			param_instance (ParameterMap) : An instance of ParameterMap
			module_api_name (string) : A string representing the module_api_name
			record_id (int) : An int representing the record_id

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		if param_instance is not None and not isinstance(param_instance, ParameterMap):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: param_instance EXPECTED TYPE: ParameterMap', None, None)
		
		if module_api_name is not None and not isinstance(module_api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: module_api_name EXPECTED TYPE: str', None, None)
		
		if record_id is not None and not isinstance(record_id, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: record_id EXPECTED TYPE: int', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/'
		api_path = api_path + str(module_api_name)
		api_path = api_path + '/'
		api_path = api_path + str(record_id)
		api_path = api_path + '/actions/remove_tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.param = param_instance
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.record_action_handler import RecordActionHandler
		except Exception:
			from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, 'application/json')

	def add_tags_to_multiple_records(self, param_instance, module_api_name):
		"""
		The method to add tags to multiple records

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
		api_path = api_path + '/actions/add_tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.param = param_instance
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.record_action_handler import RecordActionHandler
		except Exception:
			from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, 'application/json')

	def remove_tags_from_multiple_records(self, param_instance, module_api_name):
		"""
		The method to remove tags from multiple records

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
		api_path = api_path + '/actions/remove_tags'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.param = param_instance
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.record_action_handler import RecordActionHandler
		except Exception:
			from .record_action_handler import RecordActionHandler
		return handler_instance.api_call(RecordActionHandler.__module__, 'application/json')

	def get_record_count_for_tag(self, param_instance, id):
		"""
		The method to get record count for tag

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
		api_path = api_path + '/crm/v2/settings/tags/'
		api_path = api_path + str(id)
		api_path = api_path + '/actions/records_count'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_GET
		handler_instance.category_method = Constants.REQUEST_CATEGORY_READ
		handler_instance.param = param_instance
		try:
			from zcrmsdk.src.com.zoho.crm.api.tags.count_handler import CountHandler
		except Exception:
			from .count_handler import CountHandler
		return handler_instance.api_call(CountHandler.__module__, 'application/json')


class GetTagsParam(object):
	module = Param('module', 'com.zoho.crm.api.Tags.GetTagsParam')
	my_tags = Param('my_tags', 'com.zoho.crm.api.Tags.GetTagsParam')


class CreateTagsParam(object):
	module = Param('module', 'com.zoho.crm.api.Tags.CreateTagsParam')


class UpdateTagsParam(object):
	module = Param('module', 'com.zoho.crm.api.Tags.UpdateTagsParam')


class UpdateTagParam(object):
	module = Param('module', 'com.zoho.crm.api.Tags.UpdateTagParam')


class AddTagsToRecordParam(object):
	tag_names = Param('tag_names', 'com.zoho.crm.api.Tags.AddTagsToRecordParam')
	over_write = Param('over_write', 'com.zoho.crm.api.Tags.AddTagsToRecordParam')


class RemoveTagsFromRecordParam(object):
	tag_names = Param('tag_names', 'com.zoho.crm.api.Tags.RemoveTagsFromRecordParam')


class AddTagsToMultipleRecordsParam(object):
	tag_names = Param('tag_names', 'com.zoho.crm.api.Tags.AddTagsToMultipleRecordsParam')
	ids = Param('ids', 'com.zoho.crm.api.Tags.AddTagsToMultipleRecordsParam')
	over_write = Param('over_write', 'com.zoho.crm.api.Tags.AddTagsToMultipleRecordsParam')


class RemoveTagsFromMultipleRecordsParam(object):
	tag_names = Param('tag_names', 'com.zoho.crm.api.Tags.RemoveTagsFromMultipleRecordsParam')
	ids = Param('ids', 'com.zoho.crm.api.Tags.RemoveTagsFromMultipleRecordsParam')


class GetRecordCountForTagParam(object):
	module = Param('module', 'com.zoho.crm.api.Tags.GetRecordCountForTagParam')
