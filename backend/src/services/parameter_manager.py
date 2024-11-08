from typing import Dict, Any
from .chain_loader import ChainLoader


class ParameterManager:
    def __init__(self, chain_loader: ChainLoader):
        self.chain_loader = chain_loader

    def _get_serializable_params(self, model) -> Dict[str, Any]:
        """Extract serializable parameters from the model."""
        params = {}
        try:
            model_vars = vars(model)
            for key, value in model_vars.items():
                if isinstance(value, (str, int, float, bool, list, dict)):
                    params[key] = value
        except Exception as e:
            raise ValueError(f"Error extracting parameters: {str(e)}")
        return params

    def get_chain_parameters(self, chain_name: str) -> Dict[str, Any]:
        """Get current model parameters for a specific chain."""
        module = self.chain_loader.get_module(chain_name)
        if not hasattr(module, "model"):
            raise ValueError(
                f"Chain '{chain_name}' does not have a model attribute"
            )

        return self._get_serializable_params(module.model)

    def update_chain_parameters(
        self, chain_name: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update model parameters for a specific chain."""
        # Reset chain to original state before applying new parameters
        self.chain_loader.reset_chain(chain_name)
        module = self.chain_loader.get_module(chain_name)

        if not hasattr(module, "model"):
            raise ValueError(
                f"Chain '{chain_name}' does not have a model attribute"
            )

        # Apply new parameters
        for param_name, param_value in parameters.items():
            if hasattr(module.model, param_name):
                try:
                    setattr(module.model, param_name, param_value)
                except Exception as e:
                    raise ValueError(
                        f"Invalid value for parameter '{param_name}': {str(e)}"
                    )
            else:
                raise ValueError(f"Invalid parameter name: {param_name}")

        return self.get_chain_parameters(chain_name)
