import unittest

from src.C_decoding import Constrained


class ConstrainedDecodingTests(unittest.TestCase):
    def test_builds_function_call_payload_for_addition(self):
        functions_data = [
            {
                "name": "fn_add_numbers",
                "description": "Add two numbers together and return their sum.",
                "parameters": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "returns": {"type": "number"},
            }
        ]

        constrained = Constrained(
            prompt="What is the sum of 2 and 3?",
            functions_data=functions_data,
        )

        payload = constrained.build_function_call_payload("fn_add_numbers")

        self.assertEqual(payload["name"], "fn_add_numbers")
        self.assertEqual(payload["parameters"], {"a": 2, "b": 3})


if __name__ == "__main__":
    unittest.main()
