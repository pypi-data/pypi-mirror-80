from google.ads.google_ads.v4.proto.services import keyword_plan_idea_service_pb2 as keyword_plan_idea_service_pb2
from google.ads.google_ads.v4.services import keyword_plan_idea_service_client_config as keyword_plan_idea_service_client_config
from google.ads.google_ads.v4.services.transports import keyword_plan_idea_service_grpc_transport as keyword_plan_idea_service_grpc_transport
from google.oauth2 import service_account as service_account
import grpc  # type: ignore
from google.ads.google_ads.v4.services.transports.keyword_plan_idea_service_grpc_transport import KeywordPlanIdeaServiceGrpcTransport
from google.auth.credentials import Credentials  # type: ignore
from google.api_core.gapic_v1.client_info import ClientInfo  # type: ignore
from google.api_core.retry import Retry  # type: ignore
from typing import Optional, Dict, Any, List, Sequence, Tuple, Union, Callable, ClassVar

class KeywordPlanIdeaServiceClient:
    SERVICE_ADDRESS: ClassVar[str] = ...
    @classmethod
    def from_service_account_file(cls, filename: str, *args: Any, **kwargs: Any) -> KeywordPlanIdeaServiceClient: ...
    @classmethod
    def from_service_account_json(cls, filename: str, *args: Any, **kwargs: Any) -> KeywordPlanIdeaServiceClient: ...
    transport: Union[KeywordPlanIdeaServiceGrpcTransport, Callable[[Credentials, type], KeywordPlanIdeaServiceGrpcTransport]] = ...
    def __init__(self, transport: Optional[Union[KeywordPlanIdeaServiceGrpcTransport, Callable[[Credentials, type], KeywordPlanIdeaServiceGrpcTransport]]] = ..., channel: Optional[grpc.Channel] = ..., credentials: Optional[Credentials] = ..., client_config: Optional[Dict[str, Any]] = ..., client_info: Optional[ClientInfo] = ...) -> None: ...
    def generate_keyword_ideas(self, customer_id: Any, language: Any, geo_target_constants: Any, include_adult_keywords: Any, keyword_plan_network: Any, page_size: Optional[Any] = ..., keyword_and_url_seed: Optional[Any] = ..., keyword_seed: Optional[Any] = ..., url_seed: Optional[Any] = ..., site_seed: Optional[Any] = ..., retry: Any = ..., timeout: Any = ..., metadata: Optional[Any] = ...): ...
