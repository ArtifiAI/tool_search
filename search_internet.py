import requests
from Blueprint.Templates.Tools.python_base_tool import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults


class SearchTool(BaseTool):
    name = "SearchTool"
    description = "Searches the internet using a query and returns the top result."
    requires_env_vars = [
        "TAVILY_API_KEY : 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"
    ]  # No required env variables for now
    dependencies = [("requests", "requests")]  # Ensure `requests` is installed
    uses_llm = False  # No LLM involved
    input_schema = {
        "type": "object",
        "properties": {
            "input_data": {
                "query": {"type": "string", "description": "The search query"},
                "number_of_search_results": {
                    "type": "integer",
                    "description": "Number of search results to return",
                },
            },
        },
        "required": ["query"],
    }
    output_schema = {
        "type": "object",
        "properties": {
            "result": {"type": "string", "description": "Top search result"}
        },
    }
    response_type = "json"


    def run_sync(self, input_data=None, llm_config=None):
        """
        Performs a web search using the input query and returns the top result.
        """
        if not isinstance(input_data, dict) or "query" not in input_data:
            raise ValueError("Input must be a dictionary with a 'query' key.")

        query = input_data.get("query", "").strip()

        if input_data.get("number_of_search_results", ""):
            number_of_search_results = input_data.get("number_of_search_results")
        else:
            number_of_search_results = 5

        if not query:
            return {"error": "Query cannot be empty"}

        try:
            tavily_tool = TavilySearchResults(max_results=number_of_search_results)

            return {
                "result": tavily_tool.invoke(query)
            }  # Return first 500 chars as sample

        except requests.RequestException as e:
            return {"error": f"Request error: {str(e)}"}


