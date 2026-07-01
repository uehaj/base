# base

Claude Code で使う node + python のベース開発環境（ローカル設定ファイル方式）。

## 前提ランタイム

- Node.js 22（`.nvmrc`）/ パッケージマネージャ: pnpm
- Python 3.13（`.python-version`）/ パッケージ・仮想環境: uv

## セットアップ

```bash
# Node 依存（eslint / prettier）
pnpm install

# Python 依存（ruff / pytest）と仮想環境
uv sync
```

## よく使うコマンド

| 目的   | Node          | Python                 |
| ------ | ------------- | ---------------------- |
| Lint   | `pnpm lint`   | `uv run ruff check .`  |
| Format | `pnpm format` | `uv run ruff format .` |
| Test   | `pnpm test`   | `uv run pytest`        |

## 構成

```
.
├── src/            # サンプル（hello.js / hello.py）
├── tests/          # テスト（hello.test.js / test_hello.py）
├── .claude/        # Claude Code 設定（権限許可リスト + 自動整形 hook）
├── package.json    # Node プロジェクト
├── pyproject.toml  # Python プロジェクト（uv 管理）
└── CLAUDE.md       # Claude Code 向けガイダンス
```

## デモページのデプロイ

`public/`（`particles.html` などの静的ページ）を配信します。

### GitHub Pages（自動）

`main` への push で `.github/workflows/pages.yml` が実行され、自動公開されます。
公開 URL: `https://uehaj.github.io/base/`

### Cloudflare Pages（ローカルから手動）

`wrangler` で `public/` をデプロイします。設定は `wrangler.toml`（プロジェクト名 `base-particle-demo` / 出力先 `public`）。

```bash
# 初回のみ: Cloudflare にログイン
npx --yes wrangler@latest login

# デプロイ
pnpm deploy:cf          # = npx wrangler pages deploy
```

初回デプロイ時にプロジェクトが未作成なら、対話プロンプトで作成できます。公開 URL は `https://base-particle-demo.pages.dev`（初回作成時に確定）。

## Claude Code 連携

- `.claude/settings.json` に node/python/git の安全なコマンド許可リストと、編集後にファイルを自動整形する PostToolUse hook（`.claude/hooks/format.sh`）を設定済み。
- 個人ローカルの上書きは `.claude/settings.local.json`（gitignore 済み）に置く。
