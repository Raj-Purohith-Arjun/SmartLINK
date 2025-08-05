from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from typing import List
import cohere


class CohereChat(BaseChatModel):
    def __init__(self, cohere_api_key: str):
        super().__init__()
        self._api_key = cohere_api_key
        self._client = cohere.Client(cohere_api_key)

    def _generate(self, messages: List[HumanMessage], **kwargs) -> ChatResult:
        prompt = "\n".join([m.content for m in messages])

        response = self._client.chat(
            message=prompt,
            model="command-r-plus",  # ✅ Cohere Chat-compatible model
            temperature=0.3,
        )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=response.text)
                )
            ]
        )

    @property
    def _llm_type(self) -> str:
        return "cohere-chat"
