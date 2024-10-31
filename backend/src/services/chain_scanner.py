from pathlib import Path
import importlib.util
import inspect
from typing import Any, List, Optional
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
)


@dataclass
class ModelParameter:
    name: str
    type: str
    default: Any
    required: bool = False
    configurable: bool = False


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

    def extract_model_from_runnable(self, runnable: RunnableSequence) -> Any:
        """Extract the model from a RunnableSequence."""
        try:
            # Traverse the runnable steps to find the model
            for step in runnable.steps:
                # If step is the model directly
                if hasattr(step, "model_name"):
                    return step
                # If step is ConfigurableField containing the model
                if isinstance(step, ConfigurableField):
                    if hasattr(step.default, "model_name"):
                        return step.default
            return None
        except Exception as e:
            self.logger.error(
                f"Error extracting model from runnable: {str(e)}"
            )
            return None

    def extract_prompt_from_runnable(
        self, runnable: RunnableSequence
    ) -> Optional[BasePromptTemplate]:
        """Extract the prompt from a RunnableSequence."""
        try:
            # Traverse the runnable steps to find the prompt
            for step in runnable.steps:
                if isinstance(step, (PromptTemplate, ChatPromptTemplate)):
                    return step
                if isinstance(step, ConfigurableField):
                    if isinstance(
                        step.default, (PromptTemplate, ChatPromptTemplate)
                    ):
                        return step.default
            return None
        except Exception as e:
            self.logger.error(
                f"Error extracting prompt from runnable: {str(e)}"
            )
            return None

    def extract_model_parameters(
        self, model_instance: Any
    ) -> List[ModelParameter]:
        """Extract configurable parameters from a LangChain model instance."""
        parameters = []

        # Handle ConfigurableField wrapper
        if isinstance(model_instance, ConfigurableField):
            model_instance = model_instance.default

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

            # Check if this parameter is marked as configurable
            configurable = False
            if hasattr(model_instance, "_configurable_fields"):
                configurable = (
                    param_name in model_instance._configurable_fields
                )

            parameters.append(
                ModelParameter(
                    name=param_name,
                    type=param_type,
                    default=default_value,
                    required=required,
                    configurable=configurable,
                )
            )

        return parameters

    def extract_prompt_info(self, module: Any) -> Optional[PromptInfo]:
        """Extract prompt information from the module."""
        try:
            prompt = None

            # First try to get prompt directly from module
            if hasattr(module, "prompt"):
                prompt = module.prompt

            # If no direct prompt and chain exists, try to extract from chain
            elif hasattr(module, "chain"):
                chain = module.chain
                if isinstance(chain, LLMChain):
                    prompt = chain.prompt
                elif isinstance(chain, RunnableSequence):
                    prompt = self.extract_prompt_from_runnable(chain)

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

                if module:
                    model_instance = None

                    # Try to get model directly
                    if hasattr(module, "model"):
                        model_instance = module.model
                    # If no direct model but chain exists, try to extract from chain
                    elif hasattr(module, "chain"):
                        if isinstance(module.chain, RunnableSequence):
                            model_instance = self.extract_model_from_runnable(
                                module.chain
                            )

                    if model_instance:
                        model_params = self.extract_model_parameters(
                            model_instance
                        )
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
