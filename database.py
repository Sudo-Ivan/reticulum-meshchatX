from datetime import datetime, timezone

from peewee import *  # noqa: F403
from playhouse.migrate import SqliteMigrator
from playhouse.migrate import migrate as migrate_database

latest_version = 6  # increment each time new database migrations are added
database = (
    DatabaseProxy()  # noqa: F405
)  # use a proxy object, as we will init real db client inside meshchat.py
migrator = SqliteMigrator(database)


# migrates the database
def migrate(current_version):
    # migrate to version 2
    if current_version < 2:
        migrate_database(
            migrator.add_column(
                "lxmf_messages",
                "delivery_attempts",
                LxmfMessage.delivery_attempts,
            ),
            migrator.add_column(
                "lxmf_messages",
                "next_delivery_attempt_at",
                LxmfMessage.next_delivery_attempt_at,
            ),
        )

    # migrate to version 3
    if current_version < 3:
        migrate_database(
            migrator.add_column("lxmf_messages", "rssi", LxmfMessage.rssi),
            migrator.add_column("lxmf_messages", "snr", LxmfMessage.snr),
            migrator.add_column("lxmf_messages", "quality", LxmfMessage.quality),
        )

    # migrate to version 4
    if current_version < 4:
        migrate_database(
            migrator.add_column("lxmf_messages", "method", LxmfMessage.method),
        )

    # migrate to version 5
    if current_version < 5:
        migrate_database(
            migrator.add_column("announces", "rssi", Announce.rssi),
            migrator.add_column("announces", "snr", Announce.snr),
            migrator.add_column("announces", "quality", Announce.quality),
        )

    # migrate to version 6
    if current_version < 6:
        migrate_database(
            migrator.add_column("lxmf_messages", "is_spam", LxmfMessage.is_spam),
        )

    return latest_version


class BaseModel(Model):  # noqa: F405
    class Meta:
        database = database


class Config(BaseModel):
    id = BigAutoField()  # noqa: F405
    key = CharField(unique=True)  # noqa: F405
    value = TextField()  # noqa: F405
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "config"


class Announce(BaseModel):
    id = BigAutoField()  # noqa: F405
    destination_hash = CharField(  # noqa: F405
        unique=True,
    )  # unique destination hash that was announced
    aspect = TextField(  # noqa: F405
        index=True,
    )  # aspect is not included in announce, but we want to filter saved announces by aspect
    identity_hash = CharField(  # noqa: F405
        index=True,
    )  # identity hash that announced the destination
    identity_public_key = (
        CharField()  # noqa: F405
    )  # base64 encoded public key, incase we want to recreate the identity manually
    app_data = TextField(null=True)  # noqa: F405  # base64 encoded app data bytes
    rssi = IntegerField(null=True)  # noqa: F405
    snr = FloatField(null=True)  # noqa: F405
    quality = FloatField(null=True)  # noqa: F405

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "announces"


class CustomDestinationDisplayName(BaseModel):
    id = BigAutoField()  # noqa: F405
    destination_hash = CharField(unique=True)  # noqa: F405  # unique destination hash
    display_name = CharField()  # noqa: F405  # custom display name for the destination hash

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "custom_destination_display_names"


class FavouriteDestination(BaseModel):
    id = BigAutoField()  # noqa: F405
    destination_hash = CharField(unique=True)  # noqa: F405  # unique destination hash
    display_name = CharField()  # noqa: F405  # custom display name for the destination hash
    aspect = CharField()  # noqa: F405  # e.g: nomadnetwork.node

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "favourite_destinations"


class LxmfMessage(BaseModel):
    id = BigAutoField()  # noqa: F405
    hash = CharField(unique=True)  # noqa: F405  # unique lxmf message hash
    source_hash = CharField(index=True)  # noqa: F405
    destination_hash = CharField(index=True)  # noqa: F405
    state = (
        CharField()  # noqa: F405
    )  # state is converted from internal int to a human friendly string
    progress = FloatField()  # noqa: F405  # progress is converted from internal float 0.00-1.00 to float between 0.00/100 (2 decimal places)
    is_incoming = BooleanField()  # noqa: F405  # if true, we should ignore state, it's set to draft by default on incoming messages
    method = CharField(  # noqa: F405
        null=True,
    )  # what method is being used to send the message, e.g: direct, propagated
    delivery_attempts = IntegerField(  # noqa: F405
        default=0,
    )  # how many times delivery has been attempted for this message
    next_delivery_attempt_at = FloatField(  # noqa: F405
        null=True,
    )  # timestamp of when the message will attempt delivery again
    title = TextField()  # noqa: F405
    content = TextField()  # noqa: F405
    fields = TextField()  # noqa: F405  # json string
    timestamp = (
        FloatField()  # noqa: F405
    )  # timestamp of when the message was originally created (before ever being sent)
    rssi = IntegerField(null=True)  # noqa: F405
    snr = FloatField(null=True)  # noqa: F405
    quality = FloatField(null=True)  # noqa: F405
    is_spam = BooleanField(default=False)  # noqa: F405  # if true, message is marked as spam
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "lxmf_messages"


class LxmfConversationReadState(BaseModel):
    id = BigAutoField()  # noqa: F405
    destination_hash = CharField(unique=True)  # noqa: F405  # unique destination hash
    last_read_at = DateTimeField()  # noqa: F405

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "lxmf_conversation_read_state"


class LxmfUserIcon(BaseModel):
    id = BigAutoField()  # noqa: F405
    destination_hash = CharField(unique=True)  # noqa: F405  # unique destination hash
    icon_name = CharField()  # noqa: F405  # material design icon name for the destination hash
    foreground_colour = CharField()  # noqa: F405  # hex colour to use for foreground (icon colour)
    background_colour = (
        CharField()  # noqa: F405
    )  # hex colour to use for background (background colour)

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "lxmf_user_icons"


class BlockedDestination(BaseModel):
    id = BigAutoField()  # noqa: F405
    destination_hash = CharField(  # noqa: F405
        unique=True,
        index=True,
    )  # unique destination hash that is blocked
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "blocked_destinations"


class SpamKeyword(BaseModel):
    id = BigAutoField()  # noqa: F405
    keyword = CharField(  # noqa: F405
        unique=True,
        index=True,
    )  # keyword to match against message content
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))  # noqa: F405

    # define table name
    class Meta:
        table_name = "spam_keywords"
