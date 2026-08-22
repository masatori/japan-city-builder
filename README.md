# 🏯 Japan City Builder

[![GitHub License](https://img.shields.io/github/license/masatori/japan-city-builder)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

日本を舞台にしたシティービルディング＆シミュレーションゲーム。駅や空港、ビル街などを建設し、日本の経済・交通を発展させるゲームです。

**Cities: Skylines** の日本版として、リアルな日本の地形と地名を使用しながら、シンプルながら奥深いシミュレーション体験を提供します。

![Build Status](https://img.shields.io/badge/status-development-yellow)
![Version](https://img.shields.io/badge/version-0.1.0-blue)

---

## 🎮 ゲームの特徴

- 🗺️ **日本全国のマップ** - リアルな地形と都市配置
- 🏢 **多様な建築物** - 駅、空港、オフィス、住宅、工業施設など
- 💰 **リアルな経済シミュレーション** - 税収、支出、失業率などの管理
- 👥 **人口・雇用システム** - 人口流動と就業機会の関連性
- 🚂 **交通ネットワーク** - 鉄道、バス、航空ネットワークの構築
- ⚡ **リアルタイムシミュレーション** - ゲーム内時間で経済が動く
- 🎯 **複数のゲームモード** - フリープレイ、シナリオ、チャレンジモード

---

## 📋 必要な環境

- **Python**: 3.8 以上
- **OS**: Windows / macOS / Linux
- **メモリ**: 4GB以上推奨
- **ディスク容量**: 500MB以上

---

## 🚀 クイックスタート

### 1. リポジトリをクローン

```bash
git clone https://github.com/masatori/japan-city-builder.git
cd japan-city-builder
```

### 2. 仮想環境を作成（推奨）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存ライブラリをインストール

```bash
pip install -r requirements.txt
```

### 4. ゲームを起動

```bash
python src/main.py
```

詳細は [開発ガイド](docs/DEVELOPMENT.md) を参照してください。

---

## 📚 ドキュメント

- 📖 [ゲームデザインドキュメント](docs/GAME_DESIGN_DOCUMENT.md) - ゲームの仕様・コンセプト
- 🔧 [技術仕様書](docs/TECHNICAL_SPECIFICATION.md) - アーキテクチャ・実装詳細
- 💻 [開発ガイド](docs/DEVELOPMENT.md) - セットアップ・開発フロー・ガイドライン

---

## 🎯 ゲームの目標

プレイヤーが市長として、以下の目標を達成することを目指します：

- ✅ 人口を増やし、繁栄した都市を構築する
- ✅ 交通ネットワークを整備し、効率的な移動を実現する
- ✅ 企業を誘致し、経済を成長させる
- ✅ 予算を管理し、赤字に陥らないようにする
- ✅ 市民の満足度を高く保つ

---

## 🎮 基本的なゲームプレイ

### ゲームループ

```
計画フェーズ
    ↓
インフラ・建物を配置
    ↓
シミュレーションフェーズ（時間経過）
    ↓
人口・経済シミュレーション実行
    ↓
結果確認・統計表示
    ↓
次のサイクルへ
```

### 主要なシステム

| システム | 説明 |
|---------|------|
| **マップ** | グリッドベースの日本全国マップ |
| **建物** | 駅・空港・オフィス・住宅など複数カテゴリ |
| **経済** | 税収・支出・失業率などの管理 |
| **人口** | 人口増減と満足度シミュレーション |
| **交通** | 鉄道・バス・航空ネットワーク |
| **イベント** | 災害・経済変動などのランダムイベント |

---

## 🏗️ プロジェクト構造

```
japan-city-builder/
├── src/                          # ソースコード
│   ├── main.py                   # エントリーポイント
│   ├── game/                     # ゲームコア
│   ├── map/                      # マップシステム
│   ├── buildings/                # 建物システム
│   ├── economy/                  # 経済システム
│   ├── population/               # 人口システム
│   ├── transport/                # 交通システム
│   ├── ui/                       # UI/画面
│   ├── events/                   # イベントシステム
│   ├── save/                     # セーブ・ロード
│   └── utils/                    # ユーティリティ
│
├── assets/                       # ゲームリソース
│   ├── images/                   # 画像
│   ├── sounds/                   # サウンド
│   ├── data/                     # データファイル
│   └── fonts/                    # フォント
│
├── tests/                        # テストコード
├── docs/                         # ドキュメント
├── config/                       # 設定ファイル
├── requirements.txt              # Python依存関係
├── setup.py                      # セットアップスクリプト
└── README.md                     # このファイル
```

---

## 🔧 開発

### 開発環境のセットアップ

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# コード品質チェックツール
pip install black flake8 mypy isort pylint pytest

# 自動フォーマット
black src/
isort src/

# Linting
flake8 src/
mypy src/

# テスト実行
pytest
```

### ブランチ戦略

`develop` ブランチから機能ブランチを切ります：

```bash
# 新機能開発の場合
git checkout develop
git checkout -b feature/my-feature-name

# バグ修正の場合
git checkout -b bugfix/bug-name
```

詳細は [開発ガイド](docs/DEVELOPMENT.md) を参照。

### テスト

```bash
# すべてのテストを実行
pytest

# カバレッジ付きで実行
pytest --cov=src

# 特定の��ストを実行
pytest tests/test_map.py
```

---

## 📈 開発ロードマップ

### Phase 1: 基礎システム構築 ✏️
- [ ] ゲームエンジン基盤
- [ ] マップシステム
- [ ] 基本建物配置
- [ ] 簡易シミュレーション

### Phase 2: 経済・交通システム 📋
- [ ] 人口・雇用システム
- [ ] 交通ネットワーク
- [ ] 経済循環
- [ ] イベントシステム

### Phase 3: UI/ポーランド 🎨
- [ ] 統計画面
- [ ] グラフィック改善
- [ ] サウンド実装
- [ ] チュートリアル

### Phase 4: テスト・リリース 🚀
- [ ] バグ修正
- [ ] ゲームバランス調整
- [ ] ドキュメント作成
- [ ] アルファ版リリース

---

## 🤝 コントリビューション

このプロジェクトへの貢献を歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチをプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Request を作成

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。
詳細は [LICENSE](LICENSE) ファイルを参照してください。

---

## 👤 作者

- **masatori** - [@masatori](https://github.com/masatori)

---

## 💬 フィードバック・サポート

問題を見つけたり、機能提案がある場合は、
[Issues](https://github.com/masatori/japan-city-builder/issues) で報告してください。

---

## 🎓 参考資料

### 類似ゲーム
- [Cities: Skylines](https://www.paradoxinteractive.com/games/cities-skylines/)
- [SimCity](https://www.ea.com/games/simcity)
- [A Short Hike](https://ashorthike.com/)

### 技術スタック
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Documentation](https://docs.python.org/3/)
- [Godot Engine](https://godotengine.org/)

---

## 🎉 謝辞

このプロジェクトを支援いただいたすべての方に感謝します。

**最終更新**: 2026年8月22日
**バージョン**: 0.1.0 (開発中)
