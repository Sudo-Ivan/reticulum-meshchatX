<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] bg-gradient-to-br from-slate-50 via-slate-100 to-white dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-900">
        <div class="flex-1 overflow-y-auto w-full px-4 md:px-8 py-6">
            <div class="space-y-4 w-full max-w-6xl mx-auto">

            <!-- hero card -->
            <div class="bg-white/90 dark:bg-zinc-900/80 backdrop-blur border border-gray-200 dark:border-zinc-800 rounded-3xl shadow-xl p-5 md:p-6">
                <div class="flex flex-col md:flex-row md:items-center gap-4">
                    <div class="flex-1 space-y-1">
                        <div class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">Profile</div>
                        <div class="text-2xl font-semibold text-gray-900 dark:text-white">{{ config.display_name }}</div>
                        <div class="text-sm text-gray-600 dark:text-gray-300">Manage your identity, transport participation and LXMF defaults.</div>
                    </div>
                    <div class="flex flex-col sm:flex-row gap-2">
                        <button @click="copyValue(config.identity_hash, 'Identity Hash')" type="button" class="inline-flex items-center justify-center gap-x-2 rounded-xl border border-gray-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 px-4 py-2 text-sm font-semibold text-gray-900 dark:text-zinc-100 shadow-sm hover:border-blue-400 dark:hover:border-blue-400/70 transition">
                            <MaterialDesignIcon icon-name="content-copy" class="w-4 h-4"/>
                            Identity
                        </button>
                        <button @click="copyValue(config.lxmf_address_hash, 'LXMF Address')" type="button" class="inline-flex items-center justify-center gap-x-2 rounded-xl bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 px-4 py-2 text-sm font-semibold text-white shadow hover:shadow-md transition">
                            <MaterialDesignIcon icon-name="account-plus" class="w-4 h-4"/>
                            LXMF Address
                        </button>
                    </div>
                </div>
                <transition name="fade">
                    <div v-if="copyToast" class="mt-3 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200 px-3 py-1 text-xs inline-flex items-center gap-2">
                        {{ copyToast }}
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
                    </div>
                </transition>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-4 text-sm text-gray-600 dark:text-gray-300">
                    <div class="rounded-2xl border border-gray-200 dark:border-zinc-800 p-3 bg-white/70 dark:bg-zinc-900/70">
                        <div class="text-xs uppercase tracking-wide">Theme</div>
                        <div class="font-semibold text-gray-900 dark:text-white capitalize">{{ config.theme }} mode</div>
                    </div>
                    <div class="rounded-2xl border border-gray-200 dark:border-zinc-800 p-3 bg-white/70 dark:bg-zinc-900/70">
                        <div class="text-xs uppercase tracking-wide">Transport</div>
                        <div class="font-semibold text-gray-900 dark:text-white">{{ config.is_transport_enabled ? 'Enabled' : 'Disabled' }}</div>
                    </div>
                    <div class="rounded-2xl border border-gray-200 dark:border-zinc-800 p-3 bg-white/70 dark:bg-zinc-900/70">
                        <div class="text-xs uppercase tracking-wide">Propagation</div>
                        <div class="font-semibold text-gray-900 dark:text-white">{{ config.lxmf_local_propagation_node_enabled ? 'Local node running' : 'Client-only' }}</div>
                    </div>
                </div>
                <div class="grid gap-3 mt-4 text-sm text-gray-700 dark:text-gray-200 sm:grid-cols-2">
                    <div class="address-card">
                        <div class="address-card__label">Identity Hash</div>
                        <div class="address-card__value monospace-field">{{ config.identity_hash }}</div>
                        <button @click="copyValue(config.identity_hash, 'Identity Hash')" type="button" class="address-card__action">
                            <MaterialDesignIcon icon-name="content-copy" class="w-4 h-4"/>
                            Copy
                        </button>
                    </div>
                    <div class="address-card">
                        <div class="address-card__label">LXMF Address</div>
                        <div class="address-card__value monospace-field">{{ config.lxmf_address_hash }}</div>
                        <button @click="copyValue(config.lxmf_address_hash, 'LXMF Address')" type="button" class="address-card__action">
                            <MaterialDesignIcon icon-name="content-copy" class="w-4 h-4"/>
                            Copy
                        </button>
                    </div>
                </div>
            </div>

            <!-- settings grid -->
            <div class="grid gap-4 lg:grid-cols-2">

                <!-- Appearance -->
                <section class="glass-card">
                    <header class="glass-card__header">
                        <div>
                            <div class="glass-card__eyebrow">Personalise</div>
                            <h2>Appearance</h2>
                            <p>Switch between light and dark presets anytime.</p>
                        </div>
                    </header>
                    <div class="glass-card__body space-y-3">
                        <select v-model="config.theme" @change="onThemeChange" class="input-field">
                            <option value="light">Light Theme</option>
                            <option value="dark">Dark Theme</option>
                        </select>
                        <div class="flex items-center justify-between text-sm text-gray-600 dark:text-gray-300 border border-dashed border-gray-200 dark:border-zinc-800 rounded-2xl px-3 py-2">
                            <div>Live preview updates instantly.</div>
                            <span class="inline-flex items-center gap-1 text-blue-500 dark:text-blue-300 text-xs font-semibold uppercase">
                                <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                                Realtime
                            </span>
                        </div>
                    </div>
                </section>

                <!-- Transport -->
                <section class="glass-card">
                    <header class="glass-card__header">
                        <div>
                            <div class="glass-card__eyebrow">Reticulum</div>
                            <h2>Transport Mode</h2>
                            <p>Relay paths and traffic for nearby peers.</p>
                        </div>
                    </header>
                    <div class="glass-card__body space-y-3">
                        <label class="setting-toggle">
                            <input type="checkbox" v-model="config.is_transport_enabled" @change="onIsTransportEnabledChange">
                            <span class="setting-toggle__label">
                                <span class="setting-toggle__title">Enable Transport Mode</span>
                                <span class="setting-toggle__description">Route announces, respond to path requests and help your mesh stay online.</span>
                                <span class="setting-toggle__hint">Requires restart after toggling.</span>
                            </span>
                        </label>
                    </div>
                </section>

                <!-- Interfaces -->
                <section class="glass-card">
                    <header class="glass-card__header">
                        <div>
                            <div class="glass-card__eyebrow">Adapters</div>
                            <h2>Interfaces</h2>
                            <p>Show curated community configs inside the interface wizard.</p>
                        </div>
                    </header>
                    <div class="glass-card__body space-y-3">
                        <label class="setting-toggle">
                            <input type="checkbox" v-model="config.show_suggested_community_interfaces" @change="onShowSuggestedCommunityInterfacesChange">
                            <span class="setting-toggle__label">
                                <span class="setting-toggle__title">Show Community Interfaces</span>
                                <span class="setting-toggle__description">Surface community-maintained presets while adding new interfaces.</span>
                            </span>
                        </label>
                    </div>
                </section>

                <!-- Messages -->
                <section class="glass-card">
                    <header class="glass-card__header">
                        <div>
                            <div class="glass-card__eyebrow">Reliability</div>
                            <h2>Messages</h2>
                            <p>Control how MeshChat retries or escalates failed deliveries.</p>
                        </div>
                    </header>
                    <div class="glass-card__body space-y-3">
                        <label class="setting-toggle">
                            <input type="checkbox" v-model="config.auto_resend_failed_messages_when_announce_received" @change="onAutoResendFailedMessagesWhenAnnounceReceivedChange">
                            <span class="setting-toggle__label">
                                <span class="setting-toggle__title">Auto resend when peer announces</span>
                                <span class="setting-toggle__description">Failed messages automatically retry once the destination broadcasts again.</span>
                            </span>
                        </label>
                        <label class="setting-toggle">
                            <input type="checkbox" v-model="config.allow_auto_resending_failed_messages_with_attachments" @change="onAllowAutoResendingFailedMessagesWithAttachmentsChange">
                            <span class="setting-toggle__label">
                                <span class="setting-toggle__title">Allow retries with attachments</span>
                                <span class="setting-toggle__description">Large payloads will also be retried (useful when both peers have high limits).</span>
                            </span>
                        </label>
                        <label class="setting-toggle">
                            <input type="checkbox" v-model="config.auto_send_failed_messages_to_propagation_node" @change="onAutoSendFailedMessagesToPropagationNodeChange">
                            <span class="setting-toggle__label">
                                <span class="setting-toggle__title">Auto fall back to propagation node</span>
                                <span class="setting-toggle__description">Failed direct deliveries are queued on your preferred propagation node.</span>
                            </span>
                        </label>
                        <div class="space-y-2">
                            <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Inbound Message Stamp Cost</div>
                            <input v-model.number="config.lxmf_inbound_stamp_cost" @input="onLxmfInboundStampCostChange" type="number" min="1" max="254" placeholder="8" class="input-field">
                            <div class="text-xs text-gray-600 dark:text-gray-400">
                                Require proof-of-work stamps for direct delivery messages sent to you. Higher values require more computational work from senders. Range: 1-254. Default: 8.
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Propagation nodes -->
                <section class="glass-card lg:col-span-2">
                    <header class="glass-card__header">
                        <div>
                            <div class="glass-card__eyebrow">LXMF</div>
                            <h2>Propagation Nodes</h2>
                            <p>Keep conversations flowing even when peers are offline.</p>
                        </div>
                        <RouterLink :to="{ name: 'propagation-nodes' }" class="primary-chip">
                            Browse Nodes
                        </RouterLink>
                    </header>
                    <div class="glass-card__body space-y-5">
                        <div class="info-callout">
                            <ul class="list-disc list-inside space-y-1 text-sm">
                                <li>Propagation nodes hold messages securely until recipients sync again.</li>
                                <li>Nodes peer with each other to distribute encrypted payloads.</li>
                                <li>Most nodes retain data ~30 days, then discard undelivered items.</li>
                            </ul>
                        </div>
                        <label class="setting-toggle">
                            <input type="checkbox" v-model="config.lxmf_local_propagation_node_enabled" @change="onLxmfLocalPropagationNodeEnabledChange">
                            <span class="setting-toggle__label">
                                <span class="setting-toggle__title">Run a local propagation node</span>
                                <span class="setting-toggle__description">MeshChat will announce and maintain a node using this local destination hash.</span>
                                <span class="setting-toggle__hint monospace-field">{{ config.lxmf_local_propagation_node_address_hash || '—' }}</span>
                            </span>
                        </label>
                        <div class="space-y-2">
                            <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Preferred Propagation Node</div>
                            <input v-model="config.lxmf_preferred_propagation_node_destination_hash" @input="onLxmfPreferredPropagationNodeDestinationHashChange" type="text" placeholder="Destination hash, e.g. a39610c89d18bb48c73e429582423c24" class="input-field monospace-field">
                            <div class="text-xs text-gray-600 dark:text-gray-400">Messages fallback to this node whenever direct delivery fails.</div>
                        </div>
                        <div class="space-y-2">
                            <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Auto Sync Interval</div>
                            <select v-model="config.lxmf_preferred_propagation_node_auto_sync_interval_seconds" @change="onLxmfPreferredPropagationNodeAutoSyncIntervalSecondsChange" class="input-field">
                                <option value="0">Disabled</option>
                                <option value="900">Every 15 Minutes</option>
                                <option value="1800">Every 30 Minutes</option>
                                <option value="3600">Every 1 Hour</option>
                                <option value="10800">Every 3 Hours</option>
                                <option value="21600">Every 6 Hours</option>
                                <option value="43200">Every 12 Hours</option>
                                <option value="86400">Every 24 Hours</option>
                            </select>
                            <div class="text-xs text-gray-600 dark:text-gray-400">
                                <span v-if="config.lxmf_preferred_propagation_node_last_synced_at">Last synced {{ formatSecondsAgo(config.lxmf_preferred_propagation_node_last_synced_at) }} ago.</span>
                                <span v-else>Last synced: never.</span>
                            </div>
                        </div>
                        <div v-if="config.lxmf_local_propagation_node_enabled" class="space-y-2">
                            <div class="text-sm font-medium text-gray-900 dark:text-gray-100">Propagation Node Stamp Cost</div>
                            <input v-model.number="config.lxmf_propagation_node_stamp_cost" @input="onLxmfPropagationNodeStampCostChange" type="number" min="13" max="254" placeholder="16" class="input-field">
                            <div class="text-xs text-gray-600 dark:text-gray-400">
                                Require proof-of-work stamps for messages propagated through your node. Higher values require more computational work. Range: 13-254. Default: 16. <strong>Note:</strong> Changing this requires restarting the app.
                            </div>
                        </div>
                    </div>
                </section>

            </div>
            </div>
        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import WebSocketConnection from "../../js/WebSocketConnection";
import DialogUtils from "../../js/DialogUtils";
import MaterialDesignIcon from "../MaterialDesignIcon.vue";

export default {
    name: 'SettingsPage',
    components: {
        MaterialDesignIcon,
    },
    data() {
        return {
            config: {
                auto_resend_failed_messages_when_announce_received: null,
                allow_auto_resending_failed_messages_with_attachments: null,
                auto_send_failed_messages_to_propagation_node: null,
                show_suggested_community_interfaces: null,
                lxmf_local_propagation_node_enabled: null,
                lxmf_preferred_propagation_node_destination_hash: null,
            },
            copyToast: null,
            copyToastTimeout: null,
        };
    },
    beforeUnmount() {

        // stop listening for websocket messages
        WebSocketConnection.off("message", this.onWebsocketMessage);
        clearTimeout(this.copyToastTimeout);

    },
    mounted() {

        // listen for websocket messages
        WebSocketConnection.on("message", this.onWebsocketMessage);

        this.getConfig();

    },
    methods: {
        async onWebsocketMessage(message) {
            const json = JSON.parse(message.data);
            switch(json.type){
                case 'config': {
                    this.config = json.config;
                    break;
                }
            }
        },
        async getConfig() {
            try {
                const response = await window.axios.get("/api/v1/config");
                this.config = response.data.config;
            } catch(e) {
                // do nothing if failed to load config
                console.log(e);
            }
        },
        async updateConfig(config) {
            try {
                const response = await window.axios.patch("/api/v1/config", config);
                this.config = response.data.config;
            } catch(e) {
                alert("Failed to save config!");
                console.log(e);
            }
        },
        async copyValue(value, label) {
            if(!value){
                DialogUtils.alert(`Nothing to copy for ${label}`);
                return;
            }
            try {
                await navigator.clipboard.writeText(value);
                this.showCopyToast(`${label} copied to clipboard`);
            } catch(e) {
                DialogUtils.alert(`${label}: ${value}`);
            }
        },
        showCopyToast(message) {
            this.copyToast = message;
            clearTimeout(this.copyToastTimeout);
            this.copyToastTimeout = setTimeout(() => {
                this.copyToast = null;
            }, 2500);
        },
        async onThemeChange() {
            await this.updateConfig({
                "theme": this.config.theme,
            });
        },
        async onAutoResendFailedMessagesWhenAnnounceReceivedChange() {
            await this.updateConfig({
                "auto_resend_failed_messages_when_announce_received": this.config.auto_resend_failed_messages_when_announce_received,
            });
        },
        async onAllowAutoResendingFailedMessagesWithAttachmentsChange() {
            await this.updateConfig({
                "allow_auto_resending_failed_messages_with_attachments": this.config.allow_auto_resending_failed_messages_with_attachments,
            });
        },
        async onAutoSendFailedMessagesToPropagationNodeChange() {
            await this.updateConfig({
                "auto_send_failed_messages_to_propagation_node": this.config.auto_send_failed_messages_to_propagation_node,
            });
        },
        async onShowSuggestedCommunityInterfacesChange() {
            await this.updateConfig({
                "show_suggested_community_interfaces": this.config.show_suggested_community_interfaces,
            });
        },
        async onLxmfPreferredPropagationNodeDestinationHashChange() {
            await this.updateConfig({
                "lxmf_preferred_propagation_node_destination_hash": this.config.lxmf_preferred_propagation_node_destination_hash,
            });
        },
        async onLxmfLocalPropagationNodeEnabledChange() {
            await this.updateConfig({
                "lxmf_local_propagation_node_enabled": this.config.lxmf_local_propagation_node_enabled,
            });
        },
        async onLxmfPreferredPropagationNodeAutoSyncIntervalSecondsChange() {
            await this.updateConfig({
                "lxmf_preferred_propagation_node_auto_sync_interval_seconds": this.config.lxmf_preferred_propagation_node_auto_sync_interval_seconds,
            });
        },
        async onLxmfInboundStampCostChange() {
            await this.updateConfig({
                "lxmf_inbound_stamp_cost": this.config.lxmf_inbound_stamp_cost,
            });
        },
        async onLxmfPropagationNodeStampCostChange() {
            await this.updateConfig({
                "lxmf_propagation_node_stamp_cost": this.config.lxmf_propagation_node_stamp_cost,
            });
        },
        async onIsTransportEnabledChange() {
            if(this.config.is_transport_enabled){
                try {
                    const response = await window.axios.post("/api/v1/reticulum/enable-transport");
                    DialogUtils.alert(response.data.message);
                } catch(e) {
                    DialogUtils.alert("Failed to enable transport mode!");
                    console.log(e);
                }
            } else {
                try {
                    const response = await window.axios.post("/api/v1/reticulum/disable-transport");
                    DialogUtils.alert(response.data.message);
                } catch(e) {
                    DialogUtils.alert("Failed to disable transport mode!");
                    console.log(e);
                }
            }
        },
        formatSecondsAgo: function(seconds) {
            return Utils.formatSecondsAgo(seconds);
        },
    },
}
</script>

<style scoped>
.glass-card {
    @apply bg-white/90 dark:bg-zinc-900/80 backdrop-blur border border-gray-200 dark:border-zinc-800 rounded-3xl shadow-lg flex flex-col;
}
.glass-card__header {
    @apply flex items-center justify-between gap-3 px-4 py-4 border-b border-gray-100/70 dark:border-zinc-800/80;
}
.glass-card__header h2 {
    @apply text-lg font-semibold text-gray-900 dark:text-white;
}
.glass-card__header p {
    @apply text-sm text-gray-600 dark:text-gray-400;
}
.glass-card__eyebrow {
    @apply text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400;
}
.glass-card__body {
    @apply px-4 py-4 text-gray-900 dark:text-gray-100;
}
.input-field {
    @apply bg-gray-50/90 dark:bg-zinc-800/80 border border-gray-200 dark:border-zinc-700 text-sm rounded-2xl focus:ring-2 focus:ring-blue-400 focus:border-blue-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 block w-full p-2.5 text-gray-900 dark:text-gray-100 transition;
}
.setting-toggle {
    @apply flex items-start gap-3 rounded-2xl border border-gray-200 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/70 px-3 py-3;
}
.setting-toggle input[type="checkbox"] {
    @apply w-4 h-4 mt-1 rounded border-gray-300 dark:border-zinc-600 text-blue-600 focus:ring-blue-500;
}
.setting-toggle__label {
    @apply flex-1 flex flex-col gap-0.5;
}
.setting-toggle__title {
    @apply text-sm font-semibold text-gray-900 dark:text-white;
}
.setting-toggle__description {
    @apply text-sm text-gray-600 dark:text-gray-300;
}
.setting-toggle__hint {
    @apply text-xs text-gray-500 dark:text-gray-400;
}
.primary-chip {
    @apply inline-flex items-center gap-x-1 rounded-full bg-blue-600/90 px-4 py-1.5 text-xs font-semibold text-white shadow hover:bg-blue-500 transition;
}
.info-callout {
    @apply rounded-2xl border border-blue-100 dark:border-blue-900/40 bg-blue-50/60 dark:bg-blue-900/20 px-3 py-3 text-blue-900 dark:text-blue-100;
}
.monospace-field {
    font-family: "Roboto Mono", monospace;
}
.address-card {
    @apply relative border border-gray-200 dark:border-zinc-800 rounded-2xl bg-white/80 dark:bg-zinc-900/70 p-4 space-y-2;
}
.address-card__label {
    @apply text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400;
}
.address-card__value {
    @apply text-sm text-gray-900 dark:text-white break-words pr-16;
}
.address-card__action {
    @apply absolute top-3 right-3 inline-flex items-center gap-1 rounded-full border border-gray-200 dark:border-zinc-700 px-3 py-1 text-xs font-semibold text-gray-700 dark:text-gray-100 bg-white/70 dark:bg-zinc-900/60 hover:border-blue-400 dark:hover:border-blue-500 transition;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
