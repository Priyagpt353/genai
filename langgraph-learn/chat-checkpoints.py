from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import StateGraph, add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

llm = init_chat_model(
    model="gpt-3.5-turbo",
    model_provider="openai",
)

# defining state for the chat, which is a list of messages
class State(TypedDict):
    messages: Annotated[list, add_messages]

# defining the chatbot function, which takes in the state and returns a response from the LLM
# node 1: chatbot
def chatbot(state: State):
    response = llm.invoke(state.get("messages", []))
    return { "messages": response }


graph_builder = StateGraph(State)

# adding the nodes to the graph
graph_builder.add_node("chatbot", chatbot)

# defining the edges between the nodes
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# compiling the graph
graph = graph_builder.compile()

def compile_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://roor:password@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_with_checkpointer(checkpointer=checkpointer)
    config = {
            "configurable": {
                "thread_id": "1" # user_id
            }
        }
    for chunk in graph_with_checkpointer.stream(
        State({"messages": ["what is my name?"]}),
        config,
        stream_mode="values"
        ):
            chunk["messages"][-1].pretty_print()



