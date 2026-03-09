import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, InferenceClientModel
from time import sleep
import litellm
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
# it can be used for API keys or other sensitive information
# add .env in /Agents folder with the following content
# GROQ_API_KEY=your-groq-api-key
# XAI_API_KEY=your-xai-api-key
load_dotenv()


class SearchAgent:
    """A class to represent a web search agent that uses a specified model to execute search queries.

    Attributes:
        delay (int): Delay in seconds before making a request.
        model_name (str): The name of the model to use for the search.
        model (LiteLLMModel): The model instance used for generating completions.

    Methods:
        __init__(delay=0, host="xai"):
            Initializes the SearchAgent with the specified delay and host.
        
        call(query, max_results=20):
            Executes a search query using the CodeAgent with a custom delay callback.
    
        Initialize the WebSearchAgent.



        pass

        Executes a search query using the CodeAgent with a custom delay callback.

            max_results (int, optional): Maximum number of results to return. Defaults to 20.

        pass
    """
    def __init__(self, delay=0, host="xai"):
        """Initialize the WebSearchAgent.

        Args:
            delay (int, optional): Delay in seconds before making a request. Defaults to 0.
            host (str, optional): The host to use for the model. Must be either "groq" or "grok". Defaults to "xai".

        Raises:
            AssertionError: If the host is not "groq" or "grok".

        Environment Variables:
            GROQ_API_KEY: API key for the "groq" host.
            XAI_API_KEY: API key for the "grok" host.

        """
        ## set ENV variables
        

        # You may set environment variables for API keys manually
        # os.environ["GROQ_API_KEY"] = "your-groq-api-key"
        # os.environ["XAI_API_KEY"] = "your-xai-api-key"
        api_key = None
        model_kwargs = {"temperature": 0.2}

        if host == "groq":
            self.model_name = "groq/llama3-8b-8192"
            api_key = os.getenv("GROQ_API_KEY")
        elif host == "xai":
            self.model_name = "xai/grok-4-latest"
            api_key = os.getenv("XAI_API_KEY")
        elif host == "cerebras":
            self.model_name = "cerebras/llama-3.3-70b"
            api_key = os.getenv("CEREBRAS_API_KEY")
        elif host == "hf":
            self.model_name = os.getenv("HF_API")
        elif host == "ollama":
            ollama_model = os.getenv("OLLAMA_MODEL", "gemini-3-flash-preview:latest")
            if "/" in ollama_model:
                self.model_name = ollama_model
            else:
                self.model_name = f"ollama_chat/{ollama_model}"
            model_kwargs["api_base"] = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        else:
            raise AssertionError("Invalid host")
        self.delay = delay

        if host == "hf":
           self.model = InferenceClientModel(self.model_name)
        else:
            self.model = LiteLLMModel(
                self.model_name,
                api_key=api_key,
                **model_kwargs,
            )

    def call(self, query, max_results=20):
        """Executes a search query using the CodeAgent with a custom delay callback.

        Args:
            query (str): The search query to be executed.

        Returns:
            CodeAgent: The agent that executed the search query.
        """

        def add_delay(*args, **kwargs):
            """Custom callback function to add delay 
            It is used to add delay in the processing of the response 
            (i.e., when you have limited API calls - rpm or rps)
            """
            print("Adding delay")
            for i in tqdm(range(self.delay)):
                sleep(1)

        litellm._turn_on_debug()
        litellm.success_callback = [add_delay] # set custom callback function


        # Note that we are using CodeAgent
        agent = CodeAgent(tools=[   # Search engine tool with maximum number of results parameter
                                    DuckDuckGoSearchTool(max_results=max_results)

                                    # you can add more tools here
                                ], 

                          # Our LLM model for generating completions  
                          model=self.model)

        # Execute the agent with the query and tools
        # the agent will be updated with the results, logs and etc.
        agent.run(query)


        return agent # return the agent for further processing (we provide all details to frontend)
    
    def save(self, folder_path):
        """Save the model to a specified path.

        Args:
            path (str): The path to save the model.
        """
        self.model.save(folder_path)
    

if __name__=="__main__":
    # Initialize the SearchAgent
    agent = SearchAgent(delay=5, host="cerebras")
    #agent.save("search_agent")

    # Execute another search query
    agent.call("What is the weather in New York?")
