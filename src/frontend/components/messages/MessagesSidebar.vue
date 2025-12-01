<template>
    <div class="flex flex-col w-80 min-w-80">

        <!-- tabs -->
        <div class="bg-transparent border-b border-r border-gray-200/70 dark:border-zinc-700/80 backdrop-blur">
            <div class="-mb-px flex">
                <div @click="tab = 'conversations'" class="w-full border-b-2 py-3 px-1 text-center text-sm font-semibold tracking-wide uppercase cursor-pointer transition" :class="[ tab === 'conversations' ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-300' : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 dark:hover:border-zinc-600 hover:text-gray-700 dark:hover:text-gray-200']">Conversations</div>
                <div @click="tab = 'announces'" class="w-full border-b-2 py-3 px-1 text-center text-sm font-semibold tracking-wide uppercase cursor-pointer transition" :class="[ tab === 'announces' ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-300' : 'border-transparent text-gray-500 dark:text-gray-400 hover:border-gray-300 dark:hover:border-zinc-600 hover:text-gray-700 dark:hover:text-gray-200']">Announces</div>
            </div>
        </div>

        <!-- conversations -->
        <div v-if="tab === 'conversations'" class="flex-1 flex flex-col bg-white dark:bg-zinc-950 border-r border-gray-200 dark:border-zinc-700 overflow-hidden min-h-0">

            <!-- search + filters -->
            <div v-if="conversations.length > 0" class="p-1 border-b border-gray-300 dark:border-zinc-700 space-y-2">
                <input
                    :value="conversationSearchTerm"
                    @input="onConversationSearchInput"
                    type="text"
                    :placeholder="`Search ${conversations.length} conversations...`"
                    class="input-field">
                <div class="flex flex-wrap gap-1">
                    <button type="button" @click="toggleFilter('unread')" :class="filterChipClasses(filterUnreadOnly)">Unread</button>
                    <button type="button" @click="toggleFilter('failed')" :class="filterChipClasses(filterFailedOnly)">Failed</button>
                    <button type="button" @click="toggleFilter('attachments')" :class="filterChipClasses(filterHasAttachmentsOnly)">Attachments</button>
                </div>
            </div>

            <!-- conversations -->
            <div class="flex h-full overflow-y-auto">
                <div v-if="displayedConversations.length > 0" class="w-full">
                    <div
                        v-for="conversation of displayedConversations"
                        :key="conversation.destination_hash"
                        @click="onConversationClick(conversation)"
                        class="flex cursor-pointer p-2 border-l-2"
                        :class="[ conversation.destination_hash === selectedDestinationHash ? 'bg-gray-100 dark:bg-zinc-700 border-blue-500 dark:border-blue-400' : 'bg-white dark:bg-zinc-950 border-transparent hover:bg-gray-50 dark:hover:bg-zinc-700 hover:border-gray-200 dark:hover:border-zinc-600' ]">
                        <div class="my-auto mr-2">
                            <div v-if="conversation.lxmf_user_icon" class="p-2 rounded" :style="{ 'color': conversation.lxmf_user_icon.foreground_colour, 'background-color': conversation.lxmf_user_icon.background_colour }">
                                <MaterialDesignIcon :icon-name="conversation.lxmf_user_icon.icon_name" class="w-6 h-6"/>
                            </div>
                            <div v-else class="bg-gray-200 dark:bg-zinc-700 text-gray-500 dark:text-gray-400 p-2 rounded">
                                <MaterialDesignIcon icon-name="account-outline" class="w-6 h-6"/>
                            </div>
                        </div>
                        <div class="mr-auto w-full pr-2">
                            <div class="flex justify-between gap-2">
                                <div class="text-gray-900 dark:text-gray-100 truncate" :title="conversation.custom_display_name ?? conversation.display_name" :class="{ 'font-semibold': conversation.is_unread || conversation.failed_messages_count > 0 }">
                                    {{ conversation.custom_display_name ?? conversation.display_name }}
                                </div>
                                <div class="text-gray-500 dark:text-gray-400 text-xs whitespace-nowrap">
                                    {{ formatTimeAgo(conversation.updated_at) }}
                                </div>
                            </div>
                            <div class="text-gray-600 dark:text-gray-400 text-xs mt-0.5 truncate">
                                {{ conversation.latest_message_preview ?? conversation.latest_message_title ?? 'No messages yet' }}
                            </div>
                        </div>
                        <div class="flex items-center space-x-1">
                            <div v-if="conversation.has_attachments" class="text-gray-500 dark:text-gray-300">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                                    <path d="M15.26 5.01a2.25 2.25 0 0 1 3.182 3.182L11.44 15.195a3 3 0 0 1-4.243-4.243l6.364-6.364a.75.75 0 0 1 1.06 1.06l-6.364 6.364a1.5 1.5 0 1 0 2.121 2.121l6.999-6.998a.75.75 0 0 0-1.06-1.06l-6.364 6.363a.75.75 0 1 1-1.06-1.06Z"/>
                                </svg>
                            </div>
                            <div v-if="conversation.is_unread" class="my-auto ml-1">
                                <div class="bg-blue-500 dark:bg-blue-400 rounded-full p-1"></div>
                            </div>
                            <div v-else-if="conversation.failed_messages_count" class="my-auto ml-1">
                                <div class="bg-red-500 dark:bg-red-400 rounded-full p-1"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="mx-auto my-auto text-center leading-5">

                    <div v-if="isLoading" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1 animate-spin text-gray-500">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                            </svg>
                        </div>
                        <div class="font-semibold">Loading conversations…</div>
                    </div>

                    <!-- no conversations at all -->
                    <div v-else-if="conversations.length === 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 0 1 2.012 1.244l.256.512a2.25 2.25 0 0 0 2.013 1.244h3.218a2.25 2.25 0 0 0 2.013-1.244l.256-.512a2.25 2.25 0 0 1 2.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 0 0-2.15-1.588H6.911a2.25 2.25 0 0 0-2.15 1.588L2.35 13.177a2.25 2.25 0 0 0-.1.661Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Conversations</div>
                        <div>Discover peers on the Announces tab</div>
                    </div>

                    <!-- is searching, but no results -->
                    <div v-else-if="conversationSearchTerm !== ''" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Search Results</div>
                        <div>Your search didn't match any conversations.</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- discover -->
        <div v-if="tab === 'announces'" class="flex-1 flex flex-col bg-white dark:bg-zinc-950 border-r border-gray-200 dark:border-zinc-700 overflow-hidden min-h-0">

            <!-- search -->
            <div v-if="peersCount > 0" class="p-1 border-b border-gray-300 dark:border-zinc-700">
                <input v-model="peersSearchTerm" type="text" :placeholder="`Search ${peersCount} recent announces...`" class="input-field">
            </div>

            <!-- peers -->
            <div class="flex h-full overflow-y-auto">
                <div v-if="searchedPeers.length > 0" class="w-full">
                    <div @click="onPeerClick(peer)" v-for="peer of searchedPeers" class="flex cursor-pointer p-2 border-l-2" :class="[ peer.destination_hash === selectedDestinationHash ? 'bg-gray-100 dark:bg-zinc-700 border-blue-500 dark:border-blue-400' : 'bg-white dark:bg-zinc-950 border-transparent hover:bg-gray-50 dark:hover:bg-zinc-700 hover:border-gray-200 dark:hover:border-zinc-600' ]">
                        <div class="my-auto mr-2">
                            <div v-if="peer.lxmf_user_icon" class="p-2 rounded" :style="{ 'color': peer.lxmf_user_icon.foreground_colour, 'background-color': peer.lxmf_user_icon.background_colour }">
                                <MaterialDesignIcon :icon-name="peer.lxmf_user_icon.icon_name" class="w-6 h-6"/>
                            </div>
                            <div v-else class="bg-gray-200 dark:bg-zinc-700 text-gray-500 dark:text-gray-400 p-2 rounded">
                                <MaterialDesignIcon icon-name="account-outline" class="w-6 h-6"/>
                            </div>
                        </div>
                        <div>
                            <div class="text-gray-900 dark:text-gray-100 truncate" :title="peer.custom_display_name ?? peer.display_name">{{ peer.custom_display_name ?? peer.display_name }}</div>
                            <div class="flex space-x-1 text-gray-500 dark:text-gray-400 text-sm">

                                <!-- time ago -->
                                <span class="flex my-auto space-x-1">
                                    {{ formatTimeAgo(peer.updated_at) }}
                                </span>

                                <!-- hops away -->
                                <span v-if="peer.hops != null && peer.hops !== 128" class="flex my-auto text-sm text-gray-500 space-x-1">
                                    <span>•</span>
                                    <span v-if="peer.hops === 0 || peer.hops === 1">Direct</span>
                                    <span v-else>{{ peer.hops }} hops</span>
                                </span>

                                <!-- snr -->
                                <span v-if="peer.snr != null" class="flex my-auto space-x-1">
                                    <span>•</span>
                                    <span>SNR {{ peer.snr }}</span>
                                </span>

                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="mx-auto my-auto text-center leading-5">

                    <!-- no peers at all -->
                    <div v-if="peersCount === 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Peers Discovered</div>
                        <div>Waiting for someone to announce!</div>
                    </div>

                    <!-- is searching, but no results -->
                    <div v-if="peersSearchTerm !== '' && peersCount > 0" class="flex flex-col text-gray-900 dark:text-gray-100">
                        <div class="mx-auto mb-1">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                            </svg>
                        </div>
                        <div class="font-semibold">No Search Results</div>
                        <div>Your search didn't match any Peers!</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import MaterialDesignIcon from "../MaterialDesignIcon.vue";

export default {
    name: 'MessagesSidebar',
    components: {MaterialDesignIcon},
    emits: ["conversation-click", "peer-click", "conversation-search-changed", "conversation-filter-changed"],
    props: {
        peers: Object,
        conversations: Array,
        selectedDestinationHash: String,
        conversationSearchTerm: {
            type: String,
            default: "",
        },
        filterUnreadOnly: {
            type: Boolean,
            default: false,
        },
        filterFailedOnly: {
            type: Boolean,
            default: false,
        },
        filterHasAttachmentsOnly: {
            type: Boolean,
            default: false,
        },
        isLoading: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            tab: "conversations",
            peersSearchTerm: "",
        };
    },
    methods: {
        onConversationClick(conversation) {
            this.$emit("conversation-click", conversation);
        },
        onPeerClick(peer) {
            this.$emit("peer-click", peer);
        },
        formatTimeAgo: function(datetimeString) {
            return Utils.formatTimeAgo(datetimeString);
        },
        onConversationSearchInput(event) {
            this.$emit("conversation-search-changed", event.target.value);
        },
        toggleFilter(filterKey) {
            this.$emit("conversation-filter-changed", filterKey);
        },
        filterChipClasses(isActive) {
            const base = "px-2 py-1 rounded-full text-xs font-semibold transition-colors";
            if (isActive) {
                return `${base} bg-blue-600 text-white dark:bg-blue-500`;
            }
            return `${base} bg-gray-100 text-gray-700 dark:bg-zinc-800 dark:text-zinc-200`;
        },
    },
    computed: {
        displayedConversations() {
            return this.conversations;
        },
        peersCount() {
            return Object.keys(this.peers).length;
        },
        peersOrderedByLatestAnnounce() {
            const peers = Object.values(this.peers);
            return peers.sort(function(peerA, peerB) {
                // order by updated_at desc
                const peerAUpdatedAt = new Date(peerA.updated_at).getTime();
                const peerBUpdatedAt = new Date(peerB.updated_at).getTime();
                return peerBUpdatedAt - peerAUpdatedAt;
            });
        },
        searchedPeers() {
            return this.peersOrderedByLatestAnnounce.filter((peer) => {
                const search = this.peersSearchTerm.toLowerCase();
                const matchesDisplayName = peer.display_name.toLowerCase().includes(search);
                const matchesCustomDisplayName = peer.custom_display_name?.toLowerCase()?.includes(search) === true;
                const matchesDestinationHash = peer.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesCustomDisplayName || matchesDestinationHash;
            });
        },
    },
}
</script>
