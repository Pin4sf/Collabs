# Generate a `project.yaml` file from a list of steps.
>Based of C4GT 2024 Openfn

## Summary :-
Developing a Python module that takes a list of steps and their
corresponding adaptors as input and generates a `project.yaml` file. This
module should simplify the process of creating workflows for users.

## Core AI Approach Development
Employ a hybrid approach combining rule-based parsing and Natural Language Processing (NLP) techniques (NER)  for effective instruction analysis.
Utilize appropriate NLP libraries (e.g., NLTK, spaCy) and potentially train LLM models on OpenFn-specific workflow examples.

## Python Module Development

Implement a command-line interface (CLI) for clear user interactions.
Design modular code that separates instruction handling, AI processing, and YAML generation.
Incorporate the following default elements into the generated YAML:
Webhook trigger
Project name: "untitled-project"
Adaptors with @latest version


