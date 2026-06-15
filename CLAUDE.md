# CLAUDE.md

このファイルは Claude Code がこのリポジトリで作業する際のガイダンスです。

## プロジェクト概要

`base` は node + python のベース開発環境です。新しい検証やツールづくりの出発点として使います。

## ランタイムとツール

- Node.js 22（`.nvmrc`）/ pnpm。Lint=eslint、Format=prettier、Test=`node --test`。
- Python 3.13（`.python-version`）/ uv。Lint+Format=ruff、Test=pytest。

## コマンド

```bash
pnpm install          # Node 依存（eslint / prettier）
uv sync               # Python 依存（ruff / pytest）+ .venv

pnpm lint             # eslint src tests
pnpm format           # prettier --write .
pnpm test             # node --test

uv run ruff check .   # Python lint
uv run ruff format .  # Python format
uv run pytest         # Python test
```

## 自動整形 hook

`.claude/settings.json` の PostToolUse hook（`.claude/hooks/format.sh`）が、編集/作成したファイルを言語に応じて自動整形します（`.py`→ruff、`.js/.ts/.json/.md` 等→prettier）。ツール未導入時は静かにスキップします。

## 作業上の約束

- 応答は日本語で行う。
- 一時的なファイル・実験コードは `workdir/` 配下に置く（gitignore 推奨）。
- コミット／push は実行前にユーザーへ確認する。コミットメッセージは Conventional Commits。
- 破壊的操作（削除・本番反映・課金API）は事前に内容を提示して承認を得る。
- MCP は使わない方針（必要になったら相談）。
