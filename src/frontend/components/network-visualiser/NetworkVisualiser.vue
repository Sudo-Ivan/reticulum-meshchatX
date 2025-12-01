<template>
    <div class="flex-1 h-full min-w-full sm:min-w-[500px] relative dark:bg-zinc-950">
        <!-- network -->
        <div id="network" class="w-full h-full"></div>
        <!-- controls -->
        <div class="absolute bottom-4 left-4 z-10">
            <div class="border border-gray-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 rounded-2xl shadow-lg overflow-hidden min-w-[240px]">
                <div @click="isShowingControls = !isShowingControls" class="flex items-center px-4 py-3 border-b border-gray-200 dark:border-zinc-800 bg-white/80 dark:bg-zinc-900/50 backdrop-blur-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-zinc-800 transition-colors">
                    <div class="flex-1 font-semibold text-gray-900 dark:text-zinc-100">Reticulum Network</div>
                    <button 
                        @click.stop="update" 
                        type="button" 
                        class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 text-white shadow-sm transition-colors"
                        :disabled="isUpdating"
                    >
                        <svg v-if="!isUpdating" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
                        </svg>
                        <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    </button>
                </div>
                <div v-if="isShowingControls" class="px-4 py-3 space-y-3">
                    <div class="flex items-center gap-2">
                        <input 
                            v-model="autoReload" 
                            type="checkbox" 
                            id="auto-reload"
                            class="w-4 h-4 border border-gray-300 dark:border-zinc-600 rounded bg-white dark:bg-zinc-900 text-blue-600 focus:ring-2 focus:ring-blue-500/50 focus:ring-offset-0"
                        >
                        <label for="auto-reload" class="text-sm font-medium text-gray-900 dark:text-zinc-100 cursor-pointer">Auto Update (5 sec)</label>
                    </div>
                    <div class="pt-2 border-t border-gray-200 dark:border-zinc-800">
                        <div class="text-sm font-semibold text-gray-900 dark:text-zinc-100 mb-1">Interfaces</div>
                        <div class="text-xs text-gray-600 dark:text-zinc-400">
                            <span class="text-green-600 dark:text-green-400 font-medium">{{ onlineInterfaces.length }}</span> Online, 
                            <span class="text-red-600 dark:text-red-400 font-medium">{{ offlineInterfaces.length }}</span> Offline
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.vis-tooltip {
    color: white !important;
    background: rgba(0, 0, 0, 0.85) !important;
    border-radius: 0.5rem !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.875rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}

.dark .vis-tooltip {
    background: rgba(24, 24, 27, 0.95) !important;
    border: 1px solid rgba(63, 63, 70, 0.5) !important;
}

#network {
    background-color: rgb(249, 250, 251);
}

.dark #network {
    background-color: rgb(9, 9, 11);
}
</style>

<script>
import "vis-network/styles/vis-network.css";
import { Network } from "vis-network";
import { DataSet } from "vis-data";
import * as mdi from "@mdi/js";
import Utils from "../../js/Utils";
export default {
    name: 'NetworkVisualiser',
    data() {
        return {
            config: null,
            autoReload: false,
            reloadInterval: null,
            isShowingControls: true,
            isUpdating: false,
            interfaces: [],
            pathTable: [],
            announces: {},
            conversations: {},
            network: null,
            nodes: new DataSet(),
            edges: new DataSet(),
            iconCache: {},
        };
    },
    beforeUnmount() {
        clearInterval(this.reloadInterval);
    },
    mounted() {
        this.init();
    },
    methods: {
        async getInterfaceStats() {
            try {
                const response = await axios.get(`/api/v1/interface-stats`);
                this.interfaces = response.data.interface_stats?.interfaces ?? [];
            } catch(e) {
                console.log(e);
            }
        },
        async getPathTable() {
            try {
                const response = await axios.get(`/api/v1/path-table`);
                this.pathTable = response.data.path_table;
            } catch(e) {
                console.log(e);
            }
        },
        async getConfig() {
            try {
                const response = await axios.get("/api/v1/config");
                this.config = response.data.config;
            } catch(e) {
                console.error(e);
            }
        },
        async getAnnounces() {
            try {

                // fetch announces
                const response = await window.axios.get(`/api/v1/announces`);

                // cache announces
                this.announces = {};
                for(const announce of response.data.announces){
                    this.announces[announce.destination_hash] = announce;
                }

            } catch(e) {
                // do nothing if failed to load announces
                console.log(e);
            }
        },
        async getConversations() {
            try {
                const response = await window.axios.get(`/api/v1/lxmf/conversations`);
                this.conversations = {};
                for(const conversation of response.data.conversations){
                    this.conversations[conversation.destination_hash] = conversation;
                }
            } catch(e) {
                console.log(e);
            }
        },
        async createIconImage(iconName, foregroundColor, backgroundColor, size = 32) {
            const cacheKey = `${iconName}-${foregroundColor}-${backgroundColor}-${size}`;
            if(this.iconCache[cacheKey]){
                return this.iconCache[cacheKey];
            }

            return new Promise((resolve) => {
                const canvas = document.createElement('canvas');
                canvas.width = size;
                canvas.height = size;
                const ctx = canvas.getContext('2d');

                // draw background circle
                ctx.fillStyle = backgroundColor;
                ctx.beginPath();
                ctx.arc(size / 2, size / 2, size / 2 - 1, 0, 2 * Math.PI);
                ctx.fill();

                // load MDI icon SVG
                const iconSvg = this.getMdiIconSvg(iconName, foregroundColor);
                const img = new Image();
                const svgBlob = new Blob([iconSvg], { type: 'image/svg+xml' });
                const url = URL.createObjectURL(svgBlob);
                img.onload = () => {
                    ctx.drawImage(img, size * 0.2, size * 0.2, size * 0.6, size * 0.6);
                    URL.revokeObjectURL(url);
                    const dataUrl = canvas.toDataURL();
                    this.iconCache[cacheKey] = dataUrl;
                    resolve(dataUrl);
                };
                img.onerror = () => {
                    URL.revokeObjectURL(url);
                    const dataUrl = canvas.toDataURL();
                    this.iconCache[cacheKey] = dataUrl;
                    resolve(dataUrl);
                };
                img.src = url;
            });
        },
        getMdiIconSvg(iconName, foregroundColor) {
            const mdiIconName = "mdi" + iconName.split("-").map((word) => {
                return word.charAt(0).toUpperCase() + word.slice(1);
            }).join("");
            
            const iconPath = mdi[mdiIconName] || mdi["mdiAccountOutline"];
            
            return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="${foregroundColor}" d="${iconPath}"/></svg>`;
        },
        async createMdiIconImage(iconName, size = 32) {
            const foregroundColor = '#ffffff';
            const backgroundColor = '#6b7280';
            return await this.createIconImage(iconName, foregroundColor, backgroundColor, size);
        },
        async init() {

            // create network ui
            const container = document.getElementById("network");
            this.network = new Network(container, {
                nodes: this.nodes,
                edges: this.edges,
            }, {
                interaction: {
                    tooltipDelay: 0, // show tooltip instantly on hover
                },
                layout: {
                    // always layout nodes the same way across reloads if nothing changed
                    randomSeed: 1,
                },
                nodes: {
                    color: {
                        border: "#e5e7eb",
                        highlight: {
                            border: "#3b82f6",
                        },
                    },
                    font: {
                        color: "#111827",
                        size: 14,
                        background: "rgba(255, 255, 255, 0.9)",
                    },
                },
                edges: {
                    color: {
                        color: "#9ca3af",
                        highlight: "#3b82f6",
                    },
                    width: 2,
                },
                physics: {
                    barnesHut: {
                        gravitationalConstant: -5000,
                        // centralGravity: 0,
                        // springConstant: 0.1,
                        // damping: 0.15,
                    },
                    // maxVelocity: 150,
                    // minVelocity: 0.25,
                },
                groups: {
                    "me": {
                        shape: "image",
                        image: "/assets/images/reticulum_logo_512.png",
                    },
                    "interface": {

                    },
                    "announce": {

                    },
                },
            });

            // handle double click on a node
            this.network.on("doubleClick", (params) => {

                // get clicked node id
                const clickedNodeId = params.nodes[0];
                if(!clickedNodeId){
                    return;
                }

                // find node by id
                const node = this.network.body.nodes[clickedNodeId];
                if(!node){
                    return;
                }

                // handle double click on an announce node
                if(node.options.group === "announce"){

                    // get announce
                    const announce = node.options._announce;
                    if(!announce) {
                        return;
                    }

                    // handle double click on lxmf.delivery node
                    if(announce.aspect === "lxmf.delivery"){

                        // go to messages page for this destination hash
                        this.$router.push({
                            name: "messages",
                            params: {
                                destinationHash: announce.destination_hash,
                            },
                        });

                    }

                    // handle double click on nomadnetwork.node node
                    if(announce.aspect === "nomadnetwork.node"){

                        // go to nomadnetwork page for this destination hash
                        this.$router.push({
                            name: "nomadnetwork",
                            params: {
                                destinationHash: announce.destination_hash,
                            },
                        });

                    }

                }

            });

            // update network
            await this.update();

            // fit network after initial load
            setTimeout(() => {
                this.network.fit({
                    animation: true,
                });
            }, 2000);

            // auto reload
            this.reloadInterval = setInterval(this.onAutoReload, 5000);

        },
        async onAutoReload() {

            // do nothing if auto reload disabled
            if(!this.autoReload){
                return;
            }

            // do nothing if already updating
            if(this.isUpdating){
                return;
            }

            // auto reload
            try {
                this.isUpdating = true;
                await this.update();
            } finally {
                this.isUpdating = false;
            }

        },
        async update() {

            this.isUpdating = true;
            try {
                await this.getConfig();
                await this.getInterfaceStats();
                await this.getPathTable();
                await this.getAnnounces();
                await this.getConversations();
            } finally {
                this.isUpdating = false;
            }

            const nodes = [];
            const edges = [];

            const isDarkMode = document.documentElement.classList.contains('dark');
            const fontColor = isDarkMode ? "#f4f4f5" : "#111827";
            const fontBackground = isDarkMode ? "rgba(24, 24, 27, 0.9)" : "rgba(255, 255, 255, 0.9)";

            // add me
            nodes.push({
                id: "me",
                group: "me",
                size: 60,
                label: this.config?.display_name ?? "This Device",
                title: [
                    `${this.config?.display_name ?? 'This Device'}`,
                    `Identity: ${this.config?.identity_hash ?? 'Unknown'}`,
                ].join("\n"),
                font: {
                    color: fontColor,
                    background: fontBackground,
                },
            });

            // add interfaces
            for(const entry of this.interfaces){

                // determine label
                var label = entry.interface_name ?? entry.name;

                // we want to show the full info for LocalServerInterface
                // we also want to show the full info instead of just "Client on Name" for TCPServerInterface clients
                if(entry.type === "LocalServerInterface" || entry.parent_interface_name != null){
                    label = entry.name;
                }

                const node = {
                    id: entry.name,
                    group: "interface",
                    label: label,
                    title: [
                        entry.name,
                        `State: ${entry.status ? 'Online' : 'Offline'}`,
                        `Bitrate: ${this.formatBitsPerSecond(entry.bitrate)}`,
                        `TX: ${this.formatBytes(entry.txb)}`,
                        `RX: ${this.formatBytes(entry.rxb)}`,
                    ].join("\n"),
                    size: 30,
                    font: {
                        color: fontColor,
                        background: fontBackground,
                    },
                    shape: "circularImage",
                    image: entry.status ? "/assets/images/network-visualiser/interface_connected.png" : "/assets/images/network-visualiser/interface_disconnected.png",
                };

                // add interface node
                nodes.push(node);

                // add edge to interface
                if(entry.parent_interface_name){
                    // add edge from parent interface to interface
                    edges.push({
                        id: `${entry.parent_interface_name}~${entry.name}`,
                        from: entry.parent_interface_name,
                        to: entry.name,
                        color: entry.status ? "#22c55e" : "#ef4444",
                        width: 3,
                        length: 300,
                    });
                } else {
                    // add edge from me to interface
                    edges.push({
                        id: `me~${entry.name}`,
                        from: "me",
                        to: entry.name,
                        color: entry.status ? "#22c55e" : "#ef4444",
                        width: 3,
                        length: 300,
                    });
                }

            }

            // add paths for announces
            for(const entry of this.pathTable){

                // skip this path if hops are unknown
                if(entry.hops == null){
                    continue;
                }

                // find what announced this path, or skip showing it for now
                const announce = this.announces[entry.hash];
                if(!announce){
                    continue;
                }

                // skip announces if we don't want to show them
                const aspectsToShow = ["lxmf.delivery", "nomadnetwork.node"];
                if(!aspectsToShow.includes(announce.aspect)){
                    continue;
                }

                const node = {
                    id: entry.hash,
                    group: "announce",
                    size: 20,
                };

                if(announce.aspect === "lxmf.delivery"){

                    const name = announce.custom_display_name ?? announce.display_name;
                    const conversation = this.conversations[announce.destination_hash];

                    node.shape = "circularImage";
                    
                    if(conversation?.lxmf_user_icon){
                        const iconImage = await this.createIconImage(
                            conversation.lxmf_user_icon.icon_name,
                            conversation.lxmf_user_icon.foreground_colour,
                            conversation.lxmf_user_icon.background_colour,
                            40
                        );
                        node.image = iconImage;
                        node.size = 30;
                    } else {
                        node.image = entry.hops === 1 ? "/assets/images/network-visualiser/user_1hop.png" : "/assets/images/network-visualiser/user.png";
                    }

                    node.label = name;
                    node.title = [
                        `Name: ${announce.display_name}`,
                        announce.custom_display_name != null ? `Custom Name: ${announce.custom_display_name}` : null,
                        `Aspect: ${announce.aspect}`,
                        `Identity: ${announce.identity_hash}`,
                        `Destination: ${announce.destination_hash}`,
                        `Path: ${entry.hops} ${entry.hops === 1 ? 'Hop' : 'Hops'} via ${entry.interface}`,
                        `Announced At: ${announce.updated_at}`,
                    ].filter((line) => line != null).join("\n");

                }

                if(announce.aspect === "nomadnetwork.node"){

                    const name = announce.custom_display_name ?? announce.display_name;

                    node.shape = "circularImage";
                    node.image = entry.hops === 1 ? "/assets/images/network-visualiser/server_1hop.png" : "/assets/images/network-visualiser/server.png";

                    node.label = name;
                    node.title = [
                        `Name: ${announce.display_name}`,
                        announce.custom_display_name != null ? `Custom Name: ${announce.custom_display_name}` : null,
                        `Aspect: ${announce.aspect}`,
                        `Identity: ${announce.identity_hash}`,
                        `Destination: ${announce.destination_hash}`,
                        `Path: ${entry.hops} ${entry.hops === 1 ? 'Hop' : 'Hops'} via ${entry.interface}`,
                        `Announced At: ${announce.updated_at}`,
                    ].filter((line) => line != null).join("\n");

                }

                // attach announce to this node
                node._announce = announce;

                // add node
                nodes.push(node);

                // add edge from interface to announced aspect
                edges.push({
                    id: `${entry.interface}~${entry.hash}`,
                    from: entry.interface,
                    to: entry.hash,
                    color: isDarkMode ? "#71717a" : "#9ca3af",
                    width: 2,
                });

            }

            // process nodes and edges
            this.processNewNodes(nodes);
            this.processNewEdges(edges);

        },
        processNewNodes(newNodes) {

            // determine old and new nodes
            const oldNodeIds = this.nodes.map((node) => node.id);
            const newNodeIds = newNodes.map((node) => node.id);

            // log new nodes
            for(const newNodeId of newNodeIds){
                if(!oldNodeIds.includes(newNodeId)){
                    console.log("Added Node: " + newNodeId);
                }
            }

            // remove old nodes that no longer exist
            for(const oldNodeId of oldNodeIds){
                if(!newNodeIds.includes(oldNodeId)){
                    console.log("Removed Node: " + oldNodeId);
                    this.nodes.remove(oldNodeId);
                }
            }

            // update nodes
            this.nodes.update(newNodes);

        },
        processNewEdges(newEdges) {

            // determine old and new edges
            const oldEdgeIds = this.edges.map((edge) => edge.id);
            const newEdgeIds = newEdges.map((edge) => edge.id);

            // log new edges
            for(const newEdgeId of newEdgeIds){
                if(!oldEdgeIds.includes(newEdgeId)){
                    console.log("Added Edge: " + newEdgeId);
                }
            }

            // remove old edges that no longer exist
            for(const oldEdgeId of oldEdgeIds){
                if(!newEdgeIds.includes(oldEdgeId)){
                    console.log("Removed Edge: " + oldEdgeId);
                    this.edges.remove(oldEdgeId);
                }
            }

            // update edges
            this.edges.update(newEdges);

        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
        formatBitsPerSecond: function(bits) {
            return Utils.formatBitsPerSecond(bits);
        },
    },
    computed: {
        onlineInterfaces() {
            return this.interfaces.filter((iface) => {
                return iface.status;
            });
        },
        offlineInterfaces() {
            return this.interfaces.filter((iface) => {
                return !iface.status;
            });
        },
    },
}
</script>

