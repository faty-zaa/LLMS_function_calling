from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class Prompt:
    user_prompt: str
    functions_definition: List[Dict[str, Any]]

    @property
    def update_prompt(self) -> str:
        prompt: str = ""

        prompt += """<|im_start|>assistant
        You are an AI assistant specialized in function calling
        by translating natural language requests into precise function
        calls with typed arguments, You do not answer the question directly
        Instead, you provides the tools to solve it:
        the right function name and
        the correct arguments with proper types
        <|im_end|>
        """

        prompt += """<|im_start|>user
        i will give you a natural language prompt that you must process,
        and a JSON contains the available functions you can call
        <|im_end|>
        """

        prompt += f"""<|im_start|>user
            {self.user_prompt}
        <|im_end|>"""

        # prompt += """<Tasks>
        # from the JSON file of functions that you can call,
        # you must give me the following keys:
        # -prompt (string): The original natural-language request (prompt)
        # -name (string): The name of the function to call
        # -parameters (object): All required arguments with the correct types
        # </Tasks>
        # """
        # prompt += """
        # <output_format>
        # {
        #     "prompt": "original prompt",
        #     "name": "function_name",
        #     "parameters": {
        #         ...
        #     }
        # }
        # </output_format>
        # """
        prompt += """
        <rules>
        - Output only valid JSON.
        - Do not include explanations.
        - Do not include markdown.
        - Do not include code fences.
        - Use exactly one function from the provided definitions.
        - Do not stop until you generate the valid output format.
        - For regex-based string substitution,
        choose a regex that matches the intended repeated pattern.
        """
        prompt += """
        <strict_rules>
        Regex mappings:
            vowels : "[aeiouAEIOU]"
            digits : "\\d+"
            whitespace : "\\s"
        </strict_rules>
        """
        prompt += f"""
        <available_functions>
        {self.functions_definition}
        </available_functions>
        """
        return prompt
