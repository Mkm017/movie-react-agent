import os

from dotenv import load_dotenv

from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from tmdb_tool import movie_search_tool


load_dotenv()


def build_prompt():
    template = """
You are a Movie Recommendation Agent.

Your job is to recommend movies using the available tool.

IMPORTANT:

When users mention decades:

80s -> 1980-1989
90s -> 1990-1999
2000s -> 2000-2009
2010s -> 2010-2019

You have access to the following tools:

{tools}

Tool names:

{tool_names}

When calling movie_search_tool, always provide JSON.

Example:

Action: movie_search_tool

Action Input:
{{"genre":"horror","start_year":1990,"end_year":1999,"certification":"R"}}

After receiving tool results:

1. Analyze the returned movies.
2. Select ONE best recommendation.
3. Explain why it matches the user's constraints.
4. Do NOT repeat the entire list unless the user asks for multiple recommendations.

Use this format:

Question: the input question

Thought: identify genre
Thought: identify year range
Thought: identify certification

Action: one of [{tool_names}]

Action Input: a JSON string

Observation: tool result

Thought: analyze the results and select the best recommendation

Final Answer: recommend ONE movie with:
- Title
- Year
- TMDB Score
- Why it matches the request
- Short overview

Question: {input}

{agent_scratchpad}
"""
    return PromptTemplate.from_template(template)


def build_agent():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0,
    )

    prompt = build_prompt()

    agent = create_react_agent(
        llm=llm,
        tools=[movie_search_tool],
        prompt=prompt,
    )

    return AgentExecutor(
        agent=agent,
        tools=[movie_search_tool],
        verbose=True,
        handle_parsing_errors=True,
    )


def run_agent(query: str) -> str:
    agent_executor = build_agent()

    result = agent_executor.invoke(
        {"input": query}
    )

    return result["output"]


def main():
    print("\nMovie Recommendation ReAct Agent")
    print("-" * 40)

    query = input("\nEnter your request: ")

    output = run_agent(query)

    print("\nFinal Recommendation:\n")
    print(output)


if __name__ == "__main__":
    main()