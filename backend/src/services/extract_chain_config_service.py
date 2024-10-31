from typing import Dict, Any, List
from .chain_scanner import ChainScanner, ChainConfig, PromptInfo
from dataclasses import asdict


class ChainConfigService:
    def __init__(self):
        self.scanner = ChainScanner()

    def get_all_chain_configs(self) -> List[Dict[str, Any]]:
        """Get configurations for all available chains."""
        configs = self.scanner.scan_chains()
        return [self._format_config(config) for config in configs]

    def get_chain_config(self, chain_name: str) -> Dict[str, Any]:
        """Get configuration for a specific chain."""
        configs = self.scanner.scan_chains()
        config = next((c for c in configs if c.chain_name == chain_name), None)
        if not config:
            raise ValueError(f"Chain '{chain_name}' not found")
        return self._format_config(config)

    def _format_config(self, config: ChainConfig) -> Dict[str, Any]:
        """Format ChainConfig into a JSON-serializable dictionary."""
        return {
            "chain_name": config.chain_name,
            "parameters": [asdict(param) for param in config.model_parameters],
            "prompt": (
                asdict(config.prompt_info) if config.prompt_info else None
            ),
        }
