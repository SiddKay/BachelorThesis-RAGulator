from typing import Dict, Any
from .chain_loader import ChainLoader
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate


class PromptManager:
    def __init__(self, chain_loader: ChainLoader):
        self.chain_loader = chain_loader

    def get_prompt_template(self, chain_name: str) -> Dict[str, Any]:
        """Get the current prompt template configuration."""
        chain = self.chain_loader.get_chain(chain_name)
        if not hasattr(chain, "prompt"):
            raise ValueError(
                f"Chain '{chain_name}' does not have a prompt attribute"
            )

        prompt = chain.prompt
        if not isinstance(prompt, (PromptTemplate, ChatPromptTemplate)):
            raise ValueError(
                f"Chain '{chain_name}' prompt is not a valid template"
            )

        template_info = {
            "template": prompt.template,
            "input_variables": prompt.input_variables,
            "template_type": prompt.__class__.__name__,
        }

        # Add chat-specific information if it's a ChatPromptTemplate
        if isinstance(prompt, ChatPromptTemplate):
            template_info["messages"] = [
                {"role": msg.role, "template": msg.template}
                for msg in prompt.messages
            ]

        return template_info

    def update_prompt_template(
        self, chain_name: str, template_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the prompt template for a specific chain."""
        # Reset chain to original state before applying new template
        self.chain_loader.reset_chain(chain_name)
        chain = self.chain_loader.get_chain(chain_name)

        if not hasattr(chain, "prompt"):
            raise ValueError(
                f"Chain '{chain_name}' does not have a prompt attribute"
            )

        original_prompt = chain.prompt
        try:
            if isinstance(original_prompt, ChatPromptTemplate):
                if "messages" not in template_config:
                    raise ValueError(
                        "Messages required for ChatPromptTemplate"
                    )

                new_prompt = ChatPromptTemplate.from_messages(
                    template_config["messages"]
                )
            else:
                if (
                    "template" not in template_config
                    or "input_variables" not in template_config
                ):
                    raise ValueError(
                        "Template and input_variables required for PromptTemplate"
                    )

                new_prompt = PromptTemplate(
                    template=template_config["template"],
                    input_variables=template_config["input_variables"],
                )

            # Validate the new prompt by ensuring it has all required attributes
            if not hasattr(new_prompt, "template") or not hasattr(
                new_prompt, "input_variables"
            ):
                raise ValueError("Invalid prompt template configuration")

            # Update the chain's prompt
            chain.prompt = new_prompt

            return self.get_prompt_template(chain_name)

        except Exception as e:
            # Reset chain to original state if update fails
            self.chain_loader.reset_chain(chain_name)
            raise ValueError(f"Error updating prompt template: {str(e)}")
