import os
from dotenv import load_dotenv

# from api.ai_core.prompt import answer_prompt, standalone_question_prompt
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from api.ai_core.prompt import create_answer_prompt, create_standalone_question_prompt

# During development - use prompts without versioning
answer_prompt = create_answer_prompt(language="english")
standalone_question_prompt = create_standalone_question_prompt()


class ConversationalRetrievalBot:
    """
    A class for creating and managing conversational retrieval chains for multiple users.
    """

    def __init__(
        self,
        redis_url="http://127.0.0.1:6379",
        google_api_key=None,
        model="gemini-2.0-flash-lite",
        temperature=0.5,
        top_p=0.9,
    ):
        """
        Initialize the bot with configuration parameters.

        Args:
            redis_url (str, optional): Redis URL for chat history persistence. Defaults to environment variable.
            google_api_key (str, optional): Google API key. Defaults to environment variable.
            model (str, optional): Model name for Google Generative AI. Defaults to "gemini-2.0-flash-lite".
            temperature (float, optional): Temperature parameter for generation. Defaults to 0.5.
            top_p (float, optional): Top-p parameter for generation. Defaults to 0.9.
        """
        # Load environment variables if not explicitly provided
        load_dotenv()

        # Set API keys
        self.google_api_key = google_api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("Google API key is required")

        self.redis_url = redis_url  # or os.environ.get("REDIS_URL")
        if not self.redis_url:
            raise ValueError("Redis URL is required for persistent chat history")

        # Create LLM instance
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=self.google_api_key,
            model=model,
            temperature=temperature,
            top_p=top_p,
            # convert_system_message_to_human=True
        )

        # Use the same LLM for question condensation
        self.condense_question_llm = self.llm

        # Store user chains
        self.user_chains = {}

    def _create_memory(self, session_id):
        """
        Create memory specific to a user session.

        Args:
            session_id (str): Unique identifier for the user session.

        Returns:
            ConversationBufferMemory: Memory instance for the specified session.
        """
        message_history = RedisChatMessageHistory(
            session_id=session_id, url=self.redis_url
        )
        memory = ConversationBufferMemory(
            chat_memory=message_history,
            return_messages=True,
            memory_key="chat_history",
            output_key="answer",
            input_key="question",
        )
        return memory

    def get_chain_for_user(self, session_id, retriever, language="english"):
        """
        Get or create a conversational chain for a specific user.

        Args:
            session_id (str): Unique identifier for the user session.
            retriever: Document retriever instance.
            language (str, optional): Language for responses. Defaults to "english".

        Returns:
            ConversationalRetrievalChain: Chain for the specified user.
        """
        # Return existing chain if already created
        if session_id in self.user_chains:
            return self.user_chains[session_id]

        # Create user-specific memory
        memory = self._create_memory(session_id)

        # Create the chain
        chain = ConversationalRetrievalChain.from_llm(
            condense_question_prompt=standalone_question_prompt,
            combine_docs_chain_kwargs={"prompt": answer_prompt},
            condense_question_llm=self.condense_question_llm,
            memory=memory,
            retriever=retriever,
            llm=self.llm,
            chain_type="stuff",
            verbose=False,
            return_source_documents=True,
        )

        # Store chain for future use
        self.user_chains[session_id] = chain

        return chain

    def process_query(self, session_id, question, retriever, language="english"):
        """
        Process a user query and return the response.

        Args:
            session_id (str): Unique identifier for the user session.
            question (str): User's question.
            retriever: Document retriever instance.
            language (str, optional): Language for the response. Defaults to "english".

        Returns:
            dict: Response containing the answer and source documents.
        """
        chain = self.get_chain_for_user(session_id, retriever, language)
        return chain.invoke({"question": question})

    def clear_user_history(self, session_id):
        """
        Clear conversation history for a specific user.

        Args:
            session_id (str): Unique identifier for the user session.
        """
        if session_id in self.user_chains:
            # Remove from cache
            del self.user_chains[session_id]

        # Create and immediately clear Redis history
        message_history = RedisChatMessageHistory(
            session_id=session_id, url=self.redis_url
        )
        message_history.clear()


class ChatbotService:
    """
    Service class that uses the ConversationalRetrievalBot to provide chatbot functionality.
    """

    def __init__(self, retriever, redis_url=None):
        """
        Initialize the chatbot service.

        Args:
            redis_url (str, optional): Redis URL for chat history persistence.
        """
        # Initialize the conversational bot
        self.bot = ConversationalRetrievalBot(redis_url=redis_url)
        # Store the global retriever service
        self.retriever = retriever

    def chat(
        self, user_id: str, article_id: str, message: str, language: str = "english"
    ):
        """
        Process a user message and return the chatbot's response.

        Args:
            user_id (str): Unique identifier for the user.
            article_id (str): ID of the article to search within.
            message (str): User's message.
            language (str, optional): Language for the response. Defaults to "english".

        Returns:
            dict: Chatbot's response containing the answer and source documents.
        """
        # Create a session ID that includes both user ID and article ID
        # This ensures separate conversation history for each user-article pair
        session_id = f"{user_id}:{article_id}"
        adapted_retriever = self.retriever.vectorstore_backed_retriever(int(article_id))

        # Process the query
        response = self.bot.process_query(
            session_id=session_id,
            question=message,
            retriever=adapted_retriever,
            language=language,
        )
        chain = self.bot.get_chain_for_user(session_id, adapted_retriever, language)
        chat_history = (
            chain.memory.chat_memory.messages if hasattr(chain, "memory") else []
        )

        # Process the chat history to a more usable format
        processed_history = []
        for msg in chat_history:
            # Convert LangChain message objects to a simpler dict format
            # Typically messages have a 'type' (human/ai) and 'content'
            msg_type = "user" if msg.type == "human" else "assistant"
            processed_history.append({"role": msg_type, "content": msg.content})

        # Return the full response including answer and source documents
        return {"answer": response["answer"], "chat_history": processed_history}

    def reset_conversation(self, user_id: str, article_id: str):
        """
        Reset the conversation history for a user-article pair.

        Args:
            user_id (str): Unique identifier for the user.
            article_id (str): ID of the article.
        """
        session_id = f"{user_id}:{article_id}"
        self.bot.clear_user_history(session_id)
