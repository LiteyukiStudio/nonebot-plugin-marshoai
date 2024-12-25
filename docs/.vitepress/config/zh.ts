import {defineConfig} from 'vitepress'
import { ThemeConfig } from './common'

export const zh = defineConfig({
    lang: "zh-Hans",
    title: "小棉智能",
    description: "可爱，智能且易扩展",
    themeConfig: {
        docFooter: {
            prev: '上一页',
            next: '下一页'
        },
        nav: [
            {text: '家', link: '/'},
            {text: '使用', link: '/start/install-old'},
            {text: '开发', link: '/dev/extension'},
        ],
        editLink: ThemeConfig.getEditLink('编辑此页面'),
        langMenuLabel: '语言',
        returnToTopLabel: '返回顶部',
        sidebarMenuLabel: '菜单',
        darkModeSwitchLabel: '主题',
        lightModeSwitchTitle: '轻色模式',
        darkModeSwitchTitle: '深色模式',
        footer: {
            message: "文档完善中，欢迎提出建议或帮助我们完善。",
            copyright: '© 2024 <a href="https://liteyuki.icu" target="_blank">Liteyuki Studio</a>',
        }
    },
})