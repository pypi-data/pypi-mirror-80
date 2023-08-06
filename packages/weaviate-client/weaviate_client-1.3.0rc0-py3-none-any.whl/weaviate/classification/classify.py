from weaviate.exceptions import UnexpectedStatusCodeException
from weaviate.connect import REST_METHOD_GET
import sys
import validators
from .config_builder import ConfigBuilder

SOURCE_WHERE_FILTER = 0
TRAINING_SET_WHERE_FILTER = 1
TARGET_WHERE_FILTER = 2


class Classification:

    def __init__(self, connection):
        self._connection = connection

    def schedule(self):
        return ConfigBuilder(self._connection, self)

    def get(self, classification_uuid):
        """ Polls the current state of the given classification

        :param classification_uuid: identifier of the classification.
        :type classification_uuid: str
        :return: a dict containing the weaviate answer.
        :raises:
            ValueError: if not a proper uuid.
            ConnectionError: if the network connection to weaviate fails.
            UnexpectedStatusCodeException: if weaviate reports a none OK status.
        """

        if not validators.uuid(classification_uuid):
            raise ValueError("Given UUID does not have a proper form")

        try:
            response = self._connection.run_rest("/classifications/" + classification_uuid, REST_METHOD_GET)
        except ConnectionError as conn_err:
            raise type(conn_err)(str(conn_err)
                                 + ' Connection error, classification status could not be retrieved.'
                                 ).with_traceback(
                sys.exc_info()[2])
        if response.status_code == 200:
            return response.json()
        else:
            raise UnexpectedStatusCodeException("Get classification status", response)

    def is_complete(self, classification_uuid):
        """ Checks if a previously started classification job has completed.

        :param classification_uuid: identifier of the classification.
        :return: true if given classification has finished.
        """
        return self._check_status(classification_uuid, "completed")

    def is_failed(self, classification_uuid):
        """
        :param classification_uuid:
        :return: True if the classification failed
        """
        return self._check_status(classification_uuid, "failed")

    def is_running(self, classification_uuid):
        """
        :param classification_uuid:
        :return: True if the classification is currently running
        """
        return self._check_status(classification_uuid, "running")

    def _check_status(self, classification_uuid, status):
        try:
            response = self.get(classification_uuid)
        except ConnectionError:
            return False
        if response["status"] == status:
            return True
        return False
