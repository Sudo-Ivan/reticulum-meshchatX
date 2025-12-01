<template>
    <button type="button" class="text-gray-700 bg-gray-100 dark:bg-zinc-600 dark:text-white dark:hover:bg-zinc-700 dark:focus-visible:outline-zinc-500 hover:bg-gray-200 p-2 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0">
        <slot/>
    </button>
</template>

<script>
export default {
    name: 'IconButton',
}
</script>
