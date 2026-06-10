from langchain_groq import ChatGroq
from dotenv import load_dotenv
from agents.orchestrator import GraphState
from mcp import (StdioServerParameters,stdio_client)
from mcp import ClientSession
from langchain_core.messages import (SystemMessage,HumanMessage)
import asyncio

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")

def summarizer_node(state:GraphState):
    review_metadata=state["review_metadata"]
    test_metadata=state["test_metadata"]
    summary=llm.invoke([
        SystemMessage(
            content="Summarize the given content as best as possible"
        ),
        HumanMessage(
            content=f"summarize this for me: \n\n {review_metadata} \n\n {test_metadata}"
        )
    ])
    async def mcp_call():
        system_params=StdioServerParameters(
            command="python",
            args=["mcp_server/server.py"]
        )
        async with stdio_client(system_params) as(
            read_stream,
            write_stream,
        ):
            async with ClientSession(
                read_stream,
                write_stream
            ) as session:
                await session.initialize()
                result= await session.call_tool(
                    "post_review_comment",
                    {
                        "repo_name":state["repo_name"],
                        "pr_number":state["pr_number"],
                        "comment":summary.content
                    }
                )
    asyncio.run(mcp_call())
    return {"summary_metadata":summary.content}




