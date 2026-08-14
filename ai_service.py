import os
import requests

def generate_ai_response(user_input: str) -> str:
    """
    Calls an OpenAI-compatible chat API.
    API key is read only from the environment.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")

    url = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    prompt = f"""You are StaySense AI, an assistant for homestay owners.
Analyze the following guest review and give:
1. Sentiment
2. Main theme
3. Short actionable summary
4. Suggested host response

Guest review:
{user_input}
"""

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You analyze hospitality guest feedback clearly and briefly."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.4,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
