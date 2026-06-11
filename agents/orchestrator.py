    
from langgraph.graph import StateGraph
from langgraph.graph import START
from agents.fetcher import fetcher_node
from agents.reviewer import reviewer_node
from agents.test_writer import test_writer_node
from agents.summarizer import summarizer_node
from agents.state import GraphState

graph=StateGraph(GraphState)
graph.add_node("fetcher",fetcher_node)
graph.add_node("reviewer",reviewer_node)
graph.add_node("test_writer",test_writer_node)
graph.add_node("summarizer",summarizer_node)
graph.add_edge(START,"fetcher")
graph.add_edge("fetcher","reviewer")
graph.add_edge("reviewer","test_writer")
graph.add_edge("test_writer","summarizer")
app=graph.compile()


