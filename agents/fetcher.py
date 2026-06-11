from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from agents.state import GraphState
import json
import asyncio
def fetcher_node(state:GraphState):
    server_params=StdioServerParameters(
    command="python",
    args=["mcp_server/server.py"]
     )
    async def fetch():
       async with stdio_client(server_params) as (
    read_stream,
    write_stream,
    ):
        async with ClientSession(
          read_stream,
          write_stream
        ) as session:
           await session.initialize()
           result1=await session.call_tool(
               'get_pr_details_mcp',
               {
                   "repo_name":state["repo_name"],
                   "pr_number":state["pr_number"]
               }
           )
           result2=await session.call_tool(
               "get_pullRequest_files",
               {
                "repo_name":state["repo_name"],
                "pr_number":state["pr_number"]   
               }
           )
           return {
               "pr_metadata": json.loads(result1.content[0].text) ,
               "diff_files":json.loads(result2.content[0].text)
           }
    return asyncio.run(fetch())
       
       
    

