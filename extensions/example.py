from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def example(self, ctx, *args):
        """
        Example command

        What it does
        """

        await ctx.send(" ".join(args))


async def setup(client):
    await client.add_cog(Example(client))