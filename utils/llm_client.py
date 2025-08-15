from langchain_aws import ChatBedrock, ChatBedrockConverse
from abc import abstractmethod

import settings
from botocore.config import Config

from utils.singleton import Singleton 

config = Config(read_timeout=1000, max_pool_connections=50)

class ChatClientFactory(metaclass=Singleton):
    @abstractmethod
    def create_client(self):
        pass


class Claude3_7SonnetFactory(ChatClientFactory):
    _client = None
    _thinking_client = None

    def create_client(self, thinking=False, max_output_tokens=8192):
        if not thinking:
            if self._client is None:
                self._client = ChatBedrock(
                    model_id=settings.CLAUDE_3_7_SONNET_MODEL_ID,
                    region_name=settings.AWS_REGION,
                    config=config,
                    model_kwargs=dict(
                        max_tokens=max_output_tokens,
                    ),
                )
            return self._client