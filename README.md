# Crypto Sentiment Analysis Bot

This project is a Crypto Sentiment Analysis Bot that retrieves tweets from influential figures, analyzes their sentiment and crypto mentions using OpenAI's GPT-4o-mini model, and sends notifications via WhatsApp using Twilio.

## Features

1. **TwitterAgent**: Retrieves the latest tweets from specified influential figures.
2. **AnalysisAgent**: Analyzes the sentiment of tweets and checks for mentions of cryptocurrencies using OpenAI's GPT-4o-mini model.
3. **DecisionAgent**: Decides the next action based on the analysis, determining the sentiment and presence of crypto mentions.
4. **WhatsAppMessenger**: Sends notifications via WhatsApp using Twilio's API.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/crypto-sentiment-analysis-bot.git
    cd crypto-sentiment-analysis-bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a [.env](http://_vscodecontentref_/0) file in the root directory and add your environment variables:
    ```env
    TWITTER_BEARER_TOKEN=your_twitter_bearer_token
    OPENAI_API_KEY=your_openai_api_key
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_WHATSAPP_FROM=your_twilio_whatsapp_from_number
    WHATSAPP_TO=recipient_whatsapp_number
    ```

## Usage

1. Run the main script:
    ```sh
    python crypto_sentiment_analysis.py
    ```

2. The bot will:
    - Retrieve the latest tweets from specified influential figures.
    - Analyze the sentiment and crypto mentions in the tweets.
    - Decide the next action based on the analysis.
    - Send notifications via WhatsApp.

## Example

The bot searches for tweets from Elon Musk and Donald Trump, analyzes their sentiment and crypto mentions, and sends a WhatsApp message with the analysis and scenario.

## Contributing

Feel free to submit issues, fork the repository and send pull requests!

## License

This project is licensed under the MIT License.