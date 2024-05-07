/**
 * 一度、「初期値」を描画後に「変更」に変更する
 */ 
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const word = ref('初期値')

onMounted(() => {
    word.value = '変更'
})
</script>
<template>
    <h1>Hello, {{ word }}</h1>
</template>
