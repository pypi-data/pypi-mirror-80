
try:
    import logging
    import os
    import json
    import traceback
    import threading
    from zcrmsdk.src.com.zoho.api.authenticator.store.token_store import TokenStore
    from zcrmsdk.src.com.zoho.crm.api.exception.sdk_exception import SDKException
    from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
    from zcrmsdk.src.com.zoho.crm.api.dc.data_center import DataCenter
    from zcrmsdk.src.com.zoho.crm.api.util.constants import Constants
    from zcrmsdk.src.com.zoho.api.authenticator.token import Token
    from zcrmsdk.src.com.zoho.crm.api.logger import Logger, SDKLogger

except Exception:
    import logging
    import os
    import json
    import traceback
    import threading
    from ...api.authenticator.store.token_store import TokenStore
    from ..api.exception import SDKException
    from ..api.user_signature import UserSignature
    from ..api.dc.data_center import DataCenter
    from ..api.util.constants import Constants
    from ...api.authenticator.token import Token
    from ...api.logger import Logger, SDKLogger


class Initializer(object):

    """
    The class to initialize Zoho CRM SDK.
    """

    json_details = None
    environment = None
    user = None
    store = None
    token = None
    auto_refresh_fields = None
    resource_path = None
    initializer = None
    LOCAL = threading.local()
    LOCAL.init = None

    @staticmethod
    def initialize(user, environment, token, store, logger, auto_refresh_fields, resource_path):

        """
        The method to initialize the SDK.

        Parameters:
            user (UserSignature) : A UserSignature class instance represents the CRM user
            environment (DataCenter.Environment) : An Environment class instance containing the CRM API base URL and Accounts URL.
            token (Token) : A Token class instance containing the OAuth client application information.
            store (TokenStore) : A TokenStore class instance containing the token store information.
            logger (Logger): A Logger class instance containing the log file path and Logger type.
            auto_refresh_fields (bool) : A Boolean value to allow or prevent auto-refreshing of the modules' fields in the background.
            resource_path (str) : A String containing the absolute directory path to store user specific JSON files containing module fields information.
        """

        try:
            if not isinstance(user, UserSignature):
                error = {Constants.FIELD: Constants.USER, Constants.EXPECTED_TYPE: UserSignature.__module__}

                raise SDKException(Constants.INITIALIZATION_ERROR, Constants.INITIALIZATION_EXCEPTION, details=error)

            if not isinstance(environment, DataCenter.Environment):
                error = {Constants.FIELD: Constants.ENVIRONMENT,
                         Constants.EXPECTED_TYPE: DataCenter.Environment.__module__}

                raise SDKException(Constants.INITIALIZATION_ERROR, Constants.INITIALIZATION_EXCEPTION, details=error)

            if not isinstance(store, TokenStore):
                error = {Constants.FIELD: Constants.STORE, Constants.EXPECTED_TYPE: TokenStore.__module__}

                raise SDKException(Constants.INITIALIZATION_ERROR, Constants.INITIALIZATION_EXCEPTION, details=error)

            if not isinstance(token, Token):
                error = {Constants.FIELD: Constants.TOKEN, Constants.EXPECTED_TYPE: Token.__module__}

                raise SDKException(Constants.INITIALIZATION_ERROR, Constants.INITIALIZATION_EXCEPTION, details=error)

            if auto_refresh_fields is None:
                raise SDKException(Constants.INITIALIZATION_ERROR, Constants.AUTO_REFRESH_FIELDS_ERROR_MESSAGE)

            if resource_path is None or len(resource_path) == 0:
                raise SDKException(Constants.INITIALIZATION_ERROR, Constants.RESOURCE_PATH_ERROR_MESSAGE)

            if logger is not None:
                SDKLogger.initialize(logger.level, logger.file_path)

            else:
                SDKLogger.initialize(Logger.Levels.INFO, os.path.join(os.getcwd(), Constants.LOGFILE_NAME))

            initializer = Initializer()

            initializer.environment = environment
            initializer.user = user
            initializer.token = token
            initializer.store = store
            initializer.auto_refresh_fields = auto_refresh_fields
            initializer.resource_path = resource_path

            Initializer.initializer = initializer

            logging.getLogger('SDKLogger').info(Constants.INITIALIZATION_SUCCESSFUL + initializer.__str__())

        except SDKException as e:
            raise e

        dir_name = os.path.dirname(__file__)
        filename = os.path.join(dir_name, '..', '..', '..', '..', Constants.JSON_DETAILS_FILE_PATH)

        with open(filename, mode='r') as JSON:
            Initializer.json_details = json.load(JSON)

    def __str__(self):
        return Constants.FOR_EMAIL_ID + Initializer.get_initializer().user.email + Constants.IN_ENVIRONMENT + Initializer.get_initializer().environment.url + '.'

    @staticmethod
    def get_initializer():

        """
        The method to get Initializer class instance.

        Returns:
            Initializer : An instance of Initializer
        """

        if getattr(Initializer.LOCAL, 'init', None) is not None:
            return getattr(Initializer.LOCAL, 'init')

        return Initializer.initializer

    @staticmethod
    def get_json(file_path):
        with open(file_path, mode="r") as JSON:
            file_contents = json.load(JSON)
            JSON.close()

        return file_contents

    @staticmethod
    def switch_user(user, environment, token, auto_refresh_fields):

        """
        The method to switch the different user in SDK environment.

        Parameters:
            user (UserSignature) : A UserSignature class instance represents the CRM user
            environment (DataCenter.Environment) : An Environment class instance containing the CRM API base URL and Accounts URL.
            token (Token) : A Token class instance containing the OAuth client application information.
            auto_refresh_fields (bool) : A Boolean value to allow or prevent auto-refreshing of the modules' fields in the background.
        """

        initializer = Initializer()

        initializer.user = user
        initializer.environment = environment
        initializer.token = token
        initializer.auto_refresh_fields = auto_refresh_fields
        initializer.store = Initializer.initializer.store
        initializer.resource_path = Initializer.initializer.resource_path

        Initializer.LOCAL.init = initializer

        logging.getLogger('SDKLogger').info(Constants.INITIALIZATION_SWITCHED + initializer.__str__())
