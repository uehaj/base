# CSV Chart Maker — Claude Managed Agent

CSV をアップロードすると、Claude が中身を見て適切なグラフを作り、PNG で返すエージェント。

## 構成

| ファイル                     | 役割                                                                 |
| ---------------------------- | -------------------------------------------------------------------- |
| `chart-agent.agent.yaml`     | エージェント定義（モデル・プロンプト・ツール）＝コントロールプレーン |
| `chart-env.environment.yaml` | サンドボックス環境定義＝コントロールプレーン                         |
| `run.py`                     | セッション駆動（アップロード→実行→ダウンロード）＝データプレーン     |

## 1. 一度だけ：エージェントと環境を作成（ID を保存）

`ant` CLI（推奨）で YAML から作成し、返ってきた ID を控える：

```sh
export ANTHROPIC_API_KEY=sk-ant-...

AGENT_ID=$(ant beta:agents create < chart-agent.agent.yaml --transform id -r)
ENV_ID=$(ant beta:environments create < chart-env.environment.yaml --transform id -r)

echo "AGENT_ID=$AGENT_ID"
echo "ENV_ID=$ENV_ID"
```

> SDK で作りたい場合（AWS など `ant` が使えない環境）は
> `client.beta.agents.create(...)` / `client.beta.environments.create(...)` を
> **一度だけ**呼んで ID を保存する（毎回作るのはアンチパターン）。

設定を変えたら（プロンプト調整など）`update` で新バージョンを作る：

```sh
ant beta:agents update --agent-id "$AGENT_ID" --version <N> < chart-agent.agent.yaml
```

## 2. 毎回：CSV を処理

```sh
export ANTHROPIC_API_KEY=sk-ant-...
export AGENT_ID=agent_...
export ENV_ID=env_...

pip install anthropic          # or: uv add anthropic
python run.py path/to/data.csv
```

生成されたグラフは `./outputs/` に保存される。

## 料金の目安

トークン（モデルレート）＋ セッション実行時間 $0.08/h（`running` の時間のみ）。
1分程度で終わる小さな CSV なら、1回あたり数円〜十数円程度。
