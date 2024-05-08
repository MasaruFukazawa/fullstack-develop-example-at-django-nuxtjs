<script setup lang="ts">
import { ref, onMounted } from 'vue'

const ver = ref(1)
const {data: word} = await useFetch('http://host.docker.internal:8000/api/hello/backend')

</script>
<template>
    <h1>Hello, {{ word.message }} ver{{ ver }}</h1>
</template>
