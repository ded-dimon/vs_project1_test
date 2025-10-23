<template>
    <h2 class="text-zinc-200 font-semibold text-3xl">
        Взгляните на наши предложения
    </h2>
     <div class="border-t border-zinc-800 my-4"></div> 
    <ListItems></ListItems>

</template>

<script>
import ListItems from '@/components/listItems.vue';

    export default {
        components:{
            ListItems
        }
    }
</script>

<style scoped>

</style>