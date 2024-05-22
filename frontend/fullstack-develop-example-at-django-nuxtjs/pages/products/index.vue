<script setup lang="ts">
import { ref } from 'vue'

const { data: products, pending, error, refresh } = await useFetch('http://host.docker.internal:8000/api/inventory/products/')

</script>

<template>
    <UContainer>
        <h2>商品一覧</h2>
        <UTable :rows="products" />
    </UContainer>
</template>