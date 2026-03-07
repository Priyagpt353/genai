from openai import OpenAI
from dotenv import load_dotenv
from typing import Literal, Optional
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

load_dotenv()
client = OpenAI()

llm = init_chat_model(
    model="gpt-3.5-turbo",
    model_provider="openai",
)

class State(TypedDict):
    user_query:str
    llm_output:Optional[str]
    is_good:Optional[str]

def chatbot(state:State):
    print("chatbot Node", state)
    response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages = [
        {"role":"user","content": state.get("user_query")}
    ])
    state["llm_output"] = response.choices[0].message.content
    return state

def gemini_chatbot(state:State):
    print("chatbot_gemini Node", state)
    response = client.chat.completions.create(
    model = "gpt-4.1",
    messages = [
        {"role":"user","content": state.get("user_query")}
    ])
    state["llm_output"] = response.choices[0].message.content
    return state

def check_response(state:State) -> Literal["gemini_chatbot","endNode"]:
    print("check_response Node", state)
    if False:
        return "endNode"
    return "gemini_chatbot"

def endNode(state:State):
    print("endNode Node", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("gemini_chatbot", gemini_chatbot)
graph_builder.add_node("endNode", endNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",check_response)
graph_builder.add_edge("gemini_chatbot","endNode")
graph_builder.add_edge("endNode",END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query":"Evaluate 2+2*4"}))
print("updated_state",updated_state)
