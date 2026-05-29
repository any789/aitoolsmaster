# ValueCell 安装成功！下一步配置

## ValueCell 已安装在 /Applications/ValueCell.app

**已经启动但Web界面（localhost:1420）连不上** — 需要配置 API Key

## 配置文件位置
~/.valuecell/.env

## 配置方式（任选一种）
### 方案A：用智谱API Key
智谱 key: `4cfe5ff4332445088a9ee3eaae84603a.fW1MDqTAsg74tdVi`

但ValueCell原生支持的是：OpenRouter / OpenAI / Google Gemini / SiliconFlow / Azure OpenAI / 阿里百炼

如果要用智谱，需要配置为 OpenAI-compatible:
```
OPENAI_COMPATIBLE_API_KEY=4cfe5ff4332445088a9ee3eaae84603a.fW1MDqTAsg74tdVi
OPENAI_COMPATIBLE_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 方案B：注册OpenRouter（推荐）
1. 打开 https://openrouter.ai/
2. 注册账号（可用Github/Gmail）
3. 免费额度，充几美金够用很久
4. 获取API Key，填到配置文件中

## 启动方式
重启ValueCell App即可。

## 访问地址
http://localhost:1420 (浏览器)
