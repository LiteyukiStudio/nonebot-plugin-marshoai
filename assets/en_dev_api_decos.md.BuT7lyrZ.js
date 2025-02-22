import{_ as i,c as a,o as n,ae as e}from"./chunks/framework.BHrE6nLq.js";const c=JSON.parse('{"title":"decos","description":"","frontmatter":{"title":"decos","order":100},"headers":[],"relativePath":"en/dev/api/decos.md","filePath":"en/dev/api/decos.md","lastUpdated":null}'),t={name:"en/dev/api/decos.md"};function h(l,s,p,k,r,d){return n(),a("div",null,s[0]||(s[0]=[e(`<h1 id="module-nonebot-plugin-marshoai-decos" tabindex="-1"><strong>Module</strong> <code>nonebot_plugin_marshoai.decos</code> <a class="header-anchor" href="#module-nonebot-plugin-marshoai-decos" aria-label="Permalink to &quot;**Module** \`nonebot_plugin_marshoai.decos\`&quot;">​</a></h1><hr><h3 id="func-from-cache-key" tabindex="-1"><em><strong>func</strong></em> <code>from_cache(key)</code> <a class="header-anchor" href="#func-from-cache-key" aria-label="Permalink to &quot;***func*** \`from_cache(key)\`&quot;">​</a></h3><details><summary><b>Source code</b> or <a href="https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/decos.py#L4" target="_blank">View on GitHub</a></summary><div class="language-python vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">python</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> from_cache</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(key):</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">    def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> decorator</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(func):</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        def</span><span style="--shiki-light:#6F42C1;--shiki-dark:#B392F0;"> wrapper</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">(</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">*</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">args, </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">**</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">kwargs):</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">            cached </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> cache.get(key)</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">            if</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> cached:</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">                return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> cached</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">            else</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">:</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                result </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">=</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> func(</span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">*</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">args, </span><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">**</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">kwargs)</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">                cache.set(key, result)</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">                return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> result</span></span>
<span class="line"><span style="--shiki-light:#D73A49;--shiki-dark:#F97583;">        return</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> wrapper</span></span></code></pre></div></details>`,4)]))}const E=i(t,[["render",h]]);export{c as __pageData,E as default};
