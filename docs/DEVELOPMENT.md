# Japan City Builder - 開発ガイド

## 環境構築

### 前提条件
- Python 3.8 以上
- Git
- pip（Pythonパッケージマネ���ジャー）

### セットアップ手順

#### 1. リポジトリのクローン
```bash
git clone https://github.com/masatori/japan-city-builder.git
cd japan-city-builder
```

#### 2. 仮想環境の作成（推奨）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. 依存ライブラリのインストール
```bash
pip install -r requirements.txt
```

#### 4. ゲームの起動テスト
```bash
python src/main.py
```

---

## プロジェクト構造

```
japan-city-builder/
├── src/              # ソースコード
├── assets/           # 画像・音声・データ
├── tests/            # テストコード
├── docs/             # ドキュメント
├── requirements.txt  # Python依存関係
├── setup.py          # セットアップスクリプト
└── README.md         # プロジェクト概要
```

---

## 開発ワークフロー

### ブランチ戦略（Git Flow）

```
main（本番リリース）
  ↓
release/v0.1.0
  ↓
develop（開発版）
  ├─ feature/map-system
  ├─ feature/building-system
  ├─ feature/economy-system
  └─ bugfix/ui-issues
```

### 開発手順

#### 1. 新機能の開発

```bash
# developブランチから新しい機能ブランチを作成
git checkout develop
git pull origin develop
git checkout -b feature/my-feature-name

# 実装・テスト
# ...

# コミット
git add .
git commit -m "feat: 新機能の説明"

# プッシュ
git push origin feature/my-feature-name

# Pull Requestを作成
```

#### 2. バグ修正

```bash
git checkout develop
git checkout -b bugfix/bug-name
# バグ修正
git commit -m "fix: バグ修正の説明"
git push origin bugfix/bug-name
```

#### 3. Pull Requestのレビュー

- 最低1人のレビューが必要
- テストがすべてパスしていることを確認
- コード品質チェック（linting）を確認

---

## コード規約

### Python スタイルガイド

PEP 8に準拠してください。

```bash
# 自動フォーマット（Black）
black src/

# Linting（flake8）
flake8 src/

# 型チェック（mypy）
mypy src/

# Import並序（isort）
isort src/
```

### ネーミング規約

```python
# クラス名：PascalCase
class GameState:
    pass

# 関数・メソッド名：snake_case
def calculate_population():
    pass

# 定数：UPPER_SNAKE_CASE
INITIAL_BUDGET = 10000

# プライベート属性：_で始める
self._private_attribute = None
```

### ドキュメンテーション

```python
def calculate_happiness(population: int, unemployment_rate: float) -> float:
    """
    市民の幸福度を計算する
    
    Args:
        population: 人口
        unemployment_rate: 失業率（0.0-1.0）
    
    Returns:
        幸福度（0-100）
    
    Example:
        >>> happiness = calculate_happiness(10000, 0.05)
        >>> print(happiness)
        75.5
    """
    # 実装
    pass
```

---

## テスト

### テスト実行

```bash
# すべてのテストを実行
pytest

# カバレッジ付きで実行
pytest --cov=src

# 特定のテストファイルを実行
pytest tests/test_map.py

# 特定のテストを実行
pytest tests/test_map.py::test_tile_creation
```

### テストの書き方

```python
# tests/test_map.py
import pytest
from src.map.tile import Tile

class TestTile:
    def test_tile_creation(self):
        """タイルの生成テスト"""
        tile = Tile(0, 0, 'grass')
        assert tile.x == 0
        assert tile.y == 0
        assert tile.terrain_type == 'grass'
    
    def test_tile_building_assignment(self):
        """タイルへの建物配置テスト"""
        tile = Tile(0, 0, 'grass')
        # テスト実装
        pass
```

---

## ログ出力

```python
import logging

logger = logging.getLogger(__name__)

# ログレベル
logger.debug("デバッグ情報")
logger.info("情報")
logger.warning("警告")
logger.error("エラー")
logger.critical("致命的エラー")
```

---

## パフォーマンス最適化

### プロファイリング

```python
import cProfile
import pstats

cProfile.run('main_game_loop()', 'output.prof')
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative').print_stats(10)
```

### メモリプロファイリング

```bash
pip install memory-profiler
python -m memory_profiler main.py
```

---

## デバッグ

### 標準的なデバッグ方法

```python
# PDBを使用
import pdb; pdb.set_trace()

# VS Codeでのデバッグ
# .vscode/launch.jsonに設定を追加
```

### デバッグモード

```bash
# デバッグモードで起動
DEBUG=1 python src/main.py
```

---

## ドキュメント生成

```bash
# Sphinxドキュメント生成
cd docs
make html

# ブラウザで確認
open _build/html/index.html
```

---

## よくある問題

### Pygame インストールエラー

```bash
# 最新版をインストール
pip install --upgrade pygame

# キャッシュをクリア
pip cache purge
pip install pygame
```

### 仮想環境が反応しない

```bash
# 仮想環境を削除して再作成
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## リリース手順

### バージョン更新

1. `setup.py`でバージョンを更新
2. `CHANGELOG.md`に変更内容を記入
3. タグを作成してプッシュ

```bash
git tag v0.1.0
git push origin v0.1.0
```

### リリース作成

```bash
# GitHubのReleasesページから新しいリリースを作成
# タグv0.1.0を選択
# リリースノートを記入
```

---

## コントリビューション

このプロジェクトへの貢献を歓迎します！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成（`feature/AmazingFeature`）
3. 変更をコミット（`git commit -m 'Add some AmazingFeature'`）
4. ブランチをプッシュ（`git push origin feature/AmazingFeature`）
5. Pull Requestを作成

---

## ライセンス

MIT License - 詳細は[LICENSE](../LICENSE)を参照

---

## サポート

問題が発生した場合は、[Issues](https://github.com/masatori/japan-city-builder/issues)で報告してください。
