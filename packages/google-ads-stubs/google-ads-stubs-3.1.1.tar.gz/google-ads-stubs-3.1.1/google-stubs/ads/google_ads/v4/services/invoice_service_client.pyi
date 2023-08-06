from google.ads.google_ads.v4.proto.services import invoice_service_pb2 as invoice_service_pb2
from google.ads.google_ads.v4.services import invoice_service_client_config as invoice_service_client_config
from google.ads.google_ads.v4.services.transports import invoice_service_grpc_transport as invoice_service_grpc_transport
from google.oauth2 import service_account as service_account
import grpc  # type: ignore
from google.ads.google_ads.v4.services.transports.invoice_service_grpc_transport import InvoiceServiceGrpcTransport
from google.auth.credentials import Credentials  # type: ignore
from google.api_core.gapic_v1.client_info import ClientInfo  # type: ignore
from google.api_core.retry import Retry  # type: ignore
from typing import Optional, Dict, Any, List, Sequence, Tuple, Union, Callable, ClassVar

class InvoiceServiceClient:
    SERVICE_ADDRESS: ClassVar[str] = ...
    @classmethod
    def from_service_account_file(cls, filename: str, *args: Any, **kwargs: Any) -> InvoiceServiceClient: ...
    @classmethod
    def from_service_account_json(cls, filename: str, *args: Any, **kwargs: Any) -> InvoiceServiceClient: ...
    transport: Union[InvoiceServiceGrpcTransport, Callable[[Credentials, type], InvoiceServiceGrpcTransport]] = ...
    def __init__(self, transport: Optional[Union[InvoiceServiceGrpcTransport, Callable[[Credentials, type], InvoiceServiceGrpcTransport]]] = ..., channel: Optional[grpc.Channel] = ..., credentials: Optional[Credentials] = ..., client_config: Optional[Dict[str, Any]] = ..., client_info: Optional[ClientInfo] = ...) -> None: ...
    def list_invoices(self, customer_id: Any, billing_setup: Any, issue_year: Any, issue_month: Any, retry: Any = ..., timeout: Any = ..., metadata: Optional[Any] = ...): ...
