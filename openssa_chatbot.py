from pathlib import Path
from dotenv import load_dotenv
from openssa import DANA, FileResource

load_dotenv()


def get_or_create_agent() -> DANA:
    return DANA(resources={FileResource(Path("openssa_data"))})


def solve(question) -> str:
    agent = get_or_create_agent()
    print("Done Creating agent")
    try:
        return agent.solve(question)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    question = "What is the manga that the publish date is between 1997 and 2000?"
    # question = "Find me all manga series where the main character starts as weak but becomes powerful later. Then group them into different genres like fantasy, sci-fi, and sports."
    print("Question: ", question)
    print(solve(question))
