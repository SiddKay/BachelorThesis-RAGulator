from pathlib import Path
import importlib.util
import inspect
from typing import Any, List, Optional, Union
from dataclasses import dataclass
import logging
from langchain.chains import LLMChain
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    BasePromptTemplate,
)
from langchain_core.runnables import (
    RunnableSequence,
    ConfigurableField,
    RunnablePassthrough,
)


@dataclass
class ModelParameter:
    name: str
    type: str
    default: Any
    required: bool = False


@dataclass
class PromptInfo:
    template: str
    input_variables: List[str]
    template_type: str  # 'prompt' or 'chat'
    template_format: str  # 'f-string' or 'jinja2'


@dataclass
class ChainConfig:
    chain_name: str
    model_parameters: List[ModelParameter]
    prompt_info: Optional[PromptInfo] = None


class ChainScanner:
    """Service to scan chain files and extract their parameter configurations."""

    def __init__(self, chains_directory: str = "src/chains"):
        self.chains_directory = Path(chains_directory)
        self.logger = logging.getLogger(__name__)

    def get_python_files(self) -> List[Path]:
        """Get all Python files in the chains directory."""
        return list(self.chains_directory.glob("*.py"))

    def load_module(self, file_path: Path):
        """Dynamically load a Python module from file path."""
        try:
            spec = importlib.util.spec_from_file_location(
                file_path.stem, file_path
            )
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load module from {file_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            self.logger.error(f"Error loading module {file_path}: {str(e)}")
            return None

    def extract_model_parameters(
        self, model_instance: Any
    ) -> List[ModelParameter]:
        """Extract configurable parameters from a LangChain model instance."""
        parameters = []

        # Get the signature of the model's constructor
        signature = inspect.signature(model_instance.__class__)

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue

            param_type = (
                str(param.annotation)
                if param.annotation != inspect.Parameter.empty
                else "Any"
            )
            default_value = (
                param.default
                if param.default != inspect.Parameter.empty
                else None
            )
            required = param.default == inspect.Parameter.empty

            parameters.append(
                ModelParameter(
                    name=param_name,
                    type=param_type,
                    default=default_value,
                    required=required,
                )
            )

        return parameters

    def extract_prompt_info(self, module: Any) -> Optional[PromptInfo]:
        """Extract prompt information from the module."""
        try:
            # First try to find prompt directly
            prompt = getattr(module, "prompt", None)

            # If no direct prompt, try to get it from chain
            if prompt is None and hasattr(module, "chain"):
                if isinstance(module.chain, LLMChain):
                    prompt = module.chain.prompt

            if prompt is None:
                return None

            if isinstance(
                prompt,
                (PromptTemplate, ChatPromptTemplate, BasePromptTemplate),
            ):
                template_type = (
                    "chat"
                    if isinstance(prompt, ChatPromptTemplate)
                    else "prompt"
                )
                template_format = (
                    "jinja2"
                    if getattr(prompt, "template_format", "f-string")
                    == "jinja2"
                    else "f-string"
                )

                return PromptInfo(
                    template=(
                        prompt.template
                        if hasattr(prompt, "template")
                        else str(prompt)
                    ),
                    input_variables=list(prompt.input_variables),
                    template_type=template_type,
                    template_format=template_format,
                )

            return None
        except Exception as e:
            self.logger.error(f"Error extracting prompt info: {str(e)}")
            return None

    def scan_chains(self) -> List[ChainConfig]:
        """
        Scan all chain files and extract the prompt info as well as available parameter configurations of the model.
        Prerequisite: The chain file must have a 'model' attribute that refers to the model instance, and optionally a 'prompt' attribute.
        """
        configs = []

        for file_path in self.get_python_files():
            try:
                module = self.load_module(file_path)

                # TODO: Check if this if condition is sufficient for prompt info extraction as well
                if module and hasattr(module, "model"):
                    model_params = self.extract_model_parameters(module.model)
                    prompt_info = self.extract_prompt_info(module)

                    configs.append(
                        ChainConfig(
                            chain_name=file_path.stem,
                            model_parameters=model_params,
                            prompt_info=prompt_info,
                        )
                    )
            except Exception as e:
                self.logger.error(
                    f"Error processing chain {file_path}: {str(e)}"
                )

        return configs
