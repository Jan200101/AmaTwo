from discord import Member, Embed
from discord.ext import commands


class Mod:
    """
    Moderation commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: Member, reason: str="No reason given"):
        """
        Kicks a specified member
        """
        if ctx.message.author == member:
            await ctx.send(":x: You can't kick yourself")
        elif self.bot.admin_role in member.roles:
            await ctx.send(":x: You can't kick a Administrator")
        elif self.bot.mod_role in member.roles and not self.bot.admin_role in ctx.message.author.roles:
            await ctx.send(":x: You can't kick a Moderator")
        else:
            await member.kick(reason=reason)
            embed = Embed(title="Member kicked by {}".format(ctx.message.author.name),
                          description="Name: {0.name}\nID: {0.id}".format(member), color=0xFFF110)
            embed.set_thumbnail(url=member.avatar_url)
            await self.bot.log_channel.send(embed=embed)
            await ctx.send(':white_check_mark: Kicked user successfully!')

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: Member, reason: str="No reason given"):
        """
        Bans a specified member.
        """
        if ctx.message.author == member:
            await ctx.send(':x: You can\'t ban yourself!')
        elif self.bot.admin_role in member.roles:
            await ctx.send(":x: You can't ban a Administrator")
        elif self.bot.mod_role in member.roles and not self.bot.admin_role in ctx.message.author.roles:
            await ctx.send(":x: You can't ban a Moderator")
        else:
            await member.ban(reason=reason)
            embed = Embed(title="Member banned by {}".format(ctx.message.author.name),
                          description="Name: {0.name}\nID: {0.id}".format(member), color=0xFF9710)
            embed.set_thumbnail(url=member.avatar_url)
            await self.bot.log_channel.send(embed=embed)
            await ctx.send(':hammer: Banned user successfully!')


def setup(bot):
    bot.add_cog(Mod(bot))
