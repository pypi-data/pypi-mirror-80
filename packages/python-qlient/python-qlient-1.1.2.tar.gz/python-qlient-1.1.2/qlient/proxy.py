import itertools
import json
import uuid
from abc import abstractmethod, ABC
from typing import Dict, Iterable, Tuple, Callable, Optional

from websockets import connect

from qlient import helpers
from qlient.builder import GraphQLBuilder
from qlient.builder import SelectedField
from qlient.logger import logger
from qlient.schema import Operation


class OperationProxy(ABC):
    """
    The operation proxy class provides callable instances where the query,
    variables and an optional operation name can be passed by.
    An instance of this class is not intended to be called directly.
    Use it's sub classes instead.
    """

    def __init__(self, client, operation: Operation):
        """
        Instantiate a new OperationProxy instance
        :param client: holds the client
        :param operation: holds the to be executed operation
        """
        self.client = client
        self.operation = operation
        self.fields: Optional[Tuple[SelectedField]] = None
        self.variables = {}
        self._query_string = ""
        self.data_has_changed = False

    def set_variables(self, variables: Optional[Dict]) -> "OperationProxy":
        """
        Set the variables for a request.

        :param variables: holds optional variables stored as a dict.
        :return: self
        """
        if variables is None:
            self.variables = {}
        else:
            self.variables = variables
        self.data_has_changed = True
        return self

    def select(self, fields: Optional[Tuple[SelectedField]]) -> "OperationProxy":
        """
        Specify a range of selected fields for example: ...select(["id", "name"])

        :param fields: holds an optional tuple, list or string with selected fields.
        :return: self
        """
        if fields is None or isinstance(fields, tuple):
            self.fields = fields
        elif isinstance(fields, list):
            self.fields = tuple(fields)
        elif isinstance(fields, str):
            self.fields = (fields,)
        else:
            raise ValueError("Unrecognised type")
        self.data_has_changed = True
        return self

    @abstractmethod
    def build_query_string(self) -> str:
        """
        Abstract method for building the query string.
        This method must be overridden for each subclass.
        """
        pass

    @property
    def query_string(self) -> str:
        """
        Property for lazy initializing the query string because if enabled
        the recursive field selection lookup is quite heavy.

        :return: the query string.
        """
        if self._query_string == "" or self.data_has_changed:
            self._query_string = self.build_query_string()
            self.data_has_changed = False
        return self._query_string

    @property
    def name(self) -> str:
        """ Shortcut for the operations name """
        return self.operation.name

    def exec(self, *args, **kwargs):
        """
        The call makes the actual request to the endpoint.
        The result depends on the settings and transport in use.

        :param args: holds additional arguments
        :param kwargs: holds additional key word arguments
        :return: the result depending on settings and transport in use.
        """
        return self.client.transporter.post(
            self.client.endpoint,
            self.query_string,
            self.variables,
            self.name,
            self.operation.settings
        )

    def __call__(self, *args, **kwargs):
        """
        Directly calling the instance will invoke the .exec(*args, **kwargs) method.
        See OperationProxy.exec(*args, **kwargs) for further information.

        :param args: holds additional arguments
        :param kwargs: holds additional key word arguments
        :return: the result depending on settings and transport in use.
        """
        return self.exec(*args, **kwargs)


class ServiceProxy:
    """
    The base service proxy class.
    An instance of this class holds a dictionary of all possible operations that are
    available for this service.
    """

    def __init__(self, services: Dict[str, OperationProxy]):
        """
        Instantiate a new instance of ServiceProxy

        :param services: holds a dictionary with all available services
        """
        self._services: Dict[str, OperationProxy] = services

    def __getattr__(self, key) -> OperationProxy:
        """
        Return the OperationProxy for the given key.

        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        return self[key]

    def __getitem__(self, key) -> OperationProxy:
        """
        Return the OperationProxy for the given key.

        :param key: holds the operation key
        :return: the according OperationProxy
        :raises: AttributeError when the no operation with that key exists.
        """
        try:
            return self._services[key]
        except KeyError:
            raise AttributeError(f"No operation found for key {key}")

    def __iter__(self):
        """ Return iterator for the services and their callables. """
        return iter(self._services.items())

    def __dir__(self) -> Iterable[str]:
        """ Return the names of the operations. """
        return list(itertools.chain(dir(super()), self._services))


class QueryOperationProxy(OperationProxy):
    """
    The operation proxy for a query.
    The call method was slightly changed for better readability which makes it easier to use as well.
    I'm open for any suggestions and improvements.
    """

    def build_query_string(self) -> str:
        if self.fields is None and not self.operation.settings.disable_selection_lookup:
            selection = self.operation.get_return_fields(self.client.schema.types)
            self.select(selection)

        query_builder = GraphQLBuilder()

        if self.variables is not None:
            variables = helpers.map_variables_to_types(self.variables, self.operation)
            query_builder = query_builder.operation("query", name=self.name, params=variables)
            query_builder = query_builder.query(self.name, params={key: f"${key}" for key in self.variables.keys()})
        else:
            query_builder = query_builder.operation("query").query(self.name)

        query_builder = query_builder.fields(self.fields)
        return query_builder.generate()

    def where(self, variables: Dict) -> "QueryOperationProxy":
        """
        Wrapper for set variables method of OperationProxy.
        """
        return self.set_variables(variables)

    def __call__(self, select: Tuple[SelectedField] = None, where: Dict = None, *args, **kwargs):
        """
        This method is used to build the query request.

        When no selection is specified and the automatic lookup has not been disabled via the settings,
        it will try to create a tuple of possible selection fields.
        If the automatic lookup fails it will fallback to None.

        Then a query builder will be instantiated and optional variables as well as the fields are being set.

        Finally the request will be made and the result returned.

        :param select: holds a selection of all fields.
        :param where: holds a dictionary with query conditions.
        :param args: holds additional arguments
        :param kwargs: holds additional key word arguments
        :return: the result from the transporter
        """
        self.select(select)
        self.set_variables(where)
        return super(QueryOperationProxy, self).__call__(*args, **kwargs)


class QueryServiceProxy(ServiceProxy):
    """ The query service proxy holds all query operations """

    def __init__(self, client):
        """
        Instantiate a new QueryServiceProxy.
        :param client: holds the client
        """
        super(QueryServiceProxy, self).__init__({
            op.name: QueryOperationProxy(client, op) for op in client.schema.queries
        })


class MutationOperationProxy(OperationProxy):
    """
    The operation proxy for a mutation.
    The call method was slightly changed for better readability which makes it easier to use as well.
    I'm open for any suggestions and improvements.
    """

    def build_query_string(self) -> str:
        if self.fields is None and not self.operation.settings.disable_selection_lookup:
            selection = self.operation.get_return_fields(self.client.schema.types)
            self.select(selection)

        query_builder = GraphQLBuilder()
        variables = helpers.map_variables_to_types(self.variables, self.operation)
        query_builder = query_builder.operation("mutation", name=self.name, params=variables)
        query_builder = query_builder.query(self.name, params={key: f"${key}" for key in self.variables.keys()})

        query_builder = query_builder.fields(self.fields)
        return query_builder.generate()

    def __call__(self, select: Tuple[SelectedField] = None, data: Dict = None, *args, **kwargs):
        """
        This method is used to build the mutation request.

        No selection is widely accepted so the automatic lookup was not implemented here.
        Please specify the fields yourself if necessary.

        Then a query builder will be instantiated and necessary variables as well as the fields are being set.

        Finally the request will be made and the result returned.

        :param select: holds a selection of all fields.
        :param data: holds a dictionary with the data to pass by
        :param args: holds additional arguments
        :param kwargs: holds additional key word arguments
        :return: the result from the transporter
        """
        if data is None:
            raise ValueError("No Data specified")

        self.select(select)
        self.set_variables(data)
        return super(MutationOperationProxy, self).__call__(*args, **kwargs)


class MutationServiceProxy(ServiceProxy):
    """ The mutation service proxy holds all mutation operations """

    def __init__(self, client):
        """
        Instantiate a new MutationServiceProxy.
        :param client: holds the client
        """
        super(MutationServiceProxy, self).__init__({
            op.name: MutationOperationProxy(client, op) for op in client.schema.mutations
        })


class SubscriptionOperationProxy(OperationProxy):
    """
    The operation proxy for a subscription.
    The call method was slightly changed for better readability which makes it easier to use as well.
    I'm open for any suggestions and improvements.
    """

    def build_query_string(self) -> str:
        if self.fields is None and not self.operation.settings.disable_selection_lookup:
            selection = self.operation.get_return_fields(self.client.schema.types)
            self.select(selection)

        subscription_builder = GraphQLBuilder()

        subscription_builder = subscription_builder.operation("subscription").query(self.name)

        subscription_builder = subscription_builder.fields(self.fields)
        return subscription_builder.generate()

    def __init__(self, client, operation):
        super(SubscriptionOperationProxy, self).__init__(client, operation)
        self.client = client

    async def __call__(self, select: Tuple[SelectedField] = None, handle: Callable = None, *args, **kwargs):
        """
        The heart piece of a subscription.

        First this method is going to take care of the field selection.
        Only if no fields were selected and it was permitted by the user, the fields will be automatically selected.

        Surely the next step is to create the subscription query message.

        Finally we establish a new connection to the websocket server and initialize the connection
        with the predefined connection_init_message.
        Then we send our request and handle the incoming messages.

        :param select: holds the field selection.
        :param handle: holds a callable that will we called with every incoming message of type "data"
        :param args: holds additional arguments
        :param kwargs: holds additional keyword arguments.
        """
        self.select(select)

        if self.client.ws_endpoint is None:
            raise ValueError("ws_endpoint is None. Please set the value manually in the client.")

        connection_init_message = json.dumps({"type": "connection_init", self.client.settings.default_payload_key: {}})
        request_body = {"query": self.query_string, "variables": None}

        request_message = json.dumps({
            "type": "start",
            "id": f"SUBSCRIPTION-{self.name}-{uuid.uuid4()}".upper(),
            "payload": request_body
        })

        async with connect(self.client.ws_endpoint, subprotocols=["graphql-ws"]) as websocket:
            await websocket.send(connection_init_message)  # first message needs to initiate the connection
            await websocket.send(request_message)  # secondly we can send the query.
            async for response_message in websocket:
                response_body = json.loads(response_message)
                response_type = response_body["type"]
                if response_type == "connection_ack":
                    logger.info("The websocket server acknowledged the connection.")
                elif response_type == "data":
                    if self.client.settings.return_full_subscription_body:
                        handle(response_body)
                    else:
                        response_payload = response_body[self.client.settings.default_payload_key]
                        handle(response_payload[self.client.settings.default_response_key][self.name])
                else:
                    logger.warning(f"Unknown response type: '{response_type}'")


class SubscriptionServiceProxy(ServiceProxy):
    """ The subscription service proxy holds all subscription operations """

    def __init__(self, client):
        """
        Instantiate a new SubscriptionServiceProxy.
        :param client: holds the client
        """
        super(SubscriptionServiceProxy, self).__init__({
            op.name: SubscriptionOperationProxy(client, op) for op in client.schema.subscriptions
        })
