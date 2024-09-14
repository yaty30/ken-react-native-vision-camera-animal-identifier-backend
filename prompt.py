from poe_api_wrapper import PoeApi
import json

class Chat:
    tokens = {
        'p-b': 'Kvhj2VuR9aRlrKqxNQfz_g%3D%3D',
        'p-lat': 'HQ15CSgnFxi7TzDY%2Bhbi0GXDJky6FFag1AkFP5bvCw%3D%3D',
    }

    chat_code = "3l4bv0fjv14ryhzrk1a"
    bot = "KenObjectIdentifier"
    client = PoeApi(tokens=tokens)
    
    def Send(self, message):
        for chunk in self.client.send_message(bot=self.bot, message=message, chatCode=self.chat_code):
            pass
        return chunk["text"]
