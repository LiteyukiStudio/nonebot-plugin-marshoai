import { defineConfig } from 'vitepress'
import {zh} from './zh'
import {en} from './en'
import { gitea } from './common'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    head: [
        ['link', { rel: 'icon', type: 'image/x-icon', href: './favicon.ico' }],
    ],
    rewrites: {
        [`zh/:rest*`]: ":rest*",
    },
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        logo: {
            light: './marsho-full.svg',
            dark: './marsho-full.svg',
            alt: 'Marsho Logo'
        },

        socialLinks: [
            { icon: 'github', link: 'https://github.com/LiteyukiStudio/nonebot-plugin-marshoai' },
            { icon: gitea, link: 'https://git.liteyuki.icu/LiteyukiStudio/nonebot-plugin-marshoai'}
        ]
    },
    locales: {
        root: { label: "简体中文", ...zh },
        en: { label: "English", ...en },
    },
})
