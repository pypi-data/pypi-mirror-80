import sys
import validators

from weaviate.connect import *
from weaviate.exceptions import *
from weaviate.util import _get_dict_from_object, is_semantic_type
from requests.exceptions import ConnectionError
from weaviate.data.references import Reference
from weaviate import SEMANTIC_TYPE_THINGS


class DataObject:

    def __init__(self, connection):
        self._connection = connection
        self.reference = Reference(self._connection)

    def create(self, data_object, class_name, uuid=None, semantic_type=SEMANTIC_TYPE_THINGS, vector_weights=None):
        """ Takes a dict describing the thing and adds it to weaviate

        :param data_object: Object to be added.
        :type data_object: dict
        :param class_name: Associated with the object given.
        :type class_name: str
        :param uuid: Object will be created under this uuid if it is provided.
                     Otherwise weaviate will generate a uuid for this object.
        :type uuid: str
        :param semantic_type: Either things or actions.
                              Defaults to things.
                              Settable through the constants SEMANTIC_TYPE_THINGS and SEMANTIC_TYPE_ACTIONS
        :type semantic_type: str
        :param vector_weights: Influence the weight of words on thing creation.
                               Default is None for no influence.
        :type vector_weights: dict
        :return: Returns the UUID of the created thing if successful.
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            ThingAlreadyExistsException: if an thing with the given uuid already exists within weaviate.
            UnexpectedStatusCodeException: if creating the thing in weavate failed with a different reason,
            more information is given in the exception.
            ConnectionError: if the network connection to weaviate fails.
        :rtype: str
        """
        if not is_semantic_type(semantic_type):
            raise ValueError(f"{semantic_type} is not a valid semantic type")

        loaded_data_object = _get_dict_from_object(data_object)
        if not isinstance(class_name, str):
            raise TypeError("Expected class_name of type str but was: " + str(type(class_name)))

        weaviate_obj = {
            "class": class_name,
            "schema": loaded_data_object
        }
        if uuid is not None:
            if not isinstance(uuid, str):
                raise TypeError("Expected uuid to be of type str but was: " + str(type(uuid)))
            if not validators.uuid(uuid):
                raise ValueError("Given uuid does not have a valid form")

            weaviate_obj["id"] = uuid

        if vector_weights is not None:
            if not isinstance(vector_weights, dict):
                raise TypeError("Expected vector_weights to be of type dict but was " + str(type(vector_weights)))

            weaviate_obj["vectorWeights"] = vector_weights

        path = "/" + semantic_type
        try:
            response = self._connection.run_rest(path, REST_METHOD_POST, weaviate_obj)
        except ConnectionError as conn_err:
            raise type(conn_err)(
                str(conn_err) + ' Connection error, object was not added to weaviate.').with_traceback(
                sys.exc_info()[2])

        if response.status_code == 200:
            return str(response.json()["id"])

        else:
            thing_does_already_exist = False
            try:
                if 'already exists' in response.json()['error'][0]['message']:
                    thing_does_already_exist = True
            except KeyError:
                pass
            except Exception as e:
                raise type(e)(str(e)
                              + ' Unexpected exception please report this excetpion in an issue.').with_traceback(
                    sys.exc_info()[2])

            if thing_does_already_exist:
                raise ThingAlreadyExistsException(str(uuid))

            raise UnexpectedStatusCodeException("Creating thing", response)

    def merge(self, data_object, class_name, uuid, semantic_type=SEMANTIC_TYPE_THINGS):
        """ Merges the given thing with the already existing thing in weaviate.
        Overwrites all given fields.

        :param data_object: The object states the fields that should be updated.
                            Fields not stated by object will not be changed.
                            Fields that are None will not be changed.
        :type data_object: dict, url, file
        :param class_name: The name of the class of the data object.
        :type class_name: str
        :param uuid: The ID of the object that should be changed.
        :type uuid: str
        :param semantic_type: Either things or actions.
                              Defaults to things.
                              Settable through the constants SEMANTIC_TYPE_THINGS and SEMANTIC_TYPE_ACTIONS
        :type semantic_type: str
        :return: None if successful
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            ConnectionError: If the network connection to weaviate fails.
            UnexpectedStatusCodeException: If weaviate reports a none successful status.
        """
        if not is_semantic_type(semantic_type):
            raise ValueError(f"{semantic_type} is not a valid semantic type")

        object_dict = _get_dict_from_object(data_object)

        if not isinstance(class_name, str):
            raise TypeError("Class must be type str")
        if not isinstance(uuid, str):
            raise TypeError("UUID must be type str")
        if not validators.uuid(uuid):
            raise ValueError("Not a proper UUID")

        payload = {
            "id": uuid,
            "class": class_name,
            "schema": object_dict
        }

        path = f"/{semantic_type}/{uuid}"

        try:
            response = self._connection.run_rest(path, REST_METHOD_PATCH, payload)
        except ConnectionError as conn_err:
            raise type(conn_err)(str(conn_err) + ' Connection error, object was not patched.').with_traceback(
                sys.exc_info()[2])

        if response.status_code == 204:
            return None  # success
        else:
            raise UnexpectedStatusCodeException("PATCH merge of object not successful", response)

    def update(self, data_object, class_name, uuid, semantic_type=SEMANTIC_TYPE_THINGS):
        """ Updates an already existing object with the given data object. Does not keep unset values.

        :param data_object: Describes the new values.
                       It may be an URL or path to a json or a python dict describing the new values.
        :type data_object: str, dict
        :param class_name: Name of the class of the thing that should be updated.
        :type class_name: str
        :param uuid: Of the object.
        :type uuid: str
        :param semantic_type: Either things or actions.
                              Defaults to things.
                              Settable through the constants SEMANTIC_TYPE_THINGS and SEMANTIC_TYPE_ACTIONS
        :type semantic_type: str
        :return: None if successful.
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            ConnectionError: If the network connection to weaviate fails.
            UnexpectedStatusCodeException: If weaviate reports a none OK status.
        """
        if not is_semantic_type(semantic_type):
            raise ValueError(f"{semantic_type} is not a valid semantic type")

        parsed_object = _get_dict_from_object(data_object)

        weaviate_obj = {
            "id": uuid,
            "class": class_name,
            "schema": parsed_object
        }

        try:
            response = self._connection.run_rest("/" + semantic_type + "/" + uuid, REST_METHOD_PUT, weaviate_obj)
        except ConnectionError as conn_err:
            raise type(conn_err)(str(conn_err) + ' Connection error, thing was not updated.').with_traceback(
                sys.exc_info()[2])

        if response.status_code == 200:
            return

        else:
            raise UnexpectedStatusCodeException("Update thing", response)

    def get_by_id(self, uuid, underscore_properties=None, semantic_type=SEMANTIC_TYPE_THINGS):
        """ Gets an object as dict.

        :param uuid: the identifier of the thing that should be retrieved.
        :type uuid: str
        :param underscore_properties: list of underscore properties that should be included in the request.
                                      Underscore properties allow
        :type underscore_properties: list of str
        :param semantic_type: defaults to things allows also actions see SEMANTIC_TYPE_ACTIONS.
        :type semantic_type: str
        :return:
            dict in case the thing exists.
            None in case the thing does not exist.
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            ConnectionError: if the network connection to weaviate fails.
            UnexpectedStatusCodeException: if weaviate reports a none OK status.
        """

        try:
            response = self._get_object_response(semantic_type, uuid, underscore_properties)
        except ConnectionError:
            raise

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            raise UnexpectedStatusCodeException("Get object", response)

    def get(self, underscore_properties=None, semantic_type=SEMANTIC_TYPE_THINGS):
        """ Gets all objects of a semantic type

        :param semantic_type: defaults to things allows also actions see SEMANTIC_TYPE_ACTIONS.
        :type semantic_type: str
        :param underscore_properties: list of underscore properties that should be included in the request.
                                      Underscore properties allow
        :type underscore_properties: list of str
        :return: A list of all objects if no objects where found the list is empty.
        :rtype: list of dict
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            ConnectionError: if the network connection to weaviate fails.
            UnexpectedStatusCodeException: if weaviate reports a none OK status.
        """
        if not is_semantic_type(semantic_type):
            raise ValueError(f"{semantic_type} is not a valid semantic type")

        params = _get_params(underscore_properties)

        try:
            response = self._connection.run_rest("/" + semantic_type, REST_METHOD_GET, params=params)
        except ConnectionError as conn_err:
            raise type(conn_err)(str(conn_err) + ' Connection error when getting things').with_traceback(
                sys.exc_info()[2])

        if response.status_code == 200:
            response_data = response.json()
            return response_data[semantic_type]
        else:
            raise UnexpectedStatusCodeException("Get object", response)

    def _get_object_response(self, semantic_type, object_uuid, underscore_properties=None):
        """ Retrieves an object from weaviate.

        :param semantic_type: can be found as constants e.g. SEMANTIC_TYPE_THINGS.
        :type semantic_type: str
        :param object_uuid: the identifier of the object that should be retrieved.
        :type object_uuid: str
        :param underscore_properties: Defines the underscore properties that should be included in the result
        :type underscore_properties: list of str or None
        :return: response object.
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            ConnectionError: if the network connection to weaviate fails.
        """
        if not is_semantic_type(semantic_type):
            raise ValueError(f"{semantic_type} is not a valid semantic type")

        params = _get_params(underscore_properties)

        if not isinstance(object_uuid, str):
            object_uuid = str(object_uuid)
        try:
            response = self._connection.run_rest("/" + semantic_type + "/" + object_uuid, REST_METHOD_GET, params=params)
        except ConnectionError as conn_err:
            raise type(conn_err)(str(conn_err) + ' Connection error not sure if object exists').with_traceback(
                sys.exc_info()[2])
        else:
            return response

    def delete(self, uuid, semantic_type=SEMANTIC_TYPE_THINGS):
        """

        :param uuid: ID of the thing that should be removed from the graph.
        :type uuid: str
        :param semantic_type: defaults to things allows also actions see SEMANTIC_TYPE_ACTIONS.
        :type semantic_type: str
        :return: None if successful
        :raises:
            ConnectionError: if the network connection to weaviate fails.
            UnexpectedStatusCodeException: if weaviate reports a none OK status.
            TypeError: If parameter has the wrong type.
            ValueError: If uuid is not properly formed.
        """
        if not isinstance(uuid, str):
            raise TypeError("UUID must be type str")
        if not validators.uuid(uuid):
            raise ValueError("UUID does not have proper form")

        try:
            response = self._connection.run_rest("/" + semantic_type + "/" + uuid, REST_METHOD_DELETE)
        except ConnectionError as conn_err:
            raise type(conn_err)(str(conn_err)
                                 + ' Connection error, object could not be deleted.'
                                 ).with_traceback(
                sys.exc_info()[2])

        if response.status_code == 204:
            return  # Successfully deleted
        else:
            raise UnexpectedStatusCodeException("Delete object", response)

    def exists(self, uuid, semantic_type=SEMANTIC_TYPE_THINGS):
        """

        :param uuid: the uuid of the thing that may or may not exist within weaviate.
        :type uuid: str
        :param semantic_type: Either things or actions.
                              Defaults to things.
                              Settable through the constants SEMANTIC_TYPE_THINGS and SEMANTIC_TYPE_ACTIONS
        :type semantic_type: str
        :return: true if thing exists.
        :raises:
            ConnectionError: if the network connection to weaviate fails.
            UnexpectedStatusCodeException: if weaviate reports a none OK status.
        """
        try:
            response = self._get_object_response(semantic_type, uuid)
        except ConnectionError:
            raise  # Just pass the same error back

        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            raise UnexpectedStatusCodeException("Thing exists", response)

    def validate(self, data_object, class_name, uuid, semantic_type=SEMANTIC_TYPE_THINGS):
        """ Takes a dict describing the thing and validates it against weaviate

        :param data_object: Object to be validated.
        :type data_object: dict or str
        :param class_name: Associated with the object given.
        :type class_name: str
        :param uuid: uuid of object
        :type uuid: str
        :param semantic_type: Either things or actions.
                              Defaults to things.
                              Settable through the constants SEMANTIC_TYPE_THINGS and SEMANTIC_TYPE_ACTIONS
        :type semantic_type: str
        :return: dict of form:
        {
            valid: bool
            error: None or list
        }
        :rtype: dict
        :raises:
            TypeError: if argument is of wrong type.
            ValueError: if argument contains an invalid value.
            UnexpectedStatusCodeException: if validating the thing in weavate failed with a different reason,
            more information is given in the exception.
            ConnectionError: if the network connection to weaviate fails.
        :rtype: str
        """
        if not is_semantic_type(semantic_type):
            raise ValueError(f"{semantic_type} is not a valid semantic type")

        if not isinstance(uuid, str):
            raise TypeError("UUID must be of type str")

        loaded_data_object = _get_dict_from_object(data_object)
        if not isinstance(class_name, str):
            raise TypeError("Expected class_name of type str but was: " + str(type(class_name)))

        weaviate_obj = {
            "id": uuid,
            "class": class_name,
            "schema": loaded_data_object
        }

        path = f"/{semantic_type}/validate"
        try:
            response = self._connection.run_rest(path, REST_METHOD_POST, weaviate_obj)
        except ConnectionError as conn_err:
            raise type(conn_err)(
                str(conn_err) + ' Connection error, object was not validated against weaviate.').with_traceback(
                sys.exc_info()[2])

        result = {
            "error": None
        }

        if response.status_code == 200:
            result["valid"] = True
            return result
        elif response.status_code == 422:
            result["valid"] = False
            result["error"] = response.json()["error"]
            return result
        else:
            raise UnexpectedStatusCodeException("Validate thing", response)


def _get_params(underscore_properties):
    """

    :param underscore_properties: list of underscore properties or None
    :type underscore_properties: list of str, None
    :return: dict for params
    """
    params = {}
    if underscore_properties is not None:
        if not isinstance(underscore_properties, list):
            raise TypeError(f"Underscore properties must be of type list but are {type(underscore_properties)}")

        params['include'] = ",".join(underscore_properties)

    return params