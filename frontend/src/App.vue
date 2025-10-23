<template>
    <header class="fixed bg-zinc-800 flex justify-between items-center px-4 w-screen h-14">
      <h1 class="font-black text-zinc-200">Kragen</h1>
      <nav class="flex text-zinc-200 gap-4 items-center">
        <a class="no-underline hover:underline" href="">О нас</a>
        <a class="no-underline hover:underline">Категории</a>
        <button @click="modalActive = true" class="transition duration-150 bg-red-500 px-5 py-1 border-2 border-red-500 rounded-md text-red-50 font-semibold hover:bg-red-600" href="">Войти</button>
        <button class="transition duration-150 px-5 py-1 text-red-500 rounded-md border-2 border-red-500 font-semibold hover:bg-red-600 hover:text-red-50" href="">Зарегестрироваться</button>
      </nav>
    </header>
    <modalWindowUI  v-model:isModalActive="modalActive"></modalWindowUI>
    <main class="pt-20 bg-zinc-700 h-screen w-screen p-7">
        <router-view></router-view>
    </main>
</template>

<script setup>
import { ref } from 'vue';

const modalActive = ref(true)
</script>

<style>

</style>