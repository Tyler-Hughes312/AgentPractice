import os
import autogen

def get_autogen_assistant():
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    config_list = [
        {
            "model": "claude-3-opus-20240229",
            "api_key": anthropic_api_key,
            "api_type": "anthropic"
        }
    ]
    anthropic_llm_config = {
        "config_list": config_list,
        "temperature": 0.3,
    }
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=anthropic_llm_config,
        system_message="You are a helpful assistant that can answer questions and help with tasks."
    )
    return assistant

def rate_headlines_with_llm(df, assistant):
    ratings = []
    for headline in df["headline"]:
        prompt = (
            "You are an investor interested in innovation and stock prices. "
            "Rate the following news headline for the company on a scale of 1-10: "
            "1-4 = objectively bad for the company (1 is worst), 5-6 = neutral, 7-10 = good for the company (10 is best). "
            "Only return the number.\nHeadline: " + headline
        )
        response = assistant.generate_reply([{"role": "user", "content": prompt}])
        print(f"Prompt: {prompt}\nResponse: {response}")  # Debug print
        try:
            rating = int(''.join(filter(str.isdigit, str(response))))
        except Exception:
            rating = None
        ratings.append(rating)
    df["popularity_rating"] = ratings
    return df
