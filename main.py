import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from scrapegraphai.graphs import SmartScraperGraph

app = FastAPI()

# Default prompt
DEFAULT_PROMPT = """
    Present the metadata of all the polls mentioned in the article in the following JSON format:

    {
        "polls": [
        {
            "pollster": "Pollster name (or 'N/A' if not available)",
            "sponsor": "Sponsor of the poll (or 'N/A' if not available)",
            "date": "Dates the poll was conducted (or 'N/A' if not available)",
            "location": "Location of the poll (or 'N/A' if not available)",
            "sample_size": "Sample size of the poll (or 'N/A' if not available)",
            "poll url": "URL of the poll (or 'N/A' if not available)"
        },
        ...
    }

    Make sure to include all available poll metadata, even if some fields are marked as 'N/A'.
    Do not hallucinate.
"""

# Input model
class ProcessRequest(BaseModel):
    url: str
    api_key: str
    prompt: Optional[str] = None


@app.post("/process")
async def process(request: ProcessRequest):
    try:
        if not request.url:
            raise HTTPException(status_code=400, detail="URL is required")
        if not request.api_key:
            raise HTTPException(status_code=400, detail="API key is required")

        prompt = request.prompt or DEFAULT_PROMPT
        source_url = 'https://r.jina.ai/' + request.url

        # Define the configuration for the scraping pipeline
        graph_config = {
            "llm": {
                "api_key": request.api_key,
                "model": "openai/gpt-4o-mini",
            },
            "verbose": True,
            "headless": True,
        }

        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source_url,
            config=graph_config
        )

        result = smart_scraper_graph.run()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

