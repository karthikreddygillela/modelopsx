from typing import Optional
import requests
import time

class SimpleSearchAgent:
    def __init__(self):
        self.memory = []  # just for demo

    def perceive(self, query: str):
        print(f"\n📥 Received query: {query}")
        return query

    def reason(self, query: str):
        print("🔎 Searching DuckDuckGo...")
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }

        response = requests.get(url, params=params)
        data = response.json()

        answer = data.get("Answer") or data.get("AbstractText") or "No answer found."
        link = data.get("AbstractURL")
        return answer, link

    def act(self, answer: str, link: Optional[str]):
        print("🧠 Agent says:", answer)
        if link:
            print("🔗 Learn more:", link)

    def update_memory(self, query, answer):
        self.memory.append({"q": query, "a": answer})

    def run(self):
        print("🤖 Agent Ready! Ask anything.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Agent shutting down.")
                break

            query = self.perceive(user_input)
            answer, link = self.reason(query)
            self.act(answer, link)
            self.update_memory(query, answer)
            time.sleep(1)  # just to simulate processing

# Run it
if __name__ == "__main__":
    agent = SimpleSearchAgent()
    agent.run()
