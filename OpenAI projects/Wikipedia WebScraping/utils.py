from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain.agents import Tool



system_prompt = """
You are a helpful assistant and an expert in all things related to music and songs.
The output must be in a JSON format enclosed in curly brackets, and does not contain any additional details or explanation.

Example:
'genre': 'Disco, Pop',
'label': 'Sony Music',
'language': 'Korean'
'producers': 'Alex Boh, Betty, Germaine',
'songwriters': 'John Johnson, Adam Smith'
"""


def generate_input_prompt(song: str, artist: str) -> str:
    input_prompt = f"""
    This is the song to review:
    - Song title: {song}, performed by {artist}

    Based on the above song information, accurately answer the following questions in order:
    - What is the genre of the song?
    - What is the name of the record label company?
    - What is the main language of the song?
    - Who are the producers of the song?
    - Who are the songwriters of the song?

    If you do not know the answer to any of these questions, return the answer as 'Unknown'. Do not make up any answers.

    Output the above answer strictly in JSON format enclosed with curly brackets. Do not include anything like ```json in the output.
    """
    print("Inside Generate input prompt")
    return input_prompt

wikipedia_tool = Tool(
    name="wikipedia",
    func=WikipediaAPIWrapper().run,
    description="Useful for when you need to look up the songwriters, genre, \
                and producers for a song on wikipedia",
)



def create_agent_executor(prompt, llm_with_tools, tools):
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
         
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    print("Agent Executor created")

    return agent_executor


def read_markdown_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."


# Define  callback function to return default values
def default_values(retry_state):
    # Return a set of default values if error occurs
    output = {
        "genre": "Unable to extract",
        "label": "Unable to extract",
        "language": "Unable to extract",
        "producers": "Unable to extract",
        "songwriters": "Unable to extract",
    }

    return output