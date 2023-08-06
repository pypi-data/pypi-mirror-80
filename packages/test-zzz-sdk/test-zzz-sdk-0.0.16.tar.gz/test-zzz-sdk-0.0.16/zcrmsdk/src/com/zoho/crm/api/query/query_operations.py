try:
	from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.util import APIResponse, CommonAPIHandler, Constants
except Exception:
	from ..exception import SDKException
	from ..util import APIResponse, CommonAPIHandler, Constants


class QueryOperations(object):
	def __init__(self):
		"""Creates an instance of QueryOperations"""
		pass

	def get_records(self, request):
		"""
		The method to get records

		Parameters:
			request (BodyWrapper) : An instance of BodyWrapper

		Returns:
			APIResponse: An instance of APIResponse

		Raises:
			SDKException
		"""

		try:
			from zcrmsdk.src.com.zoho.crm.api.query.body_wrapper import BodyWrapper
		except Exception:
			from .body_wrapper import BodyWrapper

		if request is not None and not isinstance(request, BodyWrapper):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: request EXPECTED TYPE: BodyWrapper', None, None)
		
		handler_instance = CommonAPIHandler()
		api_path = ''
		api_path = api_path + '/crm/v2/coql'
		handler_instance.api_path = api_path
		handler_instance.http_method = Constants.REQUEST_METHOD_POST
		handler_instance.category_method = Constants.REQUEST_CATEGORY_CREATE
		handler_instance.content_type = 'application/json'
		handler_instance.request = request
		handler_instance.mandatory_checker = True
		try:
			from zcrmsdk.src.com.zoho.crm.api.query.response_handler import ResponseHandler
		except Exception:
			from .response_handler import ResponseHandler
		return handler_instance.api_call(ResponseHandler.__module__, 'application/json')
