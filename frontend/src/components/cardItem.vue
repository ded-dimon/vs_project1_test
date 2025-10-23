<template>
    <article
        class="rounded-md border-zinc-600 border-2 p-4 pt-2 w-56 relative bottom-0 hover:bottom-1 transform duration-150">
        <h2 class="font-semibold text-zinc-100">{{ item.title }}</h2>
        <div class="border-t border-zinc-800 my-2"></div>
        <div class="flex justify-between">
            <div>
                <p class="text-xs text-zinc-500">Цена:</p>
                <p class="font-bold text-amber-600">{{ item.price * 100 }} <span
                        class="text-xs font-normal text-zinc-500">руб</span></p>
            </div>

            <div>
                <p class="text-xs text-zinc-500">Рейтинг:</p>
                <p class="font-bold text-amber-600 flex justify-end">{{ item.rating }}
                    <StarIcon class="w-4 ml-1" />
                </p>
            </div>
        </div>
    </article>
</template>

<script setup>

import { StarIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
    item: Object
})


const item = props.item

</script>

<style scoped></style>