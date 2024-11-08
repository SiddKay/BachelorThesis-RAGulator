import os
import importlib.util
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class ChainConfig:
    """Stores the original configuration of a chain module"""

    module_path: str
    module_name: str
    original_params: Dict[str, Any]

    def reload_chain(self) -> Any:
        """Recreates the chain from scratch using the original module"""
        spec = importlib.util.spec_from_file_location(
            self.module_name, self.module_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.chain


class ChainLoader:

    def __init__(self, chains_dir: str = "src/chains"):
        self.chains_directory = chains_dir
        self._chain_configs: Dict[str, ChainConfig] = (
            {}
        )  # Store chain configurations
        self._active_modules: Dict[str, Any] = (
            {}
        )  # Store active module instances
        self._load_chains()

    def _extract_model_params(self, module: Any) -> Dict[str, Any]:
        """Extract serializable parameters from a model"""

        if not hasattr(module, "model"):
            raise ValueError("Module does not have a 'model' attribute")

        params = {}
        try:
            model_vars = vars(module.model)
            for key, value in model_vars.items():
                # Only store primitive types that we know are safe to serialize
                if isinstance(value, (str, int, float, bool, list, dict)):
                    params[key] = value
        except Exception as e:
            print(f"Warning: Could not extract all parameters: {str(e)}")
        return params

    def _load_chains(self) -> None:
        """Load all chain files from the specified directory."""
        for filename in os.listdir(self.chains_directory):
            if filename.endswith(".py"):
                chain_name = filename[:-3]  # Remove .py extension
                try:
                    # Load module dynamically
                    chain_path = os.path.join(self.chains_directory, filename)
                    spec = importlib.util.spec_from_file_location(
                        chain_name, chain_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Validate required attributes
                    if not all(
                        hasattr(module, attr)
                        for attr in ["chain", "model", "prompt"]
                    ):
                        raise ValueError(
                            f"Chain file {chain_name} missing required attributes: chain/model/prompt"
                        )

                    # Store the configuration
                    self._chain_configs[chain_name] = ChainConfig(
                        module_path=chain_path,
                        module_name=chain_name,
                        original_params=self._extract_model_params(
                            module.model
                        ),
                    )

                    # Store the module instance
                    self._active_modules[chain_name] = module

                except Exception as e:
                    print(f"Error loading chain {chain_name}: {str(e)}")

    def get_module(self, chain_name: str) -> Any:
        """Get the current active module instance"""
        if chain_name not in self._active_modules:
            raise ValueError(f"Chain '{chain_name}' not found")
        return self._active_modules[chain_name]

    def get_chain(self, chain_name: str) -> Any:
        """Get the current active chain instance"""
        module = self.get_module(chain_name)
        return module.chain

    def reset_chain(self, chain_name: str) -> None:
        """Reset a chain to its original state by recreating it"""
        if chain_name not in self._chain_configs:
            raise ValueError(f"Chain '{chain_name}' not found")

        # Recreate the chain from scratch using stored configuration
        self._active_modules[chain_name] = self._chain_configs[
            chain_name
        ].reload_chain()

    def list_available_chains(self) -> list[str]:
        """Get list of available chain names"""
        return list(self._chain_configs.keys())

    def get_original_parameters(self, chain_name: str) -> Dict[str, Any]:
        """Get the original parameters for a chain"""
        if chain_name not in self._chain_configs:
            raise ValueError(f"Chain '{chain_name}' not found")
        return self._chain_configs[chain_name].original_params.copy()
