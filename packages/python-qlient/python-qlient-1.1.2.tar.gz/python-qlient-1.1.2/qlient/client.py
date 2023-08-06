from qlient.proxy import MutationServiceProxy, QueryServiceProxy, SubscriptionServiceProxy
from qlient.schema import Schema
from qlient.settings import Settings
from qlient.transport import Transporter
from qlient.utils import adapt_websocket_endpoint


class Client:
    """
    The client is the core of this package.

    It is used for requests and holds important variables like endpoint, settings and the schema.
    """

    def __init__(self, endpoint: str, ws_endpoint: str = None, transporter=None, settings=None):
        """
        Instantiate a new Client.

        :param endpoint: holds the endpoint URL.
        :param ws_endpoint: holds the websocket endpoint URL.
        :param transporter: holds the transporter to use for requests.
        :param settings: holds the settings to apply.
        """
        if not endpoint:
            raise ValueError("No Endpoint specified.")
        self.endpoint = endpoint

        if not ws_endpoint:
            ws_endpoint = adapt_websocket_endpoint(endpoint)
        self.ws_endpoint = ws_endpoint

        self.transporter: Transporter = transporter or Transporter()
        self.settings: Settings = settings or Settings()

        self._query_services = None
        self._mutation_services = None
        self._subscription_services = None

        self.schema = Schema(self.endpoint, self.transporter, self.settings)

    @property
    def query(self) -> QueryServiceProxy:
        """
        Property for lazy loading the query service proxy
        :return: the clients query service proxy
        """
        if self._query_services is None:
            self._query_services = QueryServiceProxy(self)
        return self._query_services

    @property
    def mutation(self) -> MutationServiceProxy:
        """
        Property for lazy loading the mutation service proxy
        :return: the clients query mutation proxy
        """
        if self._mutation_services is None:
            self._mutation_services = MutationServiceProxy(self)
        return self._mutation_services

    @property
    def subscription(self) -> SubscriptionServiceProxy:
        """
        Property for lazy loading the subscription service proxy
        :return: the clients query subscription proxy
        """
        if self._subscription_services is None:
            self._subscription_services = SubscriptionServiceProxy(self)
        return self._subscription_services
