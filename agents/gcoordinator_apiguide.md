# gcoordinator API（エージェント向け要約）

対象バージョン: 0.0.12（Read the Docs 掲載時点）  
https://gcoordinator.readthedocs.io/en/latest/  
https://gcoordinator.readthedocs.io/en/latest/gcoordinator.html#  

## モジュール一覧
- `gcoordinator.infill_generator` — インフィル（充填）パス生成。現状は未最適化で重い。  
- `gcoordinator.path_generator` — 幾何パスのデータ構造と補助関数。  
- `gcoordinator.path_transformer` — パス平行移動・回転・オフセット・伸縮。  
- `gcoordinator.settings` — 既定設定の辞書取得／JSON読込。  
- `gcoordinator.gui_export` / `gcoordinator.gcode_generator` / `gcoordinator.plot_3d` — エクスポート・G-code 生成・可視化。

---

## 1) `gcoordinator.path_generator`

### `class Path(x, y, z, rot=None, tilt=None, **kwargs)`
**概要**: 3次元空間中の一本の押出経路。NumPy 配列で座標列を保持。

- **主要属性（抜粋）**  
  `x, y, z: numpy.ndarray`（各点の座標）  
  `rot, tilt: numpy.ndarray | None`（各点の姿勢 [rad]）  
  `kinematics: str`（`'Cartesian' | 'BedRotate' | 'BedTiltBC' | 'NozzleTilt'`）  
  造形条件: `nozzle_diameter, filament_diameter, layer_height, print_speed, travel_speed, fan_speed, nozzle_temperature, bed_temperature, retraction(諸元), z_hop(諸元), extrusion_multiplier` ほか。

- **メソッド**  
  `apply_default_settings()` — 既定設定を適用。戻り値: `None`。  
  `apply_optional_settings()` — 任意設定辞書を反映。戻り値: `None`。

**注意**: 角度はラジアン前提。`kwargs`で造形条件を一括注入可能。

---

### `class PathList(paths)`
**概要**: `Path` の集合。**Pathと同名の属性を持ち、一括で全要素に適用**される。

- **属性**: `paths: list[Path]`  
- **主要メソッド**  
  `__setattr__(name, value)` — 同名属性を全Pathへ一括適用（副作用のみ、戻り値なし）。  
  `sort_paths()` — 直前パスの終端との近接順に並べ替え。戻り値: `None`。

---

### `flatten_path_list(full_object: list[Path|PathList]) -> list[Path]`
**概要**: `Path`/`PathList` 混在リストを平坦化して `list[Path]` を返す。

- **引数**: `full_object` — `Path` と `PathList` の混在リスト  
- **戻り値**: `list[Path]`  
- **補足**: 計算前の標準化に使用。

---

## 2) `gcoordinator.path_transformer.Transform`

### `static move(arg, x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0) -> Path | PathList`
**概要**: `Path` または `PathList` を並進・回転（ラジアン）で一括変換。**入力型を保持して返す**。

- **引数**:  
  `arg: Path | PathList`  
  並進: `x, y, z: float`  
  回転: `roll, pitch, yaw: float`（XYZ軸）  
- **戻り値**: 変換後 `Path` または `PathList`  

### `static move_path(path, x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0) -> Path`  
個別の `Path` 版。

### `static move_pathlist(pathlist, x=0, y=0, z=0, roll=0, pitch=0, yaw=0) -> PathList`  
`PathList` 全体を変換し新しい `PathList` を返す。

### `static offset(path, offset_distance) -> Path`  
各頂点の法線方向に `offset_distance` だけオフセット。

### `static rotate_xy(path, theta) -> Path`  
原点周りの2D回転（XY平面、ラジアン）。

### `static stretch(path, x_stretch_ratio, y_stretch_ratio, z_stretch_ratio) -> Path`  
各軸方向にスケーリング。

---

## 3) `gcoordinator.infill_generator`（計算コスト・出力サイズが大）
> 「最適化されていないので生成に時間がかかり、ファイルが大きい」と明記。

### `gyroid_infill(path, infill_distance=1, value=0) -> PathList`
**概要**: ジャイロイド充填パターン生成。  
- **引数**:  
  `path: Path | PathList`  
  `infill_distance: float`（面間隔）  
  `value: float`（式のオフセット項）  
- **戻り値**: `PathList`  
- **例外**: `TypeError`（不正型）

### `line_infill(path, infill_distance=1, angle=π/4) -> PathList`
**概要**: 直線充填。角度はラジアン（既定は `np.pi/4`）。  
- **引数**:  
  `path: Path | PathList`  
  `infill_distance: float`（線間隔、既定1）  
  `angle: float`（既定 `π/4`）  
- **戻り値**: `PathList`  
- **例外**: `TypeError`（不正型）

---

## 4) `gcoordinator.settings`

### `get_default_settings(settings) -> dict`
**概要**: 3Dプリンタの既定値を辞書で返す。主なキー:  
`nozzle_diameter, layer_height, filament_diameter, print_speed, travel_speed, x_origin, y_origin, fan_speed, nozzle_temperature, bed_temperature, retraction, retraction_distance, unretraction_distance, z_hop, z_hop_distance, extrusion_multiplier`。

### `load_settings(config_path: str) -> None`
**概要**: JSON設定ファイルの読み込み。無効JSONは `json.JSONDecodeError`。

---

## 5) `gcoordinator.gui_export` / `gcoordinator.gcode_generator` / `gcoordinator.plot_3d`
`gui_export` はGUI側エクスポート連携、`gcode_generator` はG-code生成、`plot_3d` は可視化用途のモジュール。

---

## 最小使用例（控えめ）
> 目的: 円周パス1本を作成し、Zだけ持ち上げてから処理系に渡す下ごしらえ

```python
import numpy as np
import gcoordinator as gc

arg = np.linspace(0, 2*np.pi, 100)
p = gc.Path(10*np.cos(arg), 10*np.sin(arg), np.zeros_like(arg))
p.apply_default_settings()   # 造形条件の下地を適用
p2 = gc.Transform.move(p, z=0.2)  # 0.2 mm 持ち上げ
# 以降、infill_generatorやエクスポート側へ
```

---

## エージェント実装の指針（要点）
- **型前提**: すべての座標・姿勢は `numpy.ndarray`、角度はラジアン。`PathList` は属性一括適用が前提。  
- **前処理**: 混在コンテナは `flatten_path_list()` で正規化。  
- **計算コスト**: `infill_generator` は重い。サイズ・時間制約があるパイプラインでは回避または別アルゴリズムへ。  
- **エラーハンドリング**: 代表例は `TypeError`（インフィル関数の引数型）と `json.JSONDecodeError`（設定読込）。