*This project has been created as part of the 42 curriculum by FALAMLIH*

# LLM Function Calling

## Description

This project implements structured function calling with a local Large Language Model using constrained decoding. The goal is to guide the model to generate valid JSON outputs that select an available function and fill its parameters with the correct types, instead of producing free-form text.

The project is designed for experiments around LLM-based tool use, structured generation, and reliable JSON decoding.

## Instructions

### Requirements

- Python 3.10+
- UV
- A local Hugging Face-compatible model backend

### Installation

Install dependencies with:

```bash
uv sync
```

If you are using the 42 environment, it is recommended to configure the cache directories first:

```bash
export HF_HOME=/goinfre/$USER/huggingface_cache
export TRANSFORMERS_CACHE=/goinfre/$USER/huggingface_cache
export UV_CACHE_DIR=/goinfre/$USER/.uv-cache
```

### Execution

Run the program with:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

### Linting

```bash
make lint
```

## Algorithm Explanation

The core idea is constrained decoding. During generation, the model is not allowed to pick arbitrary next tokens. Instead, the decoder validates the generated sequence against a finite set of allowed tokens that follow the expected structure of a function call.

This approach ensures:
- valid function names are selected;
- required parameters are emitted in the right order;
- argument values match the expected types;
- the final output remains valid JSON.

The implementation uses a state machine to track the current position in the JSON/function-call structure and only allows token transitions that preserve syntactic validity.

## Design Decisions

Several implementation choices were made to keep the system simple and reliable:

- The project uses a lightweight local SDK wrapper for the model to isolate model loading and token operations.
- A state-machine-based decoder is used instead of a fully general parser to keep the generation process efficient.
- Function definitions are parsed from structured JSON so that the decoder can enforce type-aware generation.
- The pipeline is intentionally modular: prompt building, JSON state handling, and token generation are separated into distinct components.

## Performance Analysis

The current solution is reliable for small and medium-sized function definition sets and produces structured outputs with predictable syntax. Its main strengths are correctness and controllability, while the main limitation is that generation speed depends on the model size and hardware available.

In practice:
- accuracy is high for simple function schemas;
- runtime is mostly influenced by model inference speed;
- reliability improves because invalid outputs are filtered by the constrained decoder.

## Challenges Faced

One of the main difficulties was ensuring that generated outputs stayed valid while still allowing the model to produce useful function calls. Without constraints, the model often produced malformed JSON or invalid function names.

Another challenge was aligning the decoding logic with the expected grammar for nested JSON and function parameters. This was solved by introducing a state-driven approach and by validating the generated token sequence step by step.

## Testing Strategy

The implementation was validated by checking:
- correct parsing of function definitions;
- valid generation of function names and arguments;
- proper JSON formatting of final outputs;
- robustness against malformed or incomplete prompts.

The current testing approach is mainly based on running the program on example input files and inspecting the generated JSON outputs.

## Example Usage

Example input file:

```json
{
  "prompt": "Call the weather function for Paris"
}
```

Example command:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

The generated output will contain a structured function call in JSON form.

## Resources

- [Constrained decoding explained](https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output#why-unconstrained-generation-fails)
- [Constrained decoding overview](https://www.aidancooper.co.uk/constrained-decoding/)
- [Qwen3 model](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Tokenizer tool](https://tiktokenizer.chatgptcn.com/)

## AI Usage

AI tools were used to help with:
- drafting and polishing the README;
- debugging type and import issues in the Python implementation;
- improving clarity of the constrained decoding logic and project documentation.
