import requests

def ask_duckduckgo(question):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": question,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Try to fetch the answer from Instant Answer or Abstract
    answer = data.get("Answer") or data.get("AbstractText") or "No instant answer found."
    source = data.get("AbstractURL")

    return answer, source

if __name__ == "__main__":
    print("🤖 DuckDuck Agent Ready! Ask your question.")
    while True:
        query = input("\nAsk me (or type 'exit'): ")
        if query.lower() in ["exit", "quit"]:
            break

        answer, source = ask_duckduckgo(query)
        print("\n🧠 Answer:", answer)
        if source:
            print("🔗 Source:", source)
