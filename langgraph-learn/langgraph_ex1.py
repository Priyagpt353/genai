from dotenv import load_dotenv
from langchain.tools import tool
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage
from langchain.messages import ToolMessage
from typing import Literal
from langgraph.graph import MessagesState, StateGraph, START, END
from IPython.display import Image, display


load_dotenv()

llm = init_chat_model(
    model="gpt-3.5-turbo",
    model_provider="openai"
)

@tool
def add(x: int, y: int) -> int:
    return x + y

@tool
def multiply(x: int, y: int) -> int:
    return x * y

@tool
def divide(x: int, y: int) -> int:
    return x/y

tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = llm.bind_tools(tools)

# defining state
class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage],operator.add]
    llm_calls:int

# defining model node
def llm_call(state:dict):
    return {
        "messages":[
            model_with_tools.invoke([
                SystemMessage(
                    content='''You are an helpful assistant tasked with 
                            performing arithmetic on a set of inputs.'''
                )
            ] + state["messages"])
        ],
        "llm_calls": state["llm_calls"] + 1
    }

# tool node

def tool_node(state:dict):
    results = []
    for tool_call in state["messages"][-1].tool_call:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        results.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": results}

def should_continue(state: MessagesState) -> Literal["tool_node",END]:
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool_node"

    return END

# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()

# Show the agent
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

# Invoke
from langchain.messages import HumanMessage
messages = [HumanMessage(content="Add 3 and 4.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()


