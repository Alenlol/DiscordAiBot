import discord


def channel_name(given_name):
    def channel_decorator(func):
        def wrapper(*args):
            print("Done")
            new = not_found()
            if type(args[1].channel) == discord.channel.TextChannel:
                if args[1].channel.name == given_name:
                    new = func(*args)
            return new
        return wrapper
    return channel_decorator


def not_found():
    return "Channel isn't found"


if __name__ == '__main__':
    print()
