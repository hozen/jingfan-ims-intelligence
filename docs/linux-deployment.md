# Water Clay ICP Linux 部署手册

这是一个静态、只读的客户情报服务。页面由仓库中的 enriched 快照生成，不依赖 ChatGPT 登录，也不依赖 GitHub Pages。

## 推荐部署：Docker Compose

Linux 服务器需要 Git、Docker Engine 和 Docker Compose v2。默认仅监听服务器本机的 `127.0.0.1:8080`，避免客户情报直接暴露到公网。

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL> ims-gtm
cd ims-gtm
sh deploy/linux/install.sh
curl -fsS http://127.0.0.1:8080/healthz
```

浏览器可通过 SSH 隧道访问：

```bash
ssh -L 8080:127.0.0.1:8080 user@your-server
```

然后打开 `http://127.0.0.1:8080`。

若明确需要局域网直接访问，可在启动前设置监听地址：

```bash
WATER_CLAY_BIND=0.0.0.0 docker compose -f deploy/linux/docker-compose.yml up -d --build
```

这时应同时配置防火墙白名单，或在前置 Nginx/Caddy 上启用 HTTPS 与身份认证。页面包含真实客户情报，不建议匿名公网开放。

## 更新

```bash
cd ims-gtm
sh deploy/linux/update.sh
```

更新脚本会执行 fast-forward-only 的 `git pull`，重新生成页面并重建容器。若服务器没有 Python 3，则沿用仓库内已经生成的静态快照。

## 常用运维命令

```bash
docker compose -f deploy/linux/docker-compose.yml ps
docker compose -f deploy/linux/docker-compose.yml logs --tail=100 water-clay
docker compose -f deploy/linux/docker-compose.yml restart water-clay
docker compose -f deploy/linux/docker-compose.yml down
```

健康检查地址为 `http://127.0.0.1:8080/healthz`，正常响应为 `ok`。

## 不使用 Docker 的临时运行方式

```bash
python3 scripts/build_icp_poc.py
python3 -m http.server 8080 --bind 127.0.0.1 --directory customer/water-clay-poc
```

此方式适合验收，不建议作为长期生产服务。长期部署请使用 Docker Compose，或让服务器管理员把相同目录接入现有反向代理。

## 数据刷新逻辑

生成器读取：

- `intelligence/industrial/enriched/indctx_latest.json`
- `intelligence/municipal/enriched/ctx_latest.json`

运行 `python3 scripts/build_icp_poc.py` 后会更新：

- `customer/water-clay-poc/index.html`
- `customer/water-clay-poc/profiles.json`

当前 POC 只展示客户/项目情报和角色覆盖数量，不展示联系人手机号或邮箱。

