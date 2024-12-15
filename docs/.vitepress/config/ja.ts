import {defineConfig} from 'vitepress'

export const ja = defineConfig({
    lang: "ja-JP",
    title: "Marsho AI",
    description: "かわいくて、賢くて、拡張しやすい",
    themeConfig: {
        docFooter: {
            prev: '前へ',
            next: '次へ'
        },
        nav: [
            {text: 'ホーム', link: '/ja'},
            {text: '使用方法', link: '/ja/start/install'},
            {text: '開発', link: '/ja/dev/extension'},
        ],
        langMenuLabel: '言語',
        returnToTopLabel: 'トップへ戻る',
        sidebarMenuLabel: 'オプション',
        darkModeSwitchLabel: 'テーマ',
        lightModeSwitchTitle: 'ライト',
        darkModeSwitchTitle: 'ダーク',
    },
})