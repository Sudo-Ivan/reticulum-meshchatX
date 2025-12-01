import asyncio
import time

import RNS

# TODO optionally identity self over link
# TODO allowlist/denylist for incoming calls


class CallFailedException(Exception):
    pass


class AudioCall:
    def __init__(self, link: RNS.Link, is_outbound: bool):
        self.link = link
        self.is_outbound = is_outbound
        self.link.set_link_closed_callback(self.on_link_closed)
        self.link.set_packet_callback(self.on_packet)
        self.audio_packet_listeners = []
        self.hangup_listeners = []

    def register_audio_packet_listener(self, callback):
        self.audio_packet_listeners.append(callback)

    def unregister_audio_packet_listener(self, callback):
        self.audio_packet_listeners.remove(callback)

    def register_hangup_listener(self, callback):
        self.hangup_listeners.append(callback)

    # handle link being closed
    def on_link_closed(self, link):
        print("[AudioCall] on_link_closed")

        # call all hangup listeners
        for hangup_listener in self.hangup_listeners:
            hangup_listener()

    # handle packet received over link
    def on_packet(self, message, packet):
        # send audio received from call initiator to all audio packet listeners
        for audio_packet_listener in self.audio_packet_listeners:
            audio_packet_listener(message)

    # send an audio packet over the link
    def send_audio_packet(self, data):
        # do nothing if link is not active
        if self.is_active() is False:
            return

        # drop audio packet if it is too big to send
        if len(data) > RNS.Link.MDU:
            print(
                "[AudioCall] dropping audio packet "
                + str(len(data))
                + " bytes exceeds the link packet MDU of "
                + str(RNS.Link.MDU)
                + " bytes",
            )
            return

        # send codec2 audio received from call receiver to call initiator over reticulum link
        RNS.Packet(self.link, data).send()

    # gets the identity of the other person, or returns None if they did not identify
    def get_remote_identity(self):
        return self.link.get_remote_identity()

    # determine if this call is still active
    def is_active(self):
        return self.link.status == RNS.Link.ACTIVE

    # handle hanging up the call
    def hangup(self):
        print("[AudioCall] hangup")
        self.link.teardown()


class AudioCallManager:
    def __init__(self, identity: RNS.Identity, is_destination_blocked_callback=None):
        self.identity = identity
        self.on_incoming_call_callback = None
        self.on_outgoing_call_callback = None
        self.is_destination_blocked_callback = is_destination_blocked_callback
        self.audio_call_receiver = AudioCallReceiver(manager=self)

        # remember audio calls
        self.audio_calls: list[AudioCall] = []

    # announces the audio call destination
    def announce(self, app_data=None):
        self.audio_call_receiver.destination.announce(app_data)
        print(
            "[AudioCallManager] announced destination: "
            + RNS.prettyhexrep(self.audio_call_receiver.destination.hash),
        )

    # set the callback for incoming calls
    def register_incoming_call_callback(self, callback):
        self.on_incoming_call_callback = callback

    # set the callback for outgoing calls
    def register_outgoing_call_callback(self, callback):
        self.on_outgoing_call_callback = callback

    # handle incoming calls from audio call receiver
    def handle_incoming_call(self, audio_call: AudioCall):
        # remember it
        self.audio_calls.append(audio_call)

        # fire callback
        if self.on_incoming_call_callback is not None:
            self.on_incoming_call_callback(audio_call)

    # handle outgoing calls
    def handle_outgoing_call(self, audio_call: AudioCall):
        # remember it
        self.audio_calls.append(audio_call)

        # fire callback
        if self.on_outgoing_call_callback is not None:
            self.on_outgoing_call_callback(audio_call)

    # find an existing audio call from the provided link hash
    def find_audio_call_by_link_hash(self, link_hash: bytes):
        for audio_call in self.audio_calls:
            if audio_call.link.hash == link_hash:
                return audio_call
        return None

    # delete an existing audio call from the provided link hash
    def delete_audio_call_by_link_hash(self, link_hash: bytes):
        audio_call = self.find_audio_call_by_link_hash(link_hash)
        if audio_call is not None:
            self.delete_audio_call(audio_call)

    # delete an existing audio call
    def delete_audio_call(self, audio_call: AudioCall):
        self.audio_calls.remove(audio_call)

    # hangup all calls
    def hangup_all(self):
        for audio_call in self.audio_calls:
            audio_call.hangup()

    # attempts to initiate a call to the provided destination and returns the link hash on success
    async def initiate(
        self, destination_hash: bytes, timeout_seconds: int = 15,
    ) -> AudioCall:
        # determine when to timeout
        timeout_after_seconds = time.time() + timeout_seconds

        # check if we have a path to the destination
        if not RNS.Transport.has_path(destination_hash):
            # we don't have a path, so we need to request it
            RNS.Transport.request_path(destination_hash)

            # wait until we have a path, or give up after the configured timeout
            while (
                not RNS.Transport.has_path(destination_hash)
                and time.time() < timeout_after_seconds
            ):
                await asyncio.sleep(0.1)

        # if we still don't have a path, we can't establish a link, so bail out
        if not RNS.Transport.has_path(destination_hash):
            raise CallFailedException("Could not find path to destination.")

        # create outbound destination to initiate audio calls
        server_identity = RNS.Identity.recall(destination_hash)
        server_destination = RNS.Destination(
            server_identity,
            RNS.Destination.OUT,
            RNS.Destination.SINGLE,
            "call",
            "audio",
        )

        # create link
        link = RNS.Link(server_destination)

        # wait until we have established a link, or give up after the configured timeout
        while (
            link.status is not RNS.Link.ACTIVE and time.time() < timeout_after_seconds
        ):
            await asyncio.sleep(0.1)

        # if we still haven't established a link, bail out
        if link.status is not RNS.Link.ACTIVE:
            raise CallFailedException("Could not establish link to destination.")

        # link is now established, create audio call
        audio_call = AudioCall(link, is_outbound=True)

        # handle new outgoing call
        self.handle_outgoing_call(audio_call)

        # TODO: this can be optional, it's only being sent by default for ui, can be removed
        link.identify(self.identity)

        return audio_call


class AudioCallReceiver:
    def __init__(self, manager: AudioCallManager):
        self.manager = manager

        # create destination for receiving audio calls
        self.destination = RNS.Destination(
            self.manager.identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            "call",
            "audio",
        )

        # register link state callbacks
        self.destination.set_link_established_callback(self.client_connected)

    # find an existing audio call from the provided link
    def find_audio_call_by_link_hash(self, link_hash: bytes):
        for audio_call in self.manager.audio_calls:
            if audio_call.link.hash == link_hash:
                return audio_call
        return None

    # client connected to us, set up an audio call instance
    def client_connected(self, link: RNS.Link):
        # check if source is blocked
        if self.manager.is_destination_blocked_callback is not None:
            try:
                # try to get remote identity hash
                remote_identity = link.get_remote_identity()
                if remote_identity is not None:
                    source_hash = remote_identity.hash.hex()
                    if self.manager.is_destination_blocked_callback(source_hash):
                        print(
                            f"Rejecting audio call from blocked source: {source_hash}",
                        )
                        link.teardown()
                        return
            except Exception:  # noqa: E722
                # if we can't get identity yet, we'll check later
                pass

        # TODO: this can be optional, it's only being sent by default for ui, can be removed
        link.identify(self.manager.identity)

        # create audio call
        audio_call = AudioCall(link, is_outbound=False)

        # pass to manager
        self.manager.handle_incoming_call(audio_call)
