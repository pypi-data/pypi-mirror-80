try:
    import os
    import json
    import logging
    import shutil
    from zcrmsdk.src.com.zoho.crm.api.util import Constants, Converter, Utility
    from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
    from zcrmsdk.src.com.zoho.crm.api.exception import SDKException

except Exception:
    import os
    import json
    import logging
    import shutil
    from .constants import Constants
    from .converter import Converter
    from .utility import Utility
    from ..initializer import Initializer
    from ..exception import SDKException


class ModuleFieldsHandler(object):
    logger = logging.getLogger('SDKLogger')

    @staticmethod
    def get_directory():

        """
        The method to obtain resources directory path.

        Returns:
            str: A String representing the directory's absolute path.
        """
        return os.path.join(Initializer.get_initializer().resource_path, Constants.FIELD_DETAILS_DIRECTORY)

    @staticmethod
    def delete_fields_file():
        """
        The method to delete fields JSON File of the current user.

        Raises:
            SDKException
        """

        try:
            record_field_details_path = os.path.join(ModuleFieldsHandler.get_directory(), Converter.get_encoded_file_name())
            if os.path.exists(record_field_details_path):
                os.remove(record_field_details_path)
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            ModuleFieldsHandler.logger.info(Constants.DELETE_FIELD_FILE_ERROR + sdk_exception.__str__())
            raise sdk_exception

    @staticmethod
    def delete_all_field_files():
        """
        The method to delete all the field JSON files under resources directory.

        Raises:
            SDKException
        """

        try:
            record_field_details_directory = ModuleFieldsHandler.get_directory()
            if os.path.exists(record_field_details_directory):
                shutil.rmtree(record_field_details_directory)
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            ModuleFieldsHandler.logger.info(Constants.DELETE_FIELD_FILES_ERROR + sdk_exception.__str__())
            raise sdk_exception

    @staticmethod
    def __delete_fields(module):
        """
        The method to delete fields of the given module from the current user's fields JSON file.

        Parameters:
            module(str): A string representing the module.

        Raises:
            SDKException
        """

        try:
            record_field_details_path = os.path.join(ModuleFieldsHandler.get_directory(), Converter.get_encoded_file_name())
            if os.path.exists(record_field_details_path):
                subform_modules = []
                record_field_details_json = Initializer.get_json(record_field_details_path)

                if module.lower() in record_field_details_json:
                    fields_json = record_field_details_json[module.lower()]
                    for key, value in fields_json.items():
                        if Constants.SUBFORM in value and value[Constants.SUBFORM]:
                            subform_modules.append(value[Constants.MODULE])

                    del record_field_details_json[module.lower()]

                    with open(record_field_details_path, mode="w") as file:
                        json.dump(record_field_details_json, file)
                        file.flush()
                        file.close()

                    if len(subform_modules) > 0:
                        for subform_module in subform_modules:
                            ModuleFieldsHandler.__delete_fields(subform_module)
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            raise sdk_exception

    @staticmethod
    def refresh_fields(module):
        """
        The method to force-refresh fields of a module.

        Parameters:
            module(str): A string representing the module.

        Raises:
            SDKException
        """

        try:
            ModuleFieldsHandler.__delete_fields(module)
            Utility.get_fields(module)
        except SDKException as ex:
            ModuleFieldsHandler.logger.info(Constants.REFRESH_SINGLE_MODULE_FIELDS_ERROR + module + ex.__str__())
            raise ex
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            ModuleFieldsHandler.logger.info(Constants.REFRESH_SINGLE_MODULE_FIELDS_ERROR + module + sdk_exception.__str__())
            raise sdk_exception

    @staticmethod
    def refresh_all_modules():
        """
        The method to force-refresh fields of all the available modules.

        Raises:
            SDKException
        """

        try:
            Utility.refresh_modules()
        except SDKException as ex:
            ModuleFieldsHandler.logger.info(Constants.REFRESH_ALL_MODULE_FIELDS_ERROR + ex.__str__())
            raise ex
        except Exception as e:
            sdk_exception = SDKException(cause=e)
            ModuleFieldsHandler.logger.info(Constants.REFRESH_ALL_MODULE_FIELDS_ERROR + sdk_exception.__str__())
            raise sdk_exception


