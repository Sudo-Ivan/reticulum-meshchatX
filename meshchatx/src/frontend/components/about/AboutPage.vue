<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] bg-gradient-to-br from-slate-50 via-slate-100 to-white dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-900">
        <div class="flex-1 overflow-y-auto w-full px-4 md:px-8 py-6">
            <div class="space-y-4 w-full max-w-6xl mx-auto">

            <div v-if="appInfo" class="glass-card">
                <div class="flex flex-col gap-4 md:flex-row md:items-center">
                    <div class="flex-1 space-y-2">
                        <div class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">About</div>
                        <div class="text-3xl font-semibold text-gray-900 dark:text-white">Reticulum MeshChatX</div>
                        <div class="text-sm text-gray-600 dark:text-gray-300">
                            v{{ appInfo.version }} • RNS {{ appInfo.rns_version }} • LXMF {{ appInfo.lxmf_version }} • Python {{ appInfo.python_version }}
                        </div>
                    </div>
                    <div v-if="isElectron" class="flex flex-col sm:flex-row gap-2">
                        <button @click="relaunch" type="button" class="primary-chip px-4 py-2 text-sm justify-center">
                            <MaterialDesignIcon icon-name="restart" class="w-4 h-4"/>
                            Restart App
                        </button>
                    </div>
                </div>
                <div class="grid gap-3 sm:grid-cols-3 mt-4 text-sm text-gray-700 dark:text-gray-300">
                    <div>
                        <div class="glass-label">Config path</div>
                        <div class="monospace-field break-all">{{ appInfo.reticulum_config_path }}</div>
                        <button v-if="isElectron" @click="showReticulumConfigFile" type="button" class="secondary-chip mt-2 text-xs">
                            <MaterialDesignIcon icon-name="folder" class="w-4 h-4"/>
                            Reveal
                        </button>
                    </div>
                    <div>
                        <div class="glass-label">Database path</div>
                        <div class="monospace-field break-all">{{ appInfo.database_path }}</div>
                        <button v-if="isElectron" @click="showDatabaseFile" type="button" class="secondary-chip mt-2 text-xs">
                            <MaterialDesignIcon icon-name="database" class="w-4 h-4"/>
                            Reveal
                        </button>
                    </div>
                    <div>
                        <div class="glass-label">Database size</div>
                        <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ formatBytes(appInfo.database_file_size) }}</div>
                    </div>
                </div>
            </div>

            <div class="grid gap-4 lg:grid-cols-2">
                <div v-if="appInfo?.memory_usage" class="glass-card space-y-3">
                    <header class="flex items-center gap-2">
                        <MaterialDesignIcon icon-name="chip" class="w-5 h-5 text-blue-500"/>
                        <div>
                            <div class="text-lg font-semibold text-gray-900 dark:text-white">System Resources</div>
                            <div class="text-xs text-emerald-500 flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                Live
                            </div>
                        </div>
                    </header>
                    <div class="metric-row">
                        <div>
                            <div class="glass-label">Memory (RSS)</div>
                            <div class="metric-value">{{ formatBytes(appInfo.memory_usage.rss) }}</div>
                        </div>
                        <div>
                            <div class="glass-label">Virtual Memory</div>
                            <div class="metric-value">{{ formatBytes(appInfo.memory_usage.vms) }}</div>
                        </div>
                    </div>
                </div>

                <div v-if="appInfo?.network_stats" class="glass-card space-y-3">
                    <header class="flex items-center gap-2">
                        <MaterialDesignIcon icon-name="access-point-network" class="w-5 h-5 text-purple-500"/>
                        <div>
                            <div class="text-lg font-semibold text-gray-900 dark:text-white">Network Stats</div>
                            <div class="text-xs text-emerald-500 flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                Live
                            </div>
                        </div>
                    </header>
                    <div class="metric-row">
                        <div>
                            <div class="glass-label">Sent</div>
                            <div class="metric-value">{{ formatBytes(appInfo.network_stats.bytes_sent) }}</div>
                        </div>
                        <div>
                            <div class="glass-label">Received</div>
                            <div class="metric-value">{{ formatBytes(appInfo.network_stats.bytes_recv) }}</div>
                        </div>
                    </div>
                    <div class="metric-row">
                        <div>
                            <div class="glass-label">Packets Sent</div>
                            <div class="metric-value">{{ formatNumber(appInfo.network_stats.packets_sent) }}</div>
                        </div>
                        <div>
                            <div class="glass-label">Packets Received</div>
                            <div class="metric-value">{{ formatNumber(appInfo.network_stats.packets_recv) }}</div>
                        </div>
                    </div>
                </div>

                <div v-if="appInfo?.reticulum_stats" class="glass-card space-y-3">
                    <header class="flex items-center gap-2">
                        <MaterialDesignIcon icon-name="diagram-projector" class="w-5 h-5 text-indigo-500"/>
                        <div>
                            <div class="text-lg font-semibold text-gray-900 dark:text-white">Reticulum Stats</div>
                            <div class="text-xs text-emerald-500 flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                Live
                            </div>
                        </div>
                    </header>
                    <div class="metric-grid">
                        <div>
                            <div class="glass-label">Total Paths</div>
                            <div class="metric-value">{{ formatNumber(appInfo.reticulum_stats.total_paths) }}</div>
                        </div>
                        <div>
                            <div class="glass-label">Announces / sec</div>
                            <div class="metric-value">{{ formatNumber(appInfo.reticulum_stats.announces_per_second) }}</div>
                        </div>
                        <div>
                            <div class="glass-label">Announces / min</div>
                            <div class="metric-value">{{ formatNumber(appInfo.reticulum_stats.announces_per_minute) }}</div>
                        </div>
                        <div>
                            <div class="glass-label">Announces / hr</div>
                            <div class="metric-value">{{ formatNumber(appInfo.reticulum_stats.announces_per_hour) }}</div>
                        </div>
                    </div>
                </div>

                <div v-if="appInfo?.download_stats" class="glass-card space-y-3">
                    <header class="flex items-center gap-2">
                        <MaterialDesignIcon icon-name="download" class="w-5 h-5 text-sky-500"/>
                        <div>
                            <div class="text-lg font-semibold text-gray-900 dark:text-white">Download Activity</div>
                            <div class="text-xs text-emerald-500 flex items-center gap-1">
                                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                Live
                            </div>
                        </div>
                    </header>
                    <div class="metric-value">
                        <span v-if="appInfo.download_stats.avg_download_speed_bps !== null">
                            {{ formatBytesPerSecond(appInfo.download_stats.avg_download_speed_bps) }}
                        </span>
                        <span v-else class="text-sm text-gray-500">No downloads yet</span>
                    </div>
                </div>
            </div>

            <div v-if="appInfo" class="glass-card space-y-3">
                <div class="text-lg font-semibold text-gray-900 dark:text-white">Runtime Status</div>
                <div class="flex flex-wrap gap-3">
                    <span :class="statusPillClass(!appInfo.is_connected_to_shared_instance)">
                        <MaterialDesignIcon icon-name="server" class="w-4 h-4"/>
                        {{ appInfo.is_connected_to_shared_instance ? 'Shared Instance' : 'Standalone Instance' }}
                    </span>
                    <span :class="statusPillClass(appInfo.is_transport_enabled)">
                        <MaterialDesignIcon icon-name="transit-connection" class="w-4 h-4"/>
                        {{ appInfo.is_transport_enabled ? 'Transport Enabled' : 'Transport Disabled' }}
                    </span>
                </div>
            </div>

            <div v-if="config" class="glass-card space-y-4">
                <div class="text-lg font-semibold text-gray-900 dark:text-white">Identity & Addresses</div>
                <div class="grid gap-3 md:grid-cols-2">
                    <div class="address-card">
                        <div class="glass-label">Identity Hash</div>
                        <div class="monospace-field break-all">{{ config.identity_hash }}</div>
                        <button @click="copyValue(config.identity_hash, 'Identity Hash')" type="button" class="secondary-chip mt-3 text-xs">
                            <MaterialDesignIcon icon-name="content-copy" class="w-4 h-4"/>
                            Copy
                        </button>
                    </div>
                    <div class="address-card">
                        <div class="glass-label">LXMF Address</div>
                        <div class="monospace-field break-all">{{ config.lxmf_address_hash }}</div>
                        <button @click="copyValue(config.lxmf_address_hash, 'LXMF Address')" type="button" class="secondary-chip mt-3 text-xs">
                            <MaterialDesignIcon icon-name="account-network" class="w-4 h-4"/>
                            Copy
                        </button>
                    </div>
                    <div class="address-card">
                        <div class="glass-label">Propagation Node</div>
                        <div class="monospace-field break-all">{{ config.lxmf_local_propagation_node_address_hash || '—' }}</div>
                    </div>
                    <div class="address-card">
                        <div class="glass-label">Audio Call Address</div>
                        <div class="monospace-field break-all">{{ config.audio_call_address_hash || '—' }}</div>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import ElectronUtils from "../../js/ElectronUtils";
import MaterialDesignIcon from "../MaterialDesignIcon.vue";
import DialogUtils from "../../js/DialogUtils";
export default {
    name: 'AboutPage',
    components: {
        MaterialDesignIcon,
    },
    data() {
        return {
            appInfo: null,
            config: null,
            updateInterval: null,
        };
    },
    mounted() {
        this.getAppInfo();
        this.getConfig();
        // Update stats every 5 seconds
        this.updateInterval = setInterval(() => {
            this.getAppInfo();
        }, 5000);
    },
    beforeUnmount() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    },
    methods: {
        async getAppInfo() {
            try {
                const response = await window.axios.get("/api/v1/app/info");
                this.appInfo = response.data.app_info;
            } catch(e) {
                // do nothing if failed to load app info
                console.log(e);
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
        async copyValue(value, label) {
            if(!value){
                return;
            }
            try {
                await navigator.clipboard.writeText(value);
                DialogUtils.toast?.(`${label} copied`) ?? DialogUtils.alert(`${label} copied to clipboard`);
            } catch(e) {
                DialogUtils.alert(`Failed to copy ${label}`);
            }
        },
        relaunch() {
            ElectronUtils.relaunch();
        },
        showReticulumConfigFile() {
            const reticulumConfigPath = this.appInfo.reticulum_config_path;
            if(reticulumConfigPath){
                ElectronUtils.showPathInFolder(reticulumConfigPath);
            }
        },
        showDatabaseFile() {
            const databasePath = this.appInfo.database_path;
            if(databasePath){
                ElectronUtils.showPathInFolder(databasePath);
            }
        },
        formatBytes: function(bytes) {
            return Utils.formatBytes(bytes);
        },
        formatNumber: function(num) {
            return Utils.formatNumber(num);
        },
        formatBytesPerSecond: function(bytesPerSecond) {
            return Utils.formatBytesPerSecond(bytesPerSecond);
        },
        statusPillClass(isGood) {
            return isGood
                ? "inline-flex items-center gap-1 rounded-full bg-emerald-100 text-emerald-700 px-3 py-1 text-xs font-semibold"
                : "inline-flex items-center gap-1 rounded-full bg-orange-100 text-orange-700 px-3 py-1 text-xs font-semibold";
        },
    },
    computed: {
        isElectron() {
            return ElectronUtils.isElectron();
        },
    },
}
</script>
