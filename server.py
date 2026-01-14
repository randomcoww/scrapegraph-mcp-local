import os
import json
import asyncio
import uvicorn
from scrapegraphai.graphs import SmartScraperGraph
from langchain_openai import ChatOpenAI
from mcp.server.fastmcp import FastMCP
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)
mcp = FastMCP("mcp-scrapegraph-web-scraper", json_response=True)

llm_model_instance = ChatOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    model=os.getenv("OPENAI_MODEL"),
    api_key=os.getenv("OPENAI_API_KEY", "none"),
)

embedding_model_instance = ChatOpenAI(
    base_url=os.getenv("OPENAI_EMBEDDING_BASE_URL"),
    model=os.getenv("OPENAI_EMBEDDING_MODEL"),
    api_key=os.getenv("OPENAI_EMBEDDING_API_KEY", "none"),
)

graph_config = {
    "llm": {
        "model_instance": llm_model_instance,
        "model_tokens": int(os.getenv("OPENAI_MODEL_TOKENS", "8192")),
    },
    "embeddings": {
        "model_instance": embedding_model_instance,
        "model_tokens": int(os.getenv("OPENAI_EMBEDDING_MODEL_TOKENS", "8192")),
    },
    "verbose": True,
    "headless": True,
}


@mcp.tool()
async def scrape(prompt: str, url: str) -> str:
    """Scrape contents of URL"""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    def sync_scrape():
        scraper = SmartScraperGraph(prompt=prompt, source=url, config=graph_config)
        return scraper.run()

    try:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(executor, sync_scrape)
        return json.dumps(result)
    except Exception as e:
        return str(e)


def main():
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app = mcp.streamable_http_app()
    uvicorn.run(app, host=host, port=port, log_level="info", access_log=True)


if __name__ == "__main__":
    main()
