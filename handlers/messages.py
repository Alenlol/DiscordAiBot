import discord, sys
from discord.ext import commands

sys.path.append(".")
from Ai import coolAiThings
    
class Messages(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.hello = self.get_h()
        # extracting data from file once

    @staticmethod
    def get_h():
        hello = 0
        with open("Data/data.txt", 'r') as file:
            hello = int(file.read())
        return hello


    #@client.event
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.channel.name == "ai-chat-bot" or message.channel.name == "ai-text-bot":
            chat_response = ""
            try:
                async with message.channel.typing():
                    getmessage = message.content
                    if message.channel.name == "ai-chat-bot":
                        chat_response = coolAiThings.aiMessageChat(getmessage)
                    else:
                        chat_response = coolAiThings.aiGenerateText(getmessage)
                    print(f"{message.author} : {getmessage}, \n\nBing response : {chat_response}\n")
                    if chat_response is None:
                        await message.reply("Your message was censored, due to the Palm politics.")
                    else:
                        await message.reply(chat_response)
            except Exception as e:
                print(e)
                await message.reply("400 Bad request")

        if message.channel.name == "testbot":
            n = ("hello")
            count = {'0' : '0️⃣', '1' : '1️⃣', '2' : '2️⃣', '3' : '3️⃣', '4' : '4️⃣', '5' : '5️⃣',
                      '6' : '6️⃣', '7' : '7️⃣', '8' : '8️⃣', '9' : '9️⃣'}
            if message.content.strip().lower() in n:
                emoji = ("🤚")
                await message.add_reaction(emoji[0])
                self.hello += 1

                for item in str(self.hello):
                        if item in count:
                            await message.add_reaction(count[item])

                with open("Data/data.txt", 'w') as file:
                    file.write(f"{self.hello}")

async def setup(client):
    await client.add_cog(Messages(client))

if __name__ == '__main__':

    print(Messages.hello)