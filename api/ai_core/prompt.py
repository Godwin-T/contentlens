import os
import hashlib
from dotenv import load_dotenv
from promptlayer import PromptLayer


from langchain.prompts import PromptTemplate, ChatPromptTemplate

load_dotenv()

api_key = os.getenv("PROMPT_LAYER_API_KEY")
pl_client = PromptLayer(api_key="pl_0da568cdc2c67d1b0e81fe8937296290")

# Create a cache for template hashes to track changes
template_cache = {}


def get_content_hash(content):
    """Generate a hash of the content for comparison."""
    return hashlib.md5(content.encode()).hexdigest()


def publish_template_to_promptlayer(
    prompt_name,
    template_content,
    input_variables,
    tags=None,
    template_type="completion",
    template_format="f-string",
    commit_message=None,
    metadata=None,
    force_update=False,
):
    """
    Publish a template to PromptLayer only if it has changed.

    Args:
        prompt_name (str): Name of the prompt template
        template_content (str): The template string
        input_variables (list): List of input variables used in the template
        tags (list, optional): Tags to categorize the template
        template_type (str, optional): Template type (completion or chat)
        template_format (str, optional): Format of the template (f-string, jinja2, etc.)
        commit_message (str, optional): Commit message for this version
        metadata (dict, optional): Additional metadata for the template
        force_update (bool, optional): Whether to force an update regardless of changes

    Returns:
        dict: Response from PromptLayer API or None if no update was needed
    """
    tags = tags or []
    metadata = metadata or {}
    commit_message = commit_message or f"Updated {prompt_name}"

    # Calculate content hash
    content_hash = get_content_hash(template_content)

    # Check if we've already cached this template's hash
    if not force_update and prompt_name in template_cache:
        if template_cache[prompt_name] == content_hash:
            print(f"No changes detected for template '{prompt_name}'. Skipping update.")
            return None

    # Try to fetch the latest version to compare
    try:
        latest_template = get_template_from_promptlayer(prompt_name)
        latest_hash = get_content_hash(latest_template)

        if not force_update and latest_hash == content_hash:
            print(
                f"Template '{prompt_name}' matches the latest version. Skipping update."
            )
            template_cache[prompt_name] = content_hash
            return None
    except:
        # If we can't fetch the latest version, assume this is a new template
        pass

    # Update the template cache
    template_cache[prompt_name] = content_hash

    template_data = {
        "prompt_name": prompt_name,
        "tags": tags,
        "prompt_template": {
            "content": [{"type": "text", "text": template_content}],
            "input_variables": input_variables,
            "template_format": template_format,
            "type": template_type,
        },
        "metadata": metadata,
        "commit_message": commit_message,
    }

    print(f"Publishing updated template '{prompt_name}'")
    return pl_client.templates.publish(template_data)


def get_template_from_promptlayer(prompt_name, version=None):
    """
    Get a template from PromptLayer.

    Args:
        prompt_name (str): Name of the prompt template
        version (str, optional): Version label or ID to retrieve. Defaults to None (latest).

    Returns:
        str: The template content
    """
    try:
        if version:
            template = pl_client.templates.get(prompt_name, version=version)
        else:
            template = pl_client.templates.get(prompt_name)

        # Extract the text content from the template
        if (
            template
            and "prompt_template" in template
            and "content" in template["prompt_template"]
        ):
            for content_item in template["prompt_template"]["content"]:
                if content_item["type"] == "text":
                    return content_item["text"]

        raise Exception(f"Template format unexpected: {template}")
    except Exception as e:
        raise KeyError(f"Error retrieving template '{prompt_name}': {str(e)}")


def answer_template(language="english", version=None):
    """
    Create or retrieve a template for answering questions.

    Args:
        language (str, optional): Language for the response. Defaults to "english".
        version (str, optional): Specific version to use. Defaults to None (latest).

    Returns:
        str: Template string.
    """
    prompt_name = "answer_template"

    # Define input variables
    input_variables = ["chat_history", "context", "question"]

    # If a specific version is requested, retrieve it
    if version:
        return get_template_from_promptlayer(prompt_name, version)

    # Create the template content without publishing
    template_content = f"""Respond appropriately to the user's message below. If it's a greeting or casual conversation,
    respond in a friendly and natural manner. If it's a question seeking information, use both the provided
    context (delimited by <context></context>) and your own knowledge to provide a helpful response.
    
    <context>
    {{chat_history}}
    {{context}}
    </context>
    
    User message: {{question}}
    Language: {language}
    
    When addressing informational questions:
    1. Use the context as a primary source when directly relevant
    2. Supplement with your own knowledge when appropriate
    3. Maintain a conversational, helpful tone throughout
    """

    # Cache the hash but don't publish
    template_cache[prompt_name] = get_content_hash(template_content)

    return template_content


def standalone_template(version=None):
    """
    Create or retrieve a template for standalone questions.

    Args:
        version (str, optional): Specific version to use. Defaults to None (latest).

    Returns:
        str: Template string.
    """
    prompt_name = "standalone_template"

    # Define input variables
    input_variables = ["chat_history", "question"]

    # If a specific version is requested, retrieve it
    if version:
        return get_template_from_promptlayer(prompt_name, version)

    # Create the template content without publishing
    template_content = """Given the following conversation and a follow up question,
    rephrase the follow up question to be a standalone question, in its original language.
    
    Chat History:
    {chat_history}
    
    Follow Up Input: {question}
    Standalone question:"""

    # Cache the hash but don't publish
    template_cache[prompt_name] = get_content_hash(template_content)

    return template_content


# Create LangChain prompts without publishing
def create_answer_prompt(language="english", version=None):
    """Create a LangChain ChatPromptTemplate without versioning."""
    template = answer_template(language=language, version=version)
    return ChatPromptTemplate.from_template(template)


def create_standalone_question_prompt(version=None):
    """Create a LangChain PromptTemplate without versioning."""
    template = standalone_template(version=version)
    return PromptTemplate(
        input_variables=["chat_history", "question"], template=template
    )
