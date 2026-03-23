from langchain_tavily import TavilyExtract
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

tool = TavilyExtract(
    tavily_api_key ="your api",
    extract_depth="advanced", # Optional: can be 'basic' or 'advanced'
    include_images=True  # Optional: include image URLs in the output
)

# Define the URLs you want to extract content from
urls_to_extract = ["Hosted website url","github url"] # Replace with your URLs

# Invoke the tool with the list of URLs
results = tool.invoke({"urls": urls_to_extract})

system_prompt = """
    Generate a readme file content of {results} by the below format. 
    Project Title: The name of the project, typically the only level one heading (# Title).
    Description: A concise summary of what the project does, why it is useful, and the technologies used.
    Table of Contents (Optional): Helpful for longer README files to improve navigation.
    Installation: Step-by-step instructions and any prerequisites (e.g., specific software versions, dependencies) needed to set up and run the project locally.
    Usage: Examples of how to use the project, potentially including code snippets or screenshots.
    Contributing: Guidelines for how other developers can contribute to the project (e.g., pull requests, coding standards).
    License: Information about the project's license, often linking to a separate LICENSE file.
    Credits/Authors: github username
    """

prompt = ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    ("human","provide with in 1000 words of {results}")
    ])


llm = ChatGroq(model= "openai/gpt-oss-20b",groq_api_key="your api", max_completion_tokens=1024,temperature=0)
chain = prompt | llm

response = chain.invoke({
    "results" : results
})
# Print the extracted content
from IPython.display import Markdown, display

display(Markdown(response.content)) 
