<template>
    <div class="flex flex-col w-80 min-w-80 min-h-0 bg-white/90 dark:bg-zinc-950/80 backdrop-blur border-r border-gray-200 dark:border-zinc-800">

        <div class="flex">
            <button @click="tab = 'favourites'" type="button" class="sidebar-tab" :class="{ 'sidebar-tab--active': tab === 'favourites' }">
                Favourites
            </button>
            <button @click="tab = 'announces'" type="button" class="sidebar-tab" :class="{ 'sidebar-tab--active': tab === 'announces' }">
                Announces
            </button>
        </div>

        <div v-if="tab === 'favourites'" class="flex-1 flex flex-col min-h-0">
            <div class="p-3 border-b border-gray-200 dark:border-zinc-800">
                <input v-model="favouritesSearchTerm" type="text" placeholder="Search favourites" class="input-field"/>
            </div>
            <div class="flex-1 overflow-y-auto px-2 pb-4">
                <div v-if="searchedFavourites.length > 0" class="space-y-2">
                    <div
                        v-for="favourite of searchedFavourites"
                        :key="favourite.destination_hash"
                        @click="onFavouriteClick(favourite)"
                        class="favourite-card"
                        :class="[
                            favourite.destination_hash === selectedDestinationHash ? 'favourite-card--active' : '',
                            draggingFavouriteHash === favourite.destination_hash ? 'favourite-card--dragging' : ''
                        ]"
                        draggable="true"
                        @dragstart="onFavouriteDragStart($event, favourite)"
                        @dragover.prevent="onFavouriteDragOver($event)"
                        @drop.prevent="onFavouriteDrop($event, favourite)"
                        @dragend="onFavouriteDragEnd"
                    >
                        <div class="favourite-card__icon">
                            <MaterialDesignIcon icon-name="server-network" class="w-5 h-5"/>
                        </div>
                        <div class="flex-1">
                            <div class="text-sm font-semibold text-gray-900 dark:text-white truncate" :title="favourite.display_name">{{ favourite.display_name }}</div>
                            <div class="text-xs text-gray-500 dark:text-gray-400">{{ formatDestinationHash(favourite.destination_hash) }}</div>
                        </div>
                        <DropDownMenu>
                            <template #button>
                                <IconButton class="bg-transparent dark:bg-transparent">
                                    <MaterialDesignIcon icon-name="dots-vertical" class="w-5 h-5"/>
                                </IconButton>
                            </template>
                            <template #items>
                                <DropDownMenuItem @click="onRenameFavourite(favourite)">
                                    <MaterialDesignIcon icon-name="pencil" class="w-5 h-5"/>
                                    <span>Rename</span>
                                </DropDownMenuItem>
                                <DropDownMenuItem @click="onRemoveFavourite(favourite)">
                                    <MaterialDesignIcon icon-name="trash-can" class="w-5 h-5 text-red-500"/>
                                    <span class="text-red-500">Remove</span>
                                </DropDownMenuItem>
                            </template>
                        </DropDownMenu>
                    </div>
                </div>
                <div v-else class="empty-state">
                    <MaterialDesignIcon icon-name="star-outline" class="w-8 h-8"/>
                    <div class="font-semibold">No favourites</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">Add nodes from the announces tab.</div>
                </div>
            </div>
        </div>

        <div v-else class="flex-1 flex flex-col min-h-0">
            <div class="p-3 border-b border-gray-200 dark:border-zinc-800">
                <input v-model="nodesSearchTerm" type="text" placeholder="Search announces" class="input-field"/>
            </div>
            <div class="flex-1 overflow-y-auto px-2 pb-4">
                <div v-if="searchedNodes.length > 0" class="space-y-2">
                    <div v-for="node of searchedNodes" :key="node.destination_hash" @click="onNodeClick(node)" class="announce-card" :class="{ 'announce-card--active': node.destination_hash === selectedDestinationHash }">
                        <div class="announce-card__icon">
                            <MaterialDesignIcon icon-name="satellite-uplink" class="w-5 h-5"/>
                        </div>
                        <div>
                            <div class="text-sm font-semibold text-gray-900 dark:text-white truncate" :title="node.display_name">{{ node.display_name }}</div>
                            <div class="text-xs text-gray-500 dark:text-gray-400">Announced {{ formatTimeAgo(node.updated_at) }}</div>
                        </div>
                    </div>
                </div>
                <div v-else class="empty-state">
                    <MaterialDesignIcon icon-name="radar" class="w-8 h-8"/>
                    <div class="font-semibold">No announces yet</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">Listening for peers on the mesh.</div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>

import Utils from "../../js/Utils";
import MaterialDesignIcon from "../MaterialDesignIcon.vue";
import DropDownMenu from "../DropDownMenu.vue";
import IconButton from "../IconButton.vue";
import DropDownMenuItem from "../DropDownMenuItem.vue";

export default {
    name: 'NomadNetworkSidebar',
    components: {DropDownMenuItem, IconButton, DropDownMenu, MaterialDesignIcon},
    props: {
        nodes: Object,
        favourites: Array,
        selectedDestinationHash: String,
    },
    data() {
        return {
            tab: "favourites",
            favouritesSearchTerm: "",
            nodesSearchTerm: "",
            favouritesOrder: [],
            draggingFavouriteHash: null,
        };
    },
    mounted() {
        this.loadFavouriteOrder();
        this.ensureFavouriteOrder();
    },
    watch: {
        favourites: {
            handler() {
                this.ensureFavouriteOrder();
            },
            deep: true,
        },
    },
    methods: {
        onNodeClick(node) {
            this.$emit("node-click", node);
        },
        onFavouriteClick(favourite) {
            this.onNodeClick(favourite);
        },
        onRenameFavourite(favourite) {
            this.$emit("rename-favourite", favourite);
        },
        onRemoveFavourite(favourite) {
            this.$emit("remove-favourite", favourite);
        },
        loadFavouriteOrder() {
            try {
                const stored = localStorage.getItem("meshchat.nomadnet.favourites");
                if(stored){
                    this.favouritesOrder = JSON.parse(stored);
                }
            } catch(e) {
                console.log(e);
            }
        },
        persistFavouriteOrder() {
            localStorage.setItem("meshchat.nomadnet.favourites", JSON.stringify(this.favouritesOrder));
        },
        ensureFavouriteOrder() {
            const hashes = this.favourites.map((fav) => fav.destination_hash);
            const nextOrder = this.favouritesOrder.filter((hash) => hashes.includes(hash));
            hashes.forEach((hash) => {
                if(!nextOrder.includes(hash)){
                    nextOrder.push(hash);
                }
            });
            if(JSON.stringify(nextOrder) !== JSON.stringify(this.favouritesOrder)){
                this.favouritesOrder = nextOrder;
                this.persistFavouriteOrder();
            }
        },
        onFavouriteDragStart(event, favourite) {
            try {
                if(event?.dataTransfer){
                    event.dataTransfer.effectAllowed = "move";
                    event.dataTransfer.setData("text/plain", favourite.destination_hash);
                }
            } catch(e) {
                // ignore for browsers that prevent setting drag meta
            }
            this.draggingFavouriteHash = favourite.destination_hash;
        },
        onFavouriteDragOver(event) {
            if(event?.dataTransfer){
                event.dataTransfer.dropEffect = "move";
            }
        },
        onFavouriteDrop(event, targetFavourite) {
            if(!this.draggingFavouriteHash || this.draggingFavouriteHash === targetFavourite.destination_hash){
                return;
            }
            const fromIndex = this.favouritesOrder.indexOf(this.draggingFavouriteHash);
            const toIndex = this.favouritesOrder.indexOf(targetFavourite.destination_hash);
            if(fromIndex === -1 || toIndex === -1){
                return;
            }
            const updated = [...this.favouritesOrder];
            updated.splice(fromIndex, 1);
            updated.splice(toIndex, 0, this.draggingFavouriteHash);
            this.favouritesOrder = updated;
            this.persistFavouriteOrder();
            this.draggingFavouriteHash = null;
        },
        onFavouriteDragEnd() {
            this.draggingFavouriteHash = null;
        },
        formatTimeAgo: function(datetimeString) {
            return Utils.formatTimeAgo(datetimeString);
        },
        formatDestinationHash: function(destinationHash) {
            return Utils.formatDestinationHash(destinationHash);
        },
    },
    computed: {
        nodesCount() {
            return Object.keys(this.nodes).length;
        },
        nodesOrderedByLatestAnnounce() {
            const nodes = Object.values(this.nodes);
            return nodes.sort(function(nodeA, nodeB) {
                // order by updated_at desc
                const nodeAUpdatedAt = new Date(nodeA.updated_at).getTime();
                const nodeBUpdatedAt = new Date(nodeB.updated_at).getTime();
                return nodeBUpdatedAt - nodeAUpdatedAt;
            });
        },
        searchedNodes() {
            return this.nodesOrderedByLatestAnnounce.filter((node) => {
                const search = this.nodesSearchTerm.toLowerCase();
                const matchesDisplayName = node.display_name.toLowerCase().includes(search);
                const matchesDestinationHash = node.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesDestinationHash;
            });
        },
        orderedFavourites() {
            return [...this.favourites].sort((a, b) => {
                return this.favouritesOrder.indexOf(a.destination_hash) - this.favouritesOrder.indexOf(b.destination_hash);
            });
        },
        searchedFavourites() {
            return this.orderedFavourites.filter((favourite) => {
                const search = this.favouritesSearchTerm.toLowerCase();
                const matchesDisplayName = favourite.display_name.toLowerCase().includes(search);
                const matchesCustomDisplayName = favourite.custom_display_name?.toLowerCase()?.includes(search) === true;
                const matchesDestinationHash = favourite.destination_hash.toLowerCase().includes(search);
                return matchesDisplayName || matchesCustomDisplayName || matchesDestinationHash;
            });
        },
    },
}
</script>

<style scoped>
.sidebar-tab {
    @apply w-1/2 py-3 text-sm font-semibold text-gray-500 dark:text-gray-400 border-b-2 border-transparent transition;
}
.sidebar-tab--active {
    @apply text-blue-600 border-blue-500 dark:text-blue-300 dark:border-blue-400;
}
.favourite-card {
    @apply flex items-center gap-3 rounded-2xl border border-gray-200 dark:border-zinc-800 bg-white/90 dark:bg-zinc-900/70 px-3 py-2 cursor-pointer hover:border-blue-400 dark:hover:border-blue-500;
}
.favourite-card--active {
    @apply border-blue-500 dark:border-blue-400 bg-blue-50/60 dark:bg-blue-900/30;
}
.favourite-card__icon,
.announce-card__icon {
    @apply w-10 h-10 rounded-xl bg-gray-100 dark:bg-zinc-800 flex items-center justify-center text-gray-500 dark:text-gray-300;
}
.favourite-card--dragging {
    @apply opacity-60 ring-2 ring-blue-300 dark:ring-blue-600;
}
.announce-card {
    @apply flex items-center gap-3 rounded-2xl border border-gray-200 dark:border-zinc-800 bg-white/90 dark:bg-zinc-900/70 px-3 py-2 cursor-pointer hover:border-blue-400 dark:hover:border-blue-500;
}
.announce-card--active {
    @apply border-blue-500 dark:border-blue-400 bg-blue-50/70 dark:bg-blue-900/30;
}
.empty-state {
    @apply flex flex-col items-center justify-center text-center gap-2 text-gray-500 dark:text-gray-400 mt-20;
}
</style>
