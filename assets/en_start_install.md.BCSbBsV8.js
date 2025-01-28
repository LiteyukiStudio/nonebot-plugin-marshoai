import{_ as e,c as d,ae as o,o as a}from"./chunks/framework.BzDBnRMZ.js";const u=JSON.parse('{"title":"","description":"","frontmatter":{},"headers":[],"relativePath":"en/start/install.md","filePath":"en/start/install.md","lastUpdated":1737975015000}'),s={name:"en/start/install.md"};function i(r,t,n,l,c,h){return a(),d("div",null,t[0]||(t[0]=[o(`<h2 id="💿-install" tabindex="-1">💿 Install <a class="header-anchor" href="#💿-install" aria-label="Permalink to &quot;💿 Install&quot;">​</a></h2><details open><summary>Install with nb-cli</summary><p>Open shell under the root directory of nonebot2, input the command below.</p><pre><code>nb plugin install nonebot-plugin-marshoai
</code></pre></details><details><summary>Install with pack manager</summary><p>Open shell under the plugin directory of nonebot2, input corresponding command according to your pack manager.</p><details><summary>pip</summary><pre><code>pip install nonebot-plugin-marshoai
</code></pre></details><details><summary>pdm</summary><pre><code>pdm add nonebot-plugin-marshoai
</code></pre></details><details><summary>poetry</summary><pre><code>poetry add nonebot-plugin-marshoai
</code></pre></details><details><summary>conda</summary><pre><code>conda install nonebot-plugin-marshoai
</code></pre></details><p>Open the <code>pyproject.toml</code> file under nonebot2&#39;s root directory, Add to<code>[tool.nonebot]</code>.</p><pre><code>plugins = [&quot;nonebot_plugin_marshoai&quot;]
</code></pre></details><h2 id="🤖-get-token-github-models" tabindex="-1">🤖 Get token(GitHub Models) <a class="header-anchor" href="#🤖-get-token-github-models" aria-label="Permalink to &quot;🤖 Get token(GitHub Models)&quot;">​</a></h2><ul><li>Create new <a href="https://github.com/settings/tokens/new" target="_blank" rel="noreferrer">personal access token</a>，<strong>Don&#39;t need any permissions</strong>.</li><li>Copy the new token, add to the <code>.env</code> file&#39;s <code>marshoai_token</code> option.</li></ul><div class="warning custom-block"><p class="custom-block-title">WARNING</p><p>GitHub Models API comes with significant limitations and is therefore not recommended for use. For better alternatives, it&#39;s suggested to adjust the configuration <code>MARSHOAI_AZURE_ENDPOINT</code> to use other service providers&#39; models instead.</p></div><h2 id="🎉-usage" tabindex="-1">🎉 Usage <a class="header-anchor" href="#🎉-usage" aria-label="Permalink to &quot;🎉 Usage&quot;">​</a></h2><p>End <code>marsho</code> in order to get direction for use(If you configured the custom command, please use the configured one).</p><h4 id="👉-double-click-avatar" tabindex="-1">👉 Double click avatar <a class="header-anchor" href="#👉-double-click-avatar" aria-label="Permalink to &quot;👉 Double click avatar&quot;">​</a></h4><p>When nonebot linked to OneBot v11 adapter, can recieve double click and response to it. More detail in the <code>MARSHOAI_POKE_SUFFIX</code> option.</p><h2 id="🛠️-marshotools-deprecated" tabindex="-1">🛠️ <s>MarshoTools</s> (Deprecated) <a class="header-anchor" href="#🛠️-marshotools-deprecated" aria-label="Permalink to &quot;🛠️ ~~MarshoTools~~ (Deprecated)&quot;">​</a></h2><p>MarshoTools is a feature added in <code>v0.5.0</code>, support loading external function library to provide Function Call for Marsho.</p><h2 id="🧩-marsho-plugin" tabindex="-1">🧩 Marsho Plugin <a class="header-anchor" href="#🧩-marsho-plugin" aria-label="Permalink to &quot;🧩 Marsho Plugin&quot;">​</a></h2><p>Marsho Plugin is a feature added in <code>v1.0.0</code>, replacing the old MarshoTools feature. <a href="https://marsho.liteyuki.icu/dev/extension" target="_blank" rel="noreferrer">Documentation</a></p><h2 id="👍-praise-list" tabindex="-1">👍 Praise list <a class="header-anchor" href="#👍-praise-list" aria-label="Permalink to &quot;👍 Praise list&quot;">​</a></h2><p>Praise list stored in the <code>praises.json</code> in plugin directory（This directory will putput to log when Bot start), it&#39;ll automatically generate when option is <code>true</code>, include character name and advantage two basic data.</p><p>The character stored in it would be “know” and “like” by Marsho.</p><p>It&#39;s structure is similar to:</p><div class="language-json vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">json</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">{</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">  &quot;like&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: [</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    {</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">      &quot;name&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;Asankilp&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">,</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">      &quot;advantages&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;赋予了Marsho猫娘人格，使用vim与vscode为Marsho写了许多代码，使Marsho更加可爱&quot;</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    },</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    {</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">      &quot;name&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;神羽(snowykami)&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">,</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-dark:#79B8FF;">      &quot;advantages&quot;</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">: </span><span style="--shiki-light:#032F62;--shiki-dark:#9ECBFF;">&quot;人脉很广，经常找小伙伴们开银趴，很会写后端代码&quot;</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">    },</span></span>
<span class="line"><span style="--shiki-light:#B31D28;--shiki-light-font-style:italic;--shiki-dark:#FDAEB7;--shiki-dark-font-style:italic;">    ...</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">  ]</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">}</span></span></code></pre></div><h2 id="⚙️-configurable-options" tabindex="-1">⚙️ Configurable options <a class="header-anchor" href="#⚙️-configurable-options" aria-label="Permalink to &quot;⚙️ Configurable options&quot;">​</a></h2><p>Add options in the <code>.env</code> file from the diagram below in nonebot2 project.</p><h4 id="plugin-behaviour" tabindex="-1">plugin behaviour <a class="header-anchor" href="#plugin-behaviour" aria-label="Permalink to &quot;plugin behaviour&quot;">​</a></h4><table tabindex="0"><thead><tr><th>Option</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>MARSHOAI_USE_YAML_CONFIG</td><td><code>bool</code></td><td><code>false</code></td><td>Use YAML config format</td></tr><tr><td>MARSHOAI_DEVMODE</td><td><code>bool</code></td><td><code>true</code></td><td>Turn on Development Mode or not</td></tr></tbody></table><h4 id="marsho-usage" tabindex="-1">Marsho usage <a class="header-anchor" href="#marsho-usage" aria-label="Permalink to &quot;Marsho usage&quot;">​</a></h4><table tabindex="0"><thead><tr><th>Option</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>MARSHOAI_DEFAULT_NAME</td><td><code>str</code></td><td><code>marsho</code></td><td>Command to call Marsho</td></tr><tr><td>MARSHOAI_ALIASES</td><td><code>set[str]</code></td><td><code>list[&quot;小棉&quot;]</code></td><td>Other name(Alias) to call Marsho</td></tr><tr><td>MARSHOAI_AT</td><td><code>bool</code></td><td><code>false</code></td><td>Call by @ or not</td></tr><tr><td>MARSHOAI_MAIN_COLOUR</td><td><code>str</code></td><td><code>FFAAAA</code></td><td>Theme color, used by some tools and features</td></tr></tbody></table><h4 id="ai-call" tabindex="-1">AI call <a class="header-anchor" href="#ai-call" aria-label="Permalink to &quot;AI call&quot;">​</a></h4><table tabindex="0"><thead><tr><th>Option</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>MARSHOAI_TOKEN</td><td><code>str</code></td><td></td><td>The token needed to call AI API</td></tr><tr><td>MARSHOAI_DEFAULT_MODEL</td><td><code>str</code></td><td><code>gpt-4o-mini</code></td><td>The default model of Marsho</td></tr><tr><td>MARSHOAI_PROMPT</td><td><code>str</code></td><td>Catgirl Marsho&#39;s character prompt</td><td>Marsho&#39;s basic system prompt <strong>※Some models(o1 and so on) don&#39;t support it</strong></td></tr><tr><td>MARSHOAI_ADDITIONAL_PROMPT</td><td><code>str</code></td><td></td><td>Marsho&#39;s external system prompt</td></tr><tr><td>MARSHOAI_ENFORCE_NICKNAME</td><td><code>bool</code></td><td><code>true</code></td><td>Enforce user to set nickname or not</td></tr><tr><td>MARSHOAI_POKE_SUFFIX</td><td><code>str</code></td><td><code>揉了揉你的猫耳</code></td><td>When double click Marsho who connected to OneBot adapter, the chat content. When it&#39;s empty string, double click function is off. Such as, the default content is <code>*[昵称]揉了揉你的猫耳。</code></td></tr><tr><td>MARSHOAI_AZURE_ENDPOINT</td><td><code>str</code></td><td><code>https://models.inference.ai.azure.com</code></td><td>OpenAI standard API</td></tr><tr><td>MARSHOAI_TEMPERATURE</td><td><code>float</code></td><td><code>null</code></td><td>temperature parameter</td></tr><tr><td>MARSHOAI_TOP_P</td><td><code>float</code></td><td><code>null</code></td><td>Nucleus Sampling parameter</td></tr><tr><td>MARSHOAI_MAX_TOKENS</td><td><code>int</code></td><td><code>null</code></td><td>Max token number</td></tr><tr><td>MARSHOAI_ADDITIONAL_IMAGE_MODELS</td><td><code>list</code></td><td><code>[]</code></td><td>External image-support model list, such as <code>hunyuan-vision</code></td></tr><tr><td>MARSHOAI_NICKNAME_LIMIT</td><td><code>int</code></td><td><code>16</code></td><td>Limit for nickname length</td></tr><tr><td>MARSHOAI_TIMEOUT</td><td><code>float</code></td><td><code>50</code></td><td>AI request timeout (seconds)</td></tr></tbody></table><h4 id="feature-switches" tabindex="-1">Feature Switches <a class="header-anchor" href="#feature-switches" aria-label="Permalink to &quot;Feature Switches&quot;">​</a></h4><table tabindex="0"><thead><tr><th>Option</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td>MARSHOAI_ENABLE_SUPPORT_IMAGE_TIP</td><td><code>bool</code></td><td><code>true</code></td><td>When on, if user send request with photo and model don&#39;t support that, remind the user</td></tr><tr><td>MARSHOAI_ENABLE_NICKNAME_TIP</td><td><code>bool</code></td><td><code>true</code></td><td>When on, if user haven&#39;t set username, remind user to set</td></tr><tr><td>MARSHOAI_ENABLE_PRAISES</td><td><code>bool</code></td><td><code>true</code></td><td>Turn on Praise list or not</td></tr><tr><td>MARSHOAI_ENABLE_TIME_PROMPT</td><td><code>bool</code></td><td><code>true</code></td><td>Turn on real-time date and time (accurate to seconds) and lunar date system prompt</td></tr><tr><td>MARSHOAI_ENABLE_TOOLS</td><td><code>bool</code></td><td><code>false</code></td><td>Turn on Marsho Tools or not</td></tr><tr><td>MARSHOAI_ENABLE_PLUGINS</td><td><code>bool</code></td><td><code>true</code></td><td>Turn on Marsho Plugins or not</td></tr><tr><td>MARSHOAI_PLUGIN_DIRS</td><td><code>list[str]</code></td><td><code>[]</code></td><td>List of plugins directory</td></tr><tr><td>MARSHOAI_LOAD_BUILTIN_TOOLS</td><td><code>bool</code></td><td><code>true</code></td><td>Loading the built-in toolkit or not</td></tr><tr><td>MARSHOAI_TOOLSET_DIR</td><td><code>list</code></td><td><code>[]</code></td><td>List of external toolset directory</td></tr><tr><td>MARSHOAI_DISABLED_TOOLKITS</td><td><code>list</code></td><td><code>[]</code></td><td>List of disabled toolkits&#39; name</td></tr><tr><td>MARSHOAI_ENABLE_RICHTEXT_PARSE</td><td><code>bool</code></td><td><code>true</code></td><td>Turn on auto parse rich text feature(including image, LaTeX equation)</td></tr><tr><td>MARSHOAI_SINGLE_LATEX_PARSE</td><td><code>bool</code></td><td><code>false</code></td><td>Render single-line equation or not</td></tr><tr><td>MARSHOAI_FIX_TOOLCALLS</td><td><code>bool</code></td><td><code>true</code></td><td>Fix tool calls or not</td></tr><tr><td>MARSHOAI_SEND_THINKING</td><td><code>bool</code></td><td><code>true</code></td><td>Send thinking chain or not</td></tr></tbody></table>`,29)]))}const m=e(s,[["render",i]]);export{u as __pageData,m as default};