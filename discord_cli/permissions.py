from inspect import iscoroutinefunction
import discord_cli.exceptions as exceptions

class Base_Permission(object):
    def __init__(self):
        if self.__class__ == Base_Permission:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Base_Permission')
    def __and__(self, other):
        return And_Permission_Operator(self, other)
    def __or__(self, other):
        return Or_Permission_Operator(self, other)
    async def evaluate(client, message):
        raise NotImplementedError('Cannot run evaluate on base permission class')

class Permission_Operator(Base_Permission):
    def __init__(self, perm1, perm2):
        if self.__class__ == Permission_Operator:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Permission_Operator')

        super(Permission_Operator, self).__init__()

        if not isinstance(perm1, Base_Permission):
            raise exceptions.Type_Error('Permission operator perm1 expected Base_Permission instance, {} found'.format(perm1.__class__.__name__))
        if not isinstance(perm2, Base_Permission):
            raise exceptions.Type_Error('Permission operator perm2 expected Base_Permission instance, {} found'.format(perm1.__class__.__name__))

        self._perm1 = perm1
        self._perm2 = perm2

class And_Permission_Operator(Permission_Operator):
    def __init__(self, perm1, perm2):
        super(And_Permission_Operator, self).__init__(perm1, perm2)
    async def evaluate(self, client, message):
        return await self._perm1.evaluate(client, message) and await self._perm2.evaluate(client, message)
    def __str__(self):
        left_str = str(self._perm1)
        right_str = str(self._perm2)
        if isinstance(self._perm1, Permission_Operator):
            left_str = '(' + left_str + ')'
        if isinstance(self._perm2, Permission_Operator):
            right_str = '(' + right_str + ')'
        return left_str + ' and ' + right_str

class Or_Permission_Operator(Permission_Operator):
    def __init__(self, perm1, perm2):
        super(Or_Permission_Operator, self).__init__(perm1, perm2)
    async def evaluate(self, client, message):
        return await self._perm1.evaluate(client, message) or await self._perm2.evaluate(client, message)
    def __str__(self):
        left_str = str(self._perm1)
        right_str = str(self._perm2)
        if isinstance(self._perm1, Permission_Operator):
            left_str = '(' + left_str + ')'
        if isinstance(self._perm2, Permission_Operator):
            right_str = '(' + right_str + ')'
        return left_str + ' or ' + right_str

class Permission_Operand(Base_Permission):
    def __init__(self):
        if self.__class__ == Permission_Operand:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Permission_Operand')
        super(Permission_Operand, self).__init__()

class User_Permission(Permission_Operand):
    def __init__(self, user_id):
        super(User_Permission, self).__init__()
        self._user_id = user_id
    async def evaluate(self, client, message):
        return message.author.id == self._user_id
    def __str__(self):
        return 'user:{}'.format(self._user_id)

class Guild_Permission(Permission_Operand):
    def __init__(self, guild_id):
        super(Guild_Permission, self).__init__()
        self._guild_id = guild_id
    async def evaluate(self, client, message):
        return message.guild.id == self._guild_id
    def __str__(self):
        return 'guild:{}'.format(self._guild_id)

class Custom_Permission(Permission_Operand):
    def __init__(self, permission_function):
        super(Custom_Permission, self).__init__()
        if not iscoroutinefunction(permission_function):
            raise exceptions.Not_Async_Function_Error('Custom permission function must be an async function')
        self._permission_function = permission_function
    async def evaluate(self, client, message):
        return await self._permission_function(client, message)
    def __str__(self):
        return 'custom'

class Discord_Permission(Permission_Operand):
    def __init__(self):
        if self.__class__ == Discord_Permission:
            raise exceptions.Cannot_Create_Instance_Of_Base_Class_Error('Cannot create instance of Discord_Permission')
        super(Discord_Permission, self).__init__()

class Create_Instant_Invite(Discord_Permission):
    def __init__(self):
        super(Create_Instant_Invite, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).create_instant_invite
    def __str__(self):
        return 'create_instant_invite'

class Kick_Members(Discord_Permission):
    def __init__(self):
        super(Kick_Members, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).kick_members
    def __str__(self):
        return 'kick_members'

class Ban_Members(Discord_Permission):
    def __init__(self):
        super(Ban_Members, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).ban_members
    def __str__(self):
        return 'ban_members'

class Administrator(Discord_Permission):
    def __init__(self):
        super(Administrator, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).administrator
    def __str__(self):
        return 'administrator'

class Manage_Channels(Discord_Permission):
    def __init__(self):
        super(Manage_Channels, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_channels
    def __str__(self):
        return 'manage_channels'

class Manage_Guild(Discord_Permission):
    def __init__(self):
        super(Manage_Guild, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_guild
    def __str__(self):
        return 'manage_guild'

class Add_Reactions(Discord_Permission):
    def __init__(self):
        super(Add_Reactions, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).add_reactions
    def __str__(self):
        return 'add_reactions'

class View_Audit_Log(Discord_Permission):
    def __init__(self):
        super(View_Audit_Log, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).view_audit_log
    def __str__(self):
        return 'view_audit_log'

class Read_Messages(Discord_Permission):
    def __init__(self):
        super(Read_Messages, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).read_messages
    def __str__(self):
        return 'read_messages'

class Send_Messages(Discord_Permission):
    def __init__(self):
        super(Send_Messages, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).send_messages
    def __str__(self):
        return 'send_messages'

class Send_TTS_Messages(Discord_Permission):
    def __init__(self):
        super(Send_TTS_Messages, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).send_tts_messages
    def __str__(self):
        return 'send_tts_messages'

class Manage_Messages(Discord_Permission):
    def __init__(self):
        super(Manage_Messages, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_messages
    def __str__(self):
        return 'manage_messages'

class Embed_Links(Discord_Permission):
    def __init__(self):
        super(Embed_Links, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).embed_links
    def __str__(self):
        return 'embed_links'

class Attach_Files(Discord_Permission):
    def __init__(self):
        super(Attach_Files, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).attach_files
    def __str__(self):
        return 'attach_files'

class Read_Message_History(Discord_Permission):
    def __init__(self):
        super(Read_Message_History, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).read_message_history
    def __str__(self):
        return 'read_message_history'

class Mention_Everyone(Discord_Permission):
    def __init__(self):
        super(Mention_Everyone, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).mention_everyone
    def __str__(self):
        return 'mention_everyone'

class External_Emojis(Discord_Permission):
    def __init__(self):
        super(External_Emojis, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).external_emojis
    def __str__(self):
        return 'external_emojis'

class Change_Nickname(Discord_Permission):
    def __init__(self):
        super(Change_Nickname, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).change_nickname
    def __str__(self):
        return 'change_nickname'

class Manage_Nicknames(Discord_Permission):
    def __init__(self):
        super(Manage_Nicknames, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_nicknames
    def __str__(self):
        return 'manage_nicknames'

class Manage_Roles(Discord_Permission):
    def __init__(self):
        super(Manage_Roles, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_roles
    def __str__(self):
        return 'manage_roles'

class Manage_Webhooks(Discord_Permission):
    def __init__(self):
        super(Manage_Webhooks, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_webhooks
    def __str__(self):
        return 'manage_webhooks'

class Manage_Emojis(Discord_Permission):
    def __init__(self):
        super(Manage_Emojis, self).__init__()
    async def evaluate(self, client, message):
        return message.author.permissions_in(message.channel).manage_emojis
    def __str__(self):
        return 'manage_emojis'