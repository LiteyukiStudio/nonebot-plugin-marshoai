# source: https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/azure/ai/inference/models/_models.py
from typing import Any, Literal, Mapping, Optional, overload

from azure.ai.inference._model_base import rest_discriminator, rest_field
from azure.ai.inference.models import ChatRequestMessage


class DeveloperMessage(ChatRequestMessage, discriminator="developer"):

    role: Literal["developer"] = rest_discriminator(name="role")  # type: ignore
    """The chat role associated with this message, which is always 'developer' for developer messages.
     Required."""
    content: Optional[str] = rest_field()
    """The content of the message."""

    @overload
    def __init__(
        self,
        *,
        content: Optional[str] = None,
    ): ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        :param mapping: raw JSON to initialize the model.
        :type mapping: Mapping[str, Any]
        """

    def __init__(
        self, *args: Any, **kwargs: Any
    ) -> None:  # pylint: disable=useless-super-delegation
        super().__init__(*args, role="developer", **kwargs)
