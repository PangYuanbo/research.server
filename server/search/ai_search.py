import os

from dotenv import load_dotenv
from openai import OpenAI

from ..db.crud import get_researches_all, search_researches_by_ids
from ..db.dependencies import get_db

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
db = get_db()
researches = get_researches_all(db)


def ai_research(need: str):
    messages = [{"role": "user", "content": need},
                {"role": "system",
                 "content": "Match the user's request based on the information related to the RESEARCH in the "
                            "database. Returns the search_id that matches the request."},
                {"role": "system", "content": researches}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_researches_by_ids",
                "description": " Search for research projects by research_id list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "research_ids": {
                            "type": "list",
                            "items": {
                                "type": "uuid4"
                            }
                        }
                    },
                    "required": ["research_ids"],
                },
            }
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    return search_researches_by_ids(response.choices[0].message.content)
