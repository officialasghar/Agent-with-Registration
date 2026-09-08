from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from app.tools.weather_tool import get_weather
from app.config import gemini_model
from app.tools.time_tool import get_current_time
from app.config import llama_model


from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents.middleware import before_model
from langchain.agents.middleware import SummarizationMiddleware
from app.settings import settings


from typing import Any

from dotenv import load_dotenv

load_dotenv()


SYSTEM_PROMPT = """
You are a helpful weather assistant.

Rules:
1. Use the weather tool when the user asks about weather.
2. Do not use the weather tool for unrelated questions.
3. Give a concise and clear answer.
4. If the location is missing, ask the user for the location.
"""


DB_URL = settings.AGENT_DB_URL



def chat_with_agent(request, thread_id, user_id):

    messages = [HumanMessage(content=request)]

    user_thread_id = f"{user_id}:{thread_id}"
    thread_config: RunnableConfig = {"configurable": {"thread_id": user_thread_id}}

    with PostgresSaver.from_conn_string(DB_URL) as checkpointer:

        checkpointer.setup()

        agent = create_agent(
            model=gemini_model,
            tools=[get_weather, get_current_time],
            system_prompt=SYSTEM_PROMPT,
            checkpointer=checkpointer,
            middleware=[
                    SummarizationMiddleware(
                        model=llama_model,
                        trigger=("tokens", 500),
                        keep=("messages", 5)
                    )
            ],
        )

        res = agent.invoke(
            {"messages": messages},
            thread_config
        )


        return {
            "response": res["messages"][-1].content[0]["text"]
        }