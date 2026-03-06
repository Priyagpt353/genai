from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import StateGraph, add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

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

# node 2
def sampleNode(state: State):
    print("\n\nInside sampleNode node", state)
    return { "messages": ["Sample Message Appended"] }

graph_builder = StateGraph(State)

# adding the nodes to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)

# defining the edges between the nodes
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

# compiling the graph
graph = graph_builder.compile()

updated_graph = graph.invoke(State({ "messages": ["Hey! how are you?"] }))
print("\n\nupdated_graph",updated_graph)

