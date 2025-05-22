#!/usr/bin/env python
"""
Script to check for changes in prompt templates and version them on demand.
"""

import argparse
import importlib
import inspect
from prompt import (
    template_cache,
    publish_template_to_promptlayer,
    get_content_hash,
    get_template_from_promptlayer,
)


def get_all_template_functions(module_name):
    """Get all template functions from a module."""
    try:
        module = importlib.import_module(module_name)
        functions = {}

        # Find all functions that end with _template
        for name, obj in inspect.getmembers(module):
            if name.endswith("_template") and inspect.isfunction(obj):
                functions[name] = obj

        return functions
    except ImportError:
        print(f"Module {module_name} not found.")
        return {}


def version_templates(module_names, templates=None, commit_message=None, force=False):
    """
    Check and version all templates in the specified modules.

    Args:
        module_names (list): List of module names containing template functions
        templates (list, optional): Specific template names to version, or None for all
        commit_message (str, optional): Commit message for all templates
        force (bool, optional): Force versioning even if no changes detected
    """
    versioned = []
    unchanged = []

    for module_name in module_names:
        template_functions = get_all_template_functions(module_name)

        if not template_functions:
            print(f"No template functions found in module {module_name}")
            continue

        print(f"Found {len(template_functions)} template functions in {module_name}")

        for func_name, func in template_functions.items():
            # Skip if templates list is provided and this one isn't in it
            if templates and func_name not in templates:
                continue

            prompt_name = func_name

            try:
                # Get current template content
                template_content = func()
                content_hash = get_content_hash(template_content)

                # Set default to create new template
                should_create = True

                # Try to get latest version from PromptLayer
                try:
                    latest_template = get_template_from_promptlayer(prompt_name)
                    latest_hash = get_content_hash(latest_template)

                    # Template exists, check if it has changed
                    if not force and latest_hash == content_hash:
                        print(f"Template '{prompt_name}' is unchanged. Skipping.")
                        unchanged.append(prompt_name)
                        should_create = False  # Don't create if unchanged
                    else:
                        print(f"Template '{prompt_name}' has changed. Updating.")
                        should_create = True  # Update existing template

                except Exception as e:
                    # If we can't fetch the latest version, assume this is a new template
                    print(
                        f"Template '{prompt_name}' not found in PromptLayer. Creating new template."
                    )
                    should_create = True  # Create new template

                # Only proceed if we should create/update the template
                if should_create:
                    # Get input variables by inspecting function parameters
                    signature = inspect.signature(func)
                    # Filter out common parameters that aren't input variables
                    input_variables = [
                        param
                        for param in signature.parameters
                        if param not in ["version"]
                    ]

                    # For these specific templates, we know the input variables
                    if prompt_name == "answer_template":
                        input_variables = ["chat_history", "context", "question"]
                    elif prompt_name == "standalone_template":
                        input_variables = ["chat_history", "question"]

                    # Determine appropriate tags based on template name
                    tags = []
                    if "answer" in prompt_name:
                        tags = ["conversation", "answer"]
                    elif "standalone" in prompt_name:
                        tags = ["standalone", "question-rephrasing"]

                    # Publish the template
                    result = publish_template_to_promptlayer(
                        prompt_name=prompt_name,
                        template_content=template_content,
                        input_variables=input_variables,
                        tags=tags,
                        commit_message=commit_message or f"Updated {prompt_name}",
                        force_update=True,  # Force update when we've decided to create/update
                    )

                    if result:
                        versioned.append(prompt_name)
                        print(f"Successfully versioned '{prompt_name}'")

            except Exception as e:
                print(f"Error versioning template '{prompt_name}': {e}")

    print(f"\nSummary:")
    print(f"- Versioned: {len(versioned)} templates")
    print(f"- Unchanged: {len(unchanged)} templates")

    if versioned:
        print(f"\nVersioned templates: {', '.join(versioned)}")

    return versioned


def main():
    parser = argparse.ArgumentParser(description="Version prompt templates on demand")
    parser.add_argument(
        "--modules",
        "-m",
        nargs="+",
        default=["prompt"],
        help="Module names containing template functions",
    )
    parser.add_argument(
        "--templates",
        "-t",
        nargs="+",
        help="Specific template names to version (default: all)",
    )
    parser.add_argument(
        "--commit-message",
        "-c",
        type=str,
        help="Commit message for this batch of template changes",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force versioning even if no changes detected",
    )

    args = parser.parse_args()
    version_templates(args.modules, args.templates, args.commit_message, args.force)


if __name__ == "__main__":
    main()
