import os
import time
from typing import Dict, List

import openai
import requests
from dotenv import load_dotenv
from twilio.rest import Client


# ===================================
# 1. TwitterAgent: Retrieve tweets
# ===================================
class TwitterAgent:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"
        # Use a memory set for deduplication of tweet IDs
        self.already_seen = set()

    def get_latest_tweets(self, query: str, max_results=10) -> List[Dict]:
        """
        query example: '(from:elonmusk OR from:realdonaldtrump) -is:retweet'
        max_results can be up to 100 for the Twitter API v2
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "author_id,created_at"
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            tweets = data.get("data", [])
            new_tweets = []
            for tweet in tweets:
                if tweet["id"] not in self.already_seen:
                    self.already_seen.add(tweet["id"])
                    new_tweets.append(tweet)

            return new_tweets

        except requests.exceptions.RequestException as e:
            print(f"Error fetching tweets: {e}")
            return []

# ===================================
# 2. AnalysisAgent: Sentiment, Crypto presence
# ===================================
class AnalysisAgent:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key

    def analyze_tweet(self, tweet_text: str) -> Dict:
        """
        Use OpenAI to analyze sentiment and look for crypto presence or announcements.
        Returns a dictionary with sentiment, any crypto mentions, etc.
        """

        # 1. Basic sentiment analysis using OpenAI
        messages = [
            {"role": "system", "content": "You are a highly accurate sentiment analysis engine."},
            {"role": "user", "content": (
                "Determine the sentiment (Positive, Negative, or Neutral) of the following Tweet. "
                "Then check if it mentions cryptocurrencies. If yes, which ones and how are they mentioned?\n\n"
                f"Tweet: {tweet_text}\n"
            )}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.0,
                max_tokens=100
            )

            analysis = response.choices[0].message['content'].strip()
            # The analysis could be in plain text; you might parse it further or use ChatCompletion with a structured schema

            return {"analysis": analysis}

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return {"analysis": "Error", "error": str(e)}


# ===================================
# 3. DecisionAgent: Decides next action
# ===================================
class DecisionAgent:
    """
    Takes analyses and decides whether to message, and how big the impact is.
    Expand logic as needed.
    """
    def decide(self, tweet_text: str, analysis: Dict) -> Dict:
        """
        For now, let's do a simple check if there's mention of crypto or if sentiment is strongly
        negative/positive to define a 'possible scenario'.
        """
        analysis_text = analysis.get("analysis", "")
        # Basic heuristics you can refine
        is_crypto_mentioned = "crypto" in analysis_text.lower() or "bitcoin" in analysis_text.lower() or "ethereum" in analysis_text.lower()
        if "Positive" in analysis_text:
            scenario = "Likely bullish sentiment."
        elif "Negative" in analysis_text:
            scenario = "Likely bearish sentiment."
        else:
            scenario = "No strong sentiment."

        if is_crypto_mentioned:
            scenario += " Crypto mention detected."

        return {
            "tweet": tweet_text,
            "analysis_text": analysis_text,
            "scenario": scenario
        }

# ===================================
# 4. WhatsApp messenger
# ===================================
class WhatsAppMessenger:
    def __init__(self, account_sid: str, auth_token: str, from_whatsapp: str, to_whatsapp: str):
        self.client = Client(account_sid, auth_token)
        self.from_whatsapp = f"whatsapp:{from_whatsapp}"
        self.to_whatsapp = f"whatsapp:{to_whatsapp}"

    def send_message(self, body: str):
        try:
            message = self.client.messages.create(
                body=body,
                from_=self.from_whatsapp,
                to=self.to_whatsapp
            )
            print(f"Sent WhatsApp message SID: {message.sid}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")

# ===================================
# Main script logic
# ===================================
def main():
    # Load environment variables from a .env file
    load_dotenv()
    
    # Get environment variables (set in GitHub Actions or locally via .env)
    twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM")
    whatsapp_to = os.getenv("WHATSAPP_TO")

    # Initialize agents
    twitter_agent = TwitterAgent(bearer_token=twitter_bearer_token)
    analysis_agent = AnalysisAgent(openai_api_key=openai_api_key)
    decision_agent = DecisionAgent()
    messenger = WhatsAppMessenger(
        account_sid=twilio_account_sid,
        auth_token=twilio_auth_token,
        from_whatsapp=twilio_whatsapp_from,
        to_whatsapp=whatsapp_to
    )

    # message_body = "Hello from the Crypto Sentiment Analysis bot!"
    # messenger.send_message(message_body)

    # print(analysis_agent.analyze_tweet("I love Bitcoin and Ethereum!"))
    # return

    # Build a search query for multiple influential figures
    # Example includes Elon Musk and Donald Trump
    # For more people, just add: (from:person1 OR from:person2 OR ...)
    query = "(from:elonmusk OR from:realdonaldtrump) -is:retweet"

    # 1) Retrieve tweets
    new_tweets = twitter_agent.get_latest_tweets(query=query, max_results=10)

    # 2) Analyze each tweet
    for tweet in new_tweets:
        tweet_text = tweet["text"]
        
        analysis_result = analysis_agent.analyze_tweet(tweet_text)
        decision = decision_agent.decide(tweet_text, analysis_result)

        # Construct message body
        message_body = (
            f"New Tweet found:\n"
            f"Tweet: {decision['tweet']}\n\n"
            f"Analysis: {decision['analysis_text']}\n\n"
            f"Scenario: {decision['scenario']}"
        )

        # 3) Send message via WhatsApp
        messenger.send_message(message_body)

    print("Analysis complete.")

if __name__ == "__main__":
    main()
