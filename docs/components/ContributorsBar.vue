<script setup lang="ts">

const contributorImgSrc = `https://contrib.rocks/image?repo=LiteyukiStudio/nonebot-plugin-marshoai`
const contributorsUrl = `https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/graphs/contributors`
</script>

<template>
  <div class="contributor-bar">
    <a :href="contributorsUrl">
      <div class="contributor-list">
        <img :src=contributorImgSrc alt="Contributors">
      </div>
    </a>
  </div>
</template>

<style scoped>
.contributor-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>