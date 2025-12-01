<template>
    <div class="flex flex-col flex-1 overflow-hidden min-w-full sm:min-w-[500px] bg-gradient-to-br from-slate-50 via-slate-100 to-white dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-900">
        <div class="overflow-y-auto space-y-4 p-4 md:p-6 max-w-5xl mx-auto w-full">

            <div class="glass-card space-y-3">
                <div class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">Utilities</div>
                <div class="text-2xl font-semibold text-gray-900 dark:text-white">Power tools for operators</div>
                <div class="text-sm text-gray-600 dark:text-gray-300">
                    Diagnostics and firmware helpers ship with MeshChat so you can troubleshoot peers without leaving the console.
                </div>
            </div>

            <div class="grid gap-4 md:grid-cols-2">
                <RouterLink :to="{ name: 'ping' }" class="tool-card glass-card">
                    <div class="tool-card__icon bg-blue-50 text-blue-500 dark:bg-blue-900/30 dark:text-blue-200">
                        <MaterialDesignIcon icon-name="radar" class="w-6 h-6"/>
                    </div>
                    <div class="flex-1">
                        <div class="tool-card__title">Ping</div>
                        <div class="tool-card__description">Latency test for any LXMF destination hash with live status.</div>
                    </div>
                    <MaterialDesignIcon icon-name="chevron-right" class="tool-card__chevron"/>
                </RouterLink>

                <a target="_blank" href="/rnode-flasher/index.html" class="tool-card glass-card">
                    <div class="tool-card__icon bg-purple-50 text-purple-500 dark:bg-purple-900/30 dark:text-purple-200">
                        <img src="/rnode-flasher/reticulum_logo_512.png" class="w-8 h-8 rounded-full" alt="RNode"/>
                    </div>
                    <div class="flex-1">
                        <div class="tool-card__title">RNode Flasher</div>
                        <div class="tool-card__description">Flash and update RNode adapters without touching the command line.</div>
                    </div>
                    <MaterialDesignIcon icon-name="open-in-new" class="tool-card__chevron"/>
                </a>
            </div>

        </div>
    </div>
</template>

<script>
import MaterialDesignIcon from "../MaterialDesignIcon.vue";
export default {
    name: 'ToolsPage',
    components: {
        MaterialDesignIcon,
    },
}
</script>

<style scoped>
.tool-card {
    @apply flex items-center gap-4 hover:border-blue-400 dark:hover:border-blue-500 transition cursor-pointer;
}
.tool-card__icon {
    @apply w-12 h-12 rounded-2xl flex items-center justify-center;
}
.tool-card__title {
    @apply text-lg font-semibold text-gray-900 dark:text-white;
}
.tool-card__description {
    @apply text-sm text-gray-600 dark:text-gray-300;
}
.tool-card__chevron {
    @apply w-5 h-5 text-gray-400;
}
</style>
