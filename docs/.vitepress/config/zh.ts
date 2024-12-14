import {defineConfig} from 'vitepress'

export const zh = defineConfig({
    lang: "zh-Hans",
    title: "小棉智能",
    description: "可爱，智能且易扩展",
    themeConfig: {
        docFooter: {
            prev: '上一页',
            next: '下一页'
        },
        langMenuLabel: '语言',
        returnToTopLabel: '返回顶部',
        sidebarMenuLabel: '菜单',
        darkModeSwitchLabel: '主题',
        lightModeSwitchTitle: '轻色模式',
        darkModeSwitchTitle: '深色模式',
    },
})