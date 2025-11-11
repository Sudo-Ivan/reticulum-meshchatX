<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] dark:bg-zinc-950">
        <div class="overflow-y-auto space-y-2 p-2">

            <!-- app info -->
            <div v-if="appInfo" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">App Info</div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">

                    <!-- version -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Versions</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400">
                                MeshChat v{{ appInfo.version }} • RNS v{{ appInfo.rns_version }} • LXMF v{{ appInfo.lxmf_version }} • Python v{{ appInfo.python_version }}
                            </div>
                        </div>
                        <div class="hidden sm:block mx-2 my-auto">
                            <a target="_blank" 
                                href="https://github.com/liamcottle/reticulum-meshchat/releases" 
                                type="button" 
                                class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-600">
                                Check for Updates
                            </a>
                        </div>
                    </div>

                    <!-- reticulum config path -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Reticulum Config Path</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400 break-all">{{ appInfo.reticulum_config_path }}</div>
                        </div>
                        <div v-if="isElectron" class="mx-2 my-auto">
                            <button @click="showReticulumConfigFile" 
                                type="button" 
                                class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-600">
                                Show in Folder
                            </button>
                        </div>
                    </div>

                    <!-- database path -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Database Path</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400 break-all">{{ appInfo.database_path }}</div>
                        </div>
                        <div v-if="isElectron" class="mx-2 my-auto">
                            <button @click="showDatabaseFile" 
                                type="button" 
                                class="my-auto inline-flex items-center gap-x-1 rounded-md bg-gray-500 dark:bg-zinc-700 px-2 py-1 text-sm font-semibold text-white shadow-sm hover:bg-gray-400 dark:hover:bg-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-500 dark:focus-visible:outline-zinc-600">
                                Show in Folder
                            </button>
                        </div>
                    </div>

                    <!-- database file size -->
                    <div class="p-1">
                        <div>Database File Size</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatBytes(appInfo.database_file_size) }}</div>
                    </div>

                </div>
            </div>

            <!-- system resources -->
            <div v-if="appInfo && appInfo.memory_usage" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">
                    System Resources
                    <span class="ml-auto text-xs text-green-600 dark:text-green-400 flex items-center">
                        <span class="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span>
                        Live
                    </span>
                </div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">

                    <!-- memory usage -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Memory Usage (RSS)</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatBytes(appInfo.memory_usage.rss) }}</div>
                        </div>
                    </div>

                    <!-- virtual memory -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Virtual Memory Size</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatBytes(appInfo.memory_usage.vms) }}</div>
                        </div>
                    </div>

                </div>
            </div>

            <!-- network statistics -->
            <div v-if="appInfo && appInfo.network_stats" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">
                    Network Statistics
                    <span class="ml-auto text-xs text-green-600 dark:text-green-400 flex items-center">
                        <span class="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span>
                        Live
                    </span>
                </div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">

                    <!-- bytes sent -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Data Sent</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatBytes(appInfo.network_stats.bytes_sent) }}</div>
                        </div>
                    </div>

                    <!-- bytes received -->
                    <div class="flex p-1">
                        <div class="mr-auto">
                            <div>Data Received</div>
                            <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatBytes(appInfo.network_stats.bytes_recv) }}</div>
                        </div>
                    </div>

                    <!-- packets sent -->
                    <div class="p-1">
                        <div>Packets Sent</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatNumber(appInfo.network_stats.packets_sent) }}</div>
                    </div>

                    <!-- packets received -->
                    <div class="p-1">
                        <div>Packets Received</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatNumber(appInfo.network_stats.packets_recv) }}</div>
                    </div>

                </div>
            </div>

            <!-- reticulum statistics -->
            <div v-if="appInfo && appInfo.reticulum_stats" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">
                    Reticulum Statistics
                    <span class="ml-auto text-xs text-green-600 dark:text-green-400 flex items-center">
                        <span class="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span>
                        Live
                    </span>
                </div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">

                    <!-- total paths -->
                    <div class="p-1">
                        <div>Total Paths</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatNumber(appInfo.reticulum_stats.total_paths) }}</div>
                    </div>

                    <!-- announces per second -->
                    <div class="p-1">
                        <div>Announces per Second</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatNumber(appInfo.reticulum_stats.announces_per_second) }}</div>
                    </div>

                    <!-- announces per minute -->
                    <div class="p-1">
                        <div>Announces per Minute</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatNumber(appInfo.reticulum_stats.announces_per_minute) }}</div>
                    </div>

                    <!-- announces per hour -->
                    <div class="p-1">
                        <div>Announces per Hour</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ formatNumber(appInfo.reticulum_stats.announces_per_hour) }}</div>
                    </div>

                </div>
            </div>

            <!-- download statistics -->
            <div v-if="appInfo && appInfo.download_stats" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">
                    Download Statistics
                    <span class="ml-auto text-xs text-green-600 dark:text-green-400 flex items-center">
                        <span class="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span>
                        Live
                    </span>
                </div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">

                    <!-- average download speed -->
                    <div class="p-1">
                        <div>Average Download Speed</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            <span v-if="appInfo.download_stats.avg_download_speed_bps !== null">
                                {{ formatBytesPerSecond(appInfo.download_stats.avg_download_speed_bps) }}
                            </span>
                            <span v-else>No downloads yet</span>
                        </div>
                    </div>

                </div>
            </div>

            <!-- reticulum status -->
            <div v-if="appInfo" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">Reticulum Status</div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">

                    <!-- instance mode -->
                    <div class="p-1">
                        <div>Instance Mode</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            <span v-if="appInfo.is_connected_to_shared_instance" class="text-orange-600 dark:text-orange-400">Connected to Shared Instance</span>
                            <span v-else class="text-green-600 dark:text-green-400">Running as Standalone Instance</span>
                        </div>
                    </div>

                    <!-- transport mode -->
                    <div class="p-1">
                        <div>Transport Mode</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">
                            <span v-if="appInfo.is_transport_enabled" class="text-green-600 dark:text-green-400">Transport Enabled</span>
                            <span v-else class="text-orange-600 dark:text-orange-400">Transport Disabled</span>
                        </div>
                    </div>

                </div>
            </div>

            <!-- my addresses -->
            <div v-if="config" class="bg-white dark:bg-zinc-900 rounded shadow">
                <div class="flex border-b border-gray-300 dark:border-zinc-700 text-gray-700 dark:text-zinc-200 p-2 font-semibold">My Addresses</div>
                <div class="divide-y divide-gray-200 dark:divide-zinc-800 text-gray-900 dark:text-zinc-200">
                    <div class="p-1">
                        <div>Identity Hash</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ config.identity_hash }}</div>
                    </div>
                    <div class="p-1">
                        <div>LXMF Address</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ config.lxmf_address_hash }}</div>
                    </div>
                    <div class="p-1">
                        <div>LXMF Propagation Node Address</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ config.lxmf_local_propagation_node_address_hash }}</div>
                    </div>
                    <div class="p-1">
                        <div>Audio Call Address</div>
                        <div class="text-sm text-gray-700 dark:text-zinc-400">{{ config.audio_call_address_hash }}</div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import Utils from "../../js/Utils";
import ElectronUtils from "../../js/ElectronUtils";
export default {
    name: 'AboutPage',
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
    },
    computed: {
        isElectron() {
            return ElectronUtils.isElectron();
        },
    },
}
</script>
