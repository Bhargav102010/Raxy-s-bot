import telebot
import requests
import re
from typing import Tuple, Optional

# Initialize the bot with your token
bot = telebot.TeleBot("7443679602:AAGvU3GH30Uf5bh0RXbXhRBYMyeAVb8TF2Y")

def generate(prompt: str, system_prompt: str = "Don't Write Code unless Mentioned", web_access: bool = True, stream: bool = True) -> Tuple[Optional[str], str]:
    """
    Generates a response for the given prompt using the Blackbox.ai API.

    Parameters:
    - prompt (str): The prompt to generate a response for.
    - system_prompt (str): The system prompt to be used in the conversation. Defaults to "Don't Write Code unless Mentioned".
    - web_access (bool): A flag indicating whether to access web resources during the conversation. Defaults to True.
    - stream (bool): A flag indicating whether to print the conversation messages. Defaults to True.

    Returns:
    - Tuple[Optional[str], str]: A tuple containing the sources of the conversation (if available) and the complete response generated.
    """

    chat_endpoint = "https://www.blackbox.ai/api/chat"

    payload = {
        "messages": [{"content": system_prompt, "role": "system"}, {"content": prompt, "role": "user"}],
        "agentMode": {},
        "trendingAgentMode": {},
    }
    
    if web_access:
        payload["codeModelMode"] = web_access

    response = requests.post(chat_endpoint, json=payload, stream=True)

    sources = None
    resp = ""

    for text_stream in response.iter_lines(decode_unicode=True, delimiter="\n"):
        if text_stream:
            if sources is None: 
                sources = text_stream
            else:
                if stream: 
                    print(text_stream)
                resp += text_stream + "\n"

    if sources and stream: 
        print(re.sub(r'\$@\$\w+=v\d+\.\d+\$@\$', '', sources))
        
    return sources, resp

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    sources, resp = generate(query, web_access=False, stream=False)
    bot.reply_to(message, resp if resp else "Sorry, I couldn't generate a response.")

# Start polling for messages
bot.polling()
