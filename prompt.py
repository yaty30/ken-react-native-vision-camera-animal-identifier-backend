from poe_api_wrapper import PoeApi
import asyncio
import json

class Chat:
    tokens = {
        'p-b': 'Kvhj2VuR9aRlrKqxNQfz_g%3D%3D',
        'p-lat': 'HQ15CSgnFxi7TzDY%2Bhbi0GXDJky6FFag1AkFP5bvCw%3D%3D',
    }

    chat_code = "3lzvuof9za1nx4xoad7"
    bot = "KenObjectIdentifier"
    client = PoeApi("Kvhj2VuR9aRlrKqxNQfz_g%3D%3D")

    def send(self, message):
        try:
            response = None
            for chunk in self.client.send_message(bot=self.bot, message=message, chatCode=self.chat_code):
                response = chunk
            
            if response and "text" in response:
                return response["text"]
            else:
                return "No response received or invalid format."
        
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    chat = Chat()
    response = chat.send("Hello, how are you?")
    print(response)