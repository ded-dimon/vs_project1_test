<template>
    <div class="flex justify-center items-center" v-if="loading">
        <spinnerUI></spinnerUI>
    </div>

    <div class="flex flex-wrap w-full gap-4" v-else>
        <card-item v-for="item in []" :key="item.id" :item="item"></card-item>
    </div>
</template>

<script setup>
import { useRequest } from '@/hooks/useRequest';
import { useAppStore } from '@/store/app';
import { onMounted, ref, toRaw } from 'vue';
import CardItem from './cardItem.vue';

const { data, requestGet } = useRequest()

const loading = ref(false) // искуственная задержка
const appStore = useAppStore()

const fakeData = await requestGet('http://localhost:8000/categories/')
console.log(fakeData)
</script>

<style scoped></style>