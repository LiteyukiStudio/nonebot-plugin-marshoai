import{_ as i,c as a,ae as t,o as n}from"./chunks/framework.BzDBnRMZ.js";const u=JSON.parse('{"title":"utils","description":"","frontmatter":{"title":"utils","order":100},"headers":[],"relativePath":"en/dev/api/plugin/utils.md","filePath":"en/dev/api/plugin/utils.md","lastUpdated":1734175019000}'),e={name:"en/dev/api/plugin/utils.md"};function l(p,s,h,r,o,k){return n(),a("div",null,s[0]||(s[0]=[t('<h1 id="module-nonebot-plugin-marshoai-plugin-utils" tabindex="-1"><strong>Module</strong> <code>nonebot_plugin_marshoai.plugin.utils</code> <a class="header-anchor" href="#module-nonebot-plugin-marshoai-plugin-utils" aria-label="Permalink to &quot;**Module** `nonebot_plugin_marshoai.plugin.utils`&quot;">​</a></h1><hr><h3 id="func-path-to-module-name-path-path-str" tabindex="-1"><em><strong>func</strong></em> <code>path_to_module_name(path: Path) -&gt; str</code> <a class="header-anchor" href="#func-path-to-module-name-path-path-str" aria-label="Permalink to &quot;***func*** `path_to_module_name(path: Path) -&gt; str`&quot;">​</a></h3><p><strong>Description</strong>: 转换路径为模块名</p><p><strong>Arguments</strong>:</p><blockquote><ul><li>path: 路径a/b/c/d -&gt; a.b.c.d</li></ul></blockquote><p><strong>Return</strong>: str: 模块名</p><details><summary><b>Source code</b> or <a href="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/utils.py#L6" target="_blank">View on GitHub</a></summary><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> path_to_module_name</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(path: Path) -&gt; </span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">str</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>\n<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    rel_path </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> path.resolve().relative_to(Path.cwd().resolve())</span></span>\n<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    if</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> rel_path.stem </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">==</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &#39;__init__&#39;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>\n<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &#39;.&#39;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.join(rel_path.parts[:</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">-</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">])</span></span>\n<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    else</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>\n<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;"> &#39;.&#39;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">.join(rel_path.parts[:</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">-</span><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">1</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">] </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">+</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> (rel_path.stem,))</span></span></code></pre></div></details><hr><h3 id="func-parse-function-docsring" tabindex="-1"><em><strong>func</strong></em> <code>parse_function_docsring()</code> <a class="header-anchor" href="#func-parse-function-docsring" aria-label="Permalink to &quot;***func*** `parse_function_docsring()`&quot;">​</a></h3><details><summary><b>Source code</b> or <a href="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/utils.py#L21" target="_blank">View on GitHub</a></summary><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> parse_function_docsring</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">():</span></span>\n<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    pass</span></span></code></pre></div></details>',11)]))}const g=i(e,[["render",l]]);export{u as __pageData,g as default};