import { VitePressSidebarOptions } from "vitepress-sidebar/types";

export const gitea = {
  svg: '<svg t="1725391346807" class="icon" viewBox="0 0 1025 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5067" width="256" height="256"><path d="M1004.692673 466.396616l-447.094409-447.073929c-25.743103-25.763582-67.501405-25.763582-93.264987 0l-103.873521 103.873521 78.171378 78.171378c12.533635-6.00058 26.562294-9.359266 41.389666-9.359266 53.02219 0 96.00928 42.98709 96.00928 96.00928 0 14.827372-3.358686 28.856031-9.359266 41.389666l127.97824 127.97824c12.533635-6.00058 26.562294-9.359266 41.389666-9.359266 53.02219 0 96.00928 42.98709 96.00928 96.00928s-42.98709 96.00928-96.00928 96.00928-96.00928-42.98709-96.00928-96.00928c0-14.827372 3.358686-28.856031 9.359266-41.389666l-127.97824-127.97824c-3.051489 1.454065-6.184898 2.744293-9.379746 3.870681l0 266.97461c37.273227 13.188988 63.99936 48.721433 63.99936 90.520695 0 53.02219-42.98709 96.00928-96.00928 96.00928s-96.00928-42.98709-96.00928-96.00928c0-41.799262 26.726133-77.331707 63.99936-90.520695l0-266.97461c-37.273227-13.188988-63.99936-48.721433-63.99936-90.520695 0-14.827372 3.358686-28.856031 9.359266-41.389666l-78.171378-78.171378-295.892081 295.871601c-25.743103 25.784062-25.743103 67.542365 0 93.285467l447.114889 447.073929c25.743103 25.743103 67.480925 25.743103 93.264987 0l445.00547-445.00547c25.763582-25.763582 25.763582-67.542365 0-93.285467z" fill="#a2d8f4" p-id="5068"></path></svg>',
};

export const defaultLang = "zh";

const commonSidebarOptions: VitePressSidebarOptions = {
  collapsed: true,
  convertSameNameSubFileToGroupIndexPage: true,
  useTitleFromFrontmatter: true,
  useFolderTitleFromIndexFile: false,
  useFolderLinkFromIndexFile: true,
  useTitleFromFileHeading: true,
  rootGroupText: "MARSHOAI",
  includeFolderIndexFile: true,
  sortMenusByFrontmatterOrder: true,
};

export function generateSidebarConfig(): VitePressSidebarOptions[] {
  let sections = ["dev", "start"];
  let languages = ["zh", "en"];
  let ret: VitePressSidebarOptions[] = [];
  for (let language of languages) {
    for (let section of sections) {
      if (language === defaultLang) {
        ret.push({
          basePath: `/${section}/`,
          scanStartPath: `docs/${language}/${section}`,
          resolvePath: `/${section}/`,
          ...commonSidebarOptions,
        });
      } else {
        ret.push({
          basePath: `/${language}/${section}/`,
          scanStartPath: `docs/${language}/${section}`,
          resolvePath: `/${language}/${section}/`,
          ...commonSidebarOptions,
        });
      }
    }
  }
  return ret;
}

export const ThemeConfig = {
  getEditLink: (
    editPageText: string
  ): { pattern: (params: { filePath: string }) => string; text: string } => {
    return {
      pattern: ({ filePath }: { filePath: string }): string => {
        if (!filePath) {
          throw new Error("filePath is undefined");
        }
        const regex = /^(dev\/api|[^\/]+\/dev\/api)/;
        if (regex.test(filePath)) {
          filePath = filePath
            .replace(regex, "")
            .replace("index.md", "__init__.py")
            .replace(".md", ".py");
          const fileName = filePath.split("/").pop();
          const parentFolder = filePath.split("/").slice(-2, -1)[0];
          if (
            fileName &&
            parentFolder &&
            fileName.split(".")[0] === parentFolder
          ) {
            filePath =
              filePath.split("/").slice(0, -1).join("/") + "/__init__.py";
          }
          return `https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/${filePath}`;
        } else {
          return `https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/docs/${filePath}`;
        }
      },
      text: editPageText,
    };
  },

  getOutLine: (label: string): { label: string; level: [number, number] } => {
    return {
      label: label,
      level: [2, 6],
    };
  },
};
