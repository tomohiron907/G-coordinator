# AGENTS.md (g-coordinator 専用)

## Goal
このリポジトリにおけるエージェントの目的:
- **gcoordinator** を用いて **決定的に再現可能な G-code** を生成する。
- 生成物は `artifacts/` に保存し、設定・経路・変換処理を**スクリプト化**して小さな差分でPR可能にする。

## References
- API要約: `agents/gcoordinator_apiguide.md`（存在する場合は最優先で参照）
- 主対象モジュール: `gcoordinator.path_generator`, `gcoordinator.path_transformer`, `gcoordinator.infill_generator`, `gcoordinator.settings`
- 注意: `infill_generator` は計算コスト/出力サイズが大。必要時のみ使用。

## Setup (Arch Linux, Python venv)
注意: Python3.11のみのサポートの模様   
(すでに環境が存在すればそれを用いること)   

```sh
# Python 仮想環境
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

# 依存関係（本リポジトリの requirements.txt がある前提）
pip install -r requirements.txt

# Lint/Format/Test（要求される場合）
pip install ruff black pytest
```

> 本リポジトリがライブラリを内包している場合は `pip install -e .` を使用。外部パッケージとして利用する場合は、プロジェクトの指定手順に従う。

## Conventions
- **入出力を決定的に**するため、乱数・時刻依存を廃止。座標列は NumPy 配列、角度はラジアン。
- G-code の開始/終了/温度などの**プリンタ依存設定**は `user/configs/printer/*.json` に分離（例: `nozzle_diameter`, `layer_height`, `retraction` 等）。
- **大きな G-code**（>10MB）は Git LFS を使用するか、`user/artifacts/` にのみ出力しリポジトリに含めない。

## Paths of Interest

- `user/scripts/` : 経路生成・変換・出力のエントリスクリプト群（CLI想定）
- `user/configs/` : プリンタ設定JSON、材料別プロファイル
- `user/presets/` : パターン/ジオメトリのパラメータセット（例: 円周, 格子, 渦）
- `user/artifacts/` : 生成物（G-code, プレビュー画像, メタ情報）

## How to Work
1. **設定の読み込み**: `gcoordinator.settings.load_settings()` で `user/configs/printer/*.json` を読み込む。
2. **経路の生成**: `gcoordinator.path_generator.Path` / `PathList` を用いて座標列を作成（NumPy）。
3. **幾何変換**: `gcoordinator.path_transformer.Transform.move/rotate_xy/stretch/offset` を必要最小限で適用。
4. **充填（必要時のみ）**: `infill_generator` を使う場合は処理時間に注意。
5. **エクスポート**: G-code 生成ユーティリティ or GUI 経由のエクスポートを呼び出し、`user/artifacts/` に保存。
6. **検証**: 生成された G-code のメタ情報（総移動距離・レイヤ数など）を出力して記録。

## Do / Don't
- **DO**: すべての処理をスクリプト化し、同一入力から同一 G-code が得られることを担保。
- **DO**: 変換チェーン（Transform）のパラメータを `user/presets/` に保存し差分管理。
- **DON'T**: 物理プリンタへ直接送信/実行しない（オフラインでの G-code 生成・検証のみに限定）。
- **DON'T**: 巨大ファイルをリポジトリへ直コミットしない。

## Commands (標準化コマンド)
```zsh
# 1) 設定検証（JSONの妥当性チェックなど、用意があれば）
python -m scripts.validate_configs

# 2) パターン生成（例：円周）
python -m scripts.generate --preset presets/circle.yaml --printer configs/printer/sample.json --out artifacts/circle.gcode

# 3) 幾何変換（例：Zオフセット + 回転）
python -m scripts.transform --in artifacts/circle.gcode --z 0.2 --rotate-xy 1.57079632679 --out artifacts/circle_xform.gcode

# 4) 検証（レイヤ数や総移動距離の集計）
python -m scripts.inspect --in artifacts/circle_xform.gcode --meta artifacts/circle_xform.meta.json
```

> `user/scripts/*` はこのリポジトリに合わせて実装すること。最小限の CLI 引数（`--in/--out`, `--preset`, `--printer` 等）を統一。

## Verification (Done Criteria)
- `user/artifacts/*.gcode` が存在し、**再実行でバイナリ同一**（`sha256sum` が一致）
- 生成メタ情報（例：総移動距離、レイヤ数、最小/最大速度）が `*.meta.json` に保存される
- Lint/Format/Test がグリーン（設定がある場合）
```zsh
ruff check . && black --check . && pytest -q
```

## Safety Guardrails
- 外部ネットワークや実機制御は禁止。G-code は**ファイル出力のみ**。
- 入力ファイル/設定は **read-only** 扱い。破壊的操作（`rm -rf` 等）を行わない。
- `infill_generator` 使用時は**実行時間・ファイルサイズ**の増大に注意（必要時のみ）。

## PR Rules
- 変更は小さく、`scripts/`, `configs/`, `presets/` のどこに影響したかを PR 説明に明記。
- 生成物は `artifacts/` に置き、必要があればキャプチャ（PNG）やメタ情報を添付。

## English Summary (for non-JP agents)
- Use Python venv; coordinates as NumPy arrays, angles in radians.
- Keep determinism: same inputs must produce identical G-code (check `sha256`).
- No physical printer access; file outputs only under `artifacts/`.
- Read `docs/gcoordinator_api_agent.md` first for module/API cheat sheet.
