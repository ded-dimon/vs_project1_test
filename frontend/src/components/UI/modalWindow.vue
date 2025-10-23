<template>
    <div v-show="isModalActive" @click="$emit('update:isModalActive', false)"
        class="fixed flex items-center justify-center h-screen w-screen transform duration-150">
        <div :class="isModalActive ? 'top-0 opacity-100' : 'top-16 opacity-0'"
            class="relative bg-zinc-600 rounded-md border-zinc-400 border-2 transform duration-150">
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
defineOptions({
    name: 'modalWindowUI'
})
const props = defineProps({
    isModalActive: Boolean, default: false
})

if (props.isModalActive) {

}
</script>

<style scoped>
</style>