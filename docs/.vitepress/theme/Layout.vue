<!-- 该部分内容来自https://github.com/NapNeko/NapCatDocs，并遵循原仓库 MIT LICENSE 进行修改及分发，详细请参阅 ./LICENSE -->

<script setup>
import DefaultTheme from 'vitepress/theme'

const { Layout } = DefaultTheme
</script>

<template>
    <Layout>
        <template #home-hero-before>
            <div
                class="absolute flex flex-col z-[40] w-full !max-w-full items-center justify-center bg-transparent transition-bg overflow-hidden h-[60vh] -top-16 pointer-events-none opacity-[.35] dark:opacity-50">
                <div class="jumbo absolute opacity-60 animate"></div>
            </div>
        </template>
    </Layout>
</template>

<style>
.opacity-\[\.35\] {
    opacity: .35;
}

.bg-transparent {
    background-color: transparent;
}

.overflow-hidden {
    overflow: hidden;
}

.justify-center {
    justify-content: center;
}

.items-center {
    align-items: center;
}

.flex-col {
    flex-direction: column;
}

.\!max-w-full {
    max-width: 100% !important;
}

.w-full {
    width: 100%;
}

.h-\[60vh\] {
    height: 60vh;
}

.flex {
    display: flex;
}

.z-\[40\] {
    z-index: 40;
}

.-top-16 {
    top: -4rem;
}

.absolute {
    position: absolute;
}

.pointer-events-none {
    pointer-events: none;
}

.jumbo {
    --stripes: repeating-linear-gradient(100deg, #fff 0%, #fff 7%, transparent 10%, transparent 12%, #fff 16%);
    --stripesDark: repeating-linear-gradient(100deg, #000 0%, #000 7%, transparent 10%, transparent 12%, #000 16%);
    --rainbow: repeating-linear-gradient(100deg, #60a5fa 10%, #ff6666 16%, #ff7ff4 22%, #60a5fa 30%);
    contain: strict;
    contain-intrinsic-size: 100vw 40vh;
    background-image: var(--stripes), var(--rainbow);
    background-size: 300%, 200%;
    background-position: 50% 50%, 50% 50%;
    height: inherit;
    -webkit-transform: translateZ(0);
    -webkit-perspective: 1000;
    -webkit-backface-visibility: hidden;
    filter: invert(100%);
    -webkit-mask-image: radial-gradient(ellipse at 100% 0%, black 40%, transparent 70%);
    mask-image: radial-gradient(ellipse at 100% 0%, black 40%, transparent 70%);
    pointer-events: none;
}

.opacity-60 {
    opacity: .6;
}

.absolute {
    position: absolute;
}

@keyframes jumbo-5f0d2d0c {
    0% {
        background-position: 50% 50%,50% 50%
    }

    to {
        background-position: 350% 50%,350% 50%
    }
}

.jumbo:after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-image: var(--stripes),var(--rainbow);
    background-size: 200%,100%;
    mix-blend-mode: difference
}

.animate.jumbo:after {
    animation: jumbo-5f0d2d0c 90s linear infinite
}
</style>