<script setup lang="ts">

const {data: word} = await useFetch('http://host.docker.internal:8000/api/hello_db/backend')

</script>
<template>
    <h1>Hello, {{ word.message }}</h1>
</template>
