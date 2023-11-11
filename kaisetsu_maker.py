import os
import sys
from src.openai_api_bridge import OpenAIAPIBridge
from src.explanation import Explanation

def run(apikey, question):
    api = OpenAIAPIBridge(apikey)
    generator = Explanation(api, "./resource", "./output")
    print(f"Question: {question}")
    generator.generate(question)


if __name__ == '__main__':
    api_key = os.environ.get("OPENAI_API_KEY")
    run(api_key, sys.argv[1])
