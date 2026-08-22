# 日本シティービルダー - 技術仕様書

## 1. システムアーキテクチャ

### 推奨構成：Pygame + Python

```
┌─────────────────────────────────────────────┐
│         ゲームアプリケーション層               │
│  ┌─────────────────────────────────────┐   │
│  │  Main Loop / Game State Manager     │   │
│  └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│         ビジネスロジック層                   │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │ Simulation   │  │ Build System     │   │
│  │ Engine       │  │ (Config-driven)  │   │
│  └──────────────┘  └──────────────────┘   │
├─────────────────────────────────────────────┤
│         データ層                            │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │ Map/Tile     │  │ Game State       │   │
│  │ Manager      │  │ (Serializable)   │   │
│  └──────────────┘  └──────────────────┘   │
├─────────────────────────────────────────────┤
│         レンダリング層                      │
│  ┌──────────────────────────────────────┐  │
│  │ Pygame Renderer                      │  │
│  └──────────────────────────────────────┘  │
└──���──────────────────────────────────────────┘
```

---

## 2. ディレクトリ構造

```
japan-city-builder/
│
├── src/
│   ├── main.py                    # エントリーポイント
│   │
│   ├── game/
│   │   ├── __init__.py
│   │   ├── game.py                # メインゲームループ
│   │   └── game_state.py          # ゲーム状態管理
│   │
│   ├── map/
│   │   ├── __init__.py
│   │   ├── tile.py                # タイルクラス
│   │   ├── map_manager.py         # マップ管理
│   │   └── tilemap.py             # タイルマップ全体
│   │
│   ├── buildings/
│   │   ├── __init__.py
│   │   ├── building.py            # 建物基底クラス
│   │   ├── building_registry.py   # 建物カタログ
│   │   ├── types/
│   │   │   ├── residence.py       # 住宅
│   │   │   ├── commercial.py      # 商業施設
│   │   │   ├── industrial.py      # 工業施設
│   │   │   └── infrastructure.py  # インフラ
│   │   └── manager.py             # 建物管理
│   │
│   ├── economy/
│   │   ├── __init__.py
│   │   ├── budget.py              # 予算・資金管理
│   │   ├── taxation.py            # 税制システム
│   │   └── market.py              # 経済シミュレーション
│   │
│   ├── population/
│   │   ├── __init__.py
│   │   ├── citizen.py             # 市民クラス
│   │   ├── population.py          # 人口管理
│   │   └── employment.py          # 雇用システム
│   │
│   ├── transport/
│   │   ├── __init__.py
│   │   ├── network.py             # 交通ネットワーク
│   │   ├── route.py               # ルート管理
│   │   └── traffic.py             # 交通流シミュレーション
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── screen.py              # 画面管理
│   │   ├── hud.py                 # HUD表示
│   │   ├── menu/
│   │   │   ├── main_menu.py
│   │   │   └── settings_menu.py
│   │   ├── panels/
│   │   │   ├── build_panel.py     # 建築パネル
│   │   │   ├── stats_panel.py     # 統計パネル
│   │   │   └── info_panel.py      # 情報パネル
│   │   └── widgets/
│   │       ├── button.py
│   │       ├── slider.py
│   │       └── graph.py
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── event_manager.py       # イベント管理
│   │   ├── event_types.py         # イベント種別定義
│   │   └── event_effects.py       # イベント効果
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py              # 設定管理
│   │   ├── constants.py           # 定数定義
│   │   ├── logger.py              # ログ出力
│   │   └── math_utils.py          # 数学ユーティリティ
│   │
│   └── save/
│       ├── __init__.py
│       ├── save_manager.py        # セーブ・ロード
│       └── serializer.py          # オブジェクトシリアライズ
│
├── assets/
│   ├── images/
│   │   ├── tiles/                 # タイル画像
│   │   ├── buildings/             # 建物画像
│   │   ├── ui/                    # UI画像
│   │   └── icons/                 # アイコン
│   │
│   ├── sounds/
│   │   ├── bgm/                   # BGM
│   │   └── sfx/                   # 効果音
│   │
│   ├── data/
│   │   ├── buildings.yaml         # 建物定義
│   │   ├── items.yaml             # アイテム定義
│   │   └── map_data/              # マップデータ
│   │       ├── japan_map.json
│   │       └── region_data.json
│   │
│   └── fonts/                     # フォント
│       ├── regular.ttf
│       └── bold.ttf
│
├── tests/
│   ├── test_map.py
│   ├── test_buildings.py
│   ├── test_economy.py
│   ├── test_population.py
│   └── test_transport.py
│
├── docs/
│   ├── GAME_DESIGN_DOCUMENT.md    # ゲームデザイン
│   ├── TECHNICAL_SPECIFICATION.md # 技術仕様（このファイル）
│   ├── API.md                     # API仕様
│   └── DEVELOPMENT.md             # 開発ガイド
│
├── .gitignore
├── requirements.txt               # Python依存関係
├── README.md                      # プロジェクト概要
├── setup.py                       # セットアップスクリプト
└── run.py                         # ゲーム起動スクリプト
```

---

## 3. コア クラス設計

### 3.1 Tile（タイル）

```python
class Tile:
    """マップの基本単位"""
    
    TERRAIN_TYPES = {
        'grass': 0,
        'mountain': 1,
        'water': 2,
        'coast': 3,
        'urban': 4
    }
    
    def __init__(self, x: int, y: int, terrain_type: str):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.building: Optional[Building] = None
        self.development_level = 0  # 0-3
        self.population = 0
        self.happiness = 100
        self.pollution = 0
```

### 3.2 Building（建物）

```python
class Building:
    """建物の基底クラス"""
    
    def __init__(self, x: int, y: int, building_id: str):
        self.x = x
        self.y = y
        self.building_id = building_id  # 'residential_1', 'station', etc.
        self.construction_time = 0
        self.maintenance_cost = 0
        self.population_capacity = 0
        self.employment_provided = 0
        self.revenue = 0
        self.is_operational = False
    
    def tick(self, game_state):
        """毎ターンの更新"""
        pass
    
    def get_info(self) -> dict:
        """建物情報を取得"""
        pass
```

### 3.3 GameState（ゲーム状態）

```python
class GameState:
    """ゲーム全体の状態管理"""
    
    def __init__(self):
        self.current_year = 2024
        self.current_month = 1
        self.current_day = 1
        
        # ゲームデータ
        self.tilemap: Tilemap = None
        self.buildings: BuildingManager = None
        self.population: PopulationManager = None
        self.economy: EconomyManager = None
        self.transport: TransportManager = None
        
        # ゲーム統計
        self.total_population = 0
        self.total_budget = 10000  # 初期予算
        self.current_balance = 10000
        
        self.is_paused = False
        self.game_speed = 1  # 1x, 2x, 4x
    
    def tick(self):
        """ゲーム内時間を進める"""
        # 各システムの更新
        self.population.update()
        self.economy.update()
        self.transport.update()
        self.buildings.update()
        
        # 時間進行
        self.current_day += 1
        if self.current_day > 30:
            self.current_day = 1
            self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
```

### 3.4 SimulationEngine（シミュレーション）

```python
class SimulationEngine:
    """経済・人口シミュレーション"""
    
    def simulate_month(self, game_state: GameState):
        """1ヶ月分のシミュレーション実行"""
        # 1. 人口流入・流出
        self._update_population(game_state)
        
        # 2. 雇用マッチング
        self._match_employment(game_state)
        
        # 3. 収支計算
        self._calculate_finances(game_state)
        
        # 4. 満足度計算
        self._calculate_happiness(game_state)
        
        # 5. イベント判定
        self._check_events(game_state)
    
    def _update_population(self, game_state: GameState):
        """人口動態シミュレーション"""
        pass
    
    def _calculate_finances(self, game_state: GameState):
        """収支計算"""
        pass
```

---

## 4. データフォーマット

### 4.1 建物定義 (assets/data/buildings.yaml)

```yaml
residential_1:
  name: "小住宅"
  category: "residential"
  size: [2, 2]
  build_cost: 500
  maintenance_cost: 10
  population_capacity: 50
  happiness_modifier: 1.0
  construction_time: 10  # ゲーム内日数
  sprite: "buildings/residential_1.png"

commercial_1:
  name: "商店街"
  category: "commercial"
  size: [3, 2]
  build_cost: 1500
  maintenance_cost: 30
  employment_provided: 20
  revenue: 100  # 月額
  construction_time: 15
  sprite: "buildings/commercial_1.png"

station:
  name: "駅"
  category: "infrastructure"
  size: [2, 3]
  build_cost: 5000
  maintenance_cost: 50
  employment_provided: 30
  construction_time: 20
  network_type: "rail"  # 交通ネットワーク接続
  sprite: "buildings/station.png"
```

### 4.2 セーブファイル形式 (JSON)

```json
{
  "version": "0.1.0",
  "game_state": {
    "current_year": 2025,
    "current_month": 3,
    "current_day": 15,
    "total_budget": 50000,
    "current_balance": 35000,
    "total_population": 100000
  },
  "map_data": {
    "width": 100,
    "height": 100,
    "tiles": [
      {
        "x": 0,
        "y": 0,
        "terrain": "grass",
        "building_id": null,
        "population": 0
      }
    ]
  },
  "buildings": [
    {
      "id": "station_001",
      "building_id": "station",
      "x": 10,
      "y": 10,
      "is_operational": true
    }
  ]
}
```

---

## 5. ゲームループ

```
┌─────────────────────────────────────┐
│      Initialize Game                │
│   - Load Config                     │
│   - Create Game State               │
│   - Load Assets                     │
└──────────────┬──────────────────────┘
               │
         ┌─────▼─────┐
         │ Game Loop │
         └─────┬─────┘
               │
      ┌────────┴────────┐
      │                 │
  ┌───▼────┐        ┌──▼────┐
  │ Input  │        │ Tick   │
  │Handle  │        │(Update)│
  └────┬───┘        └──┬─────┘
       │               │
       ▼               ▼
  ┌──────────────────────────┐
  │   Game State Update      │
  │ - Simulation Step        │
  │ - Entity Updates         │
  │ - Event Processing       │
  └────┬─────────────────────┘
       │
  ┌────▼─────────────────────┐
  │      Render Phase        │
  │ - Draw Map               │
  │ - Draw Buildings         │
  │ - Draw UI                │
  │ - Swap Buffers           │
  └────┬─────────────────────┘
       │
   ┌───▼──┐
   │ Loop?│
   └───┬──┘
       │
    Yes├──┐
       │  │
       └──┘
       │
      No
       │
    ┌──▼──────────────┐
    │ Cleanup & Exit  │
    │ - Save State    │
    │ - Free Memory   │
    └─────────────────┘
```

---

## 6. 主要アルゴリズム

### 6.1 交通ネットワーク接続

```python
def find_connected_stations(self, start_station: Building) -> Set[Building]:
    """
    駅から接続可能な駅を全て探索（BFS）
    """
    visited = set()
    queue = [start_station]
    connected = set()
    
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        connected.add(current)
        
        # 隣接した駅を探索
        for neighbor in self.get_adjacent_stations(current):
            if neighbor not in visited and self.is_connected(current, neighbor):
                queue.append(neighbor)
    
    return connected
```

### 6.2 人口流入ロジック

```python
def calculate_population_flow(self, tile: Tile) -> int:
    """
    このタイルへの月間人口流入・流出を計算
    
    factors:
    - 失業率
    - 満足度
    - 周辺施設（学校・病院など）
    """
    base_flow = 10  # 基本流入
    
    # 雇用満足度
    unemployment = self.get_unemployment_rate()
    if unemployment > 0.5:
        base_flow *= 0.5  # 失業率高いと人口流出
    
    # 満足度
    happiness = tile.happiness / 100
    base_flow *= happiness
    
    # 周辺施設ボーナス
    nearby_schools = self.count_nearby_buildings(tile, 'school', radius=5)
    base_flow += nearby_schools * 2
    
    return int(base_flow)
```

### 6.3 収支計算

```python
def calculate_monthly_finances(self, game_state: GameState):
    """
    月間の収支を計算
    """
    income = 0
    expenses = 0
    
    # 収入：税金
    income += game_state.total_population * 0.5  # 市民税
    
    # 収入：企業利益
    for building in game_state.buildings.get_all():
        if building.revenue > 0:
            income += building.revenue
    
    # 支出：維持費
    for building in game_state.buildings.get_all():
        expenses += building.maintenance_cost
    
    # 支出：公共サービス
    expenses += game_state.total_population * 0.1
    
    # 支出：災害復旧（イベント発生時）
    if game_state.has_active_disaster:
        expenses += game_state.disaster_cost
    
    net = income - expenses
    game_state.current_balance += net
```

---

## 7. 性能最適化

### 7.1 レンダリング最適化
- **ビューポートカリング**: 画面外のタイル・建物は描画しない
- **タイルキャッシング**: 頻繁に更新されないタイルは事前レンダリング
- **レイヤー分離**: 背景・オブジェクト・UIを別レイヤーで管理

### 7.2 シミュレーション最適化
- **セクター分割**: マップを複数セクターに分割
- **遅延計算**: 必要な時だけ計算（Lazy Evaluation）
- **イベント駆動**: ポーリングではなくイベント駆動で処理

---

## 8. 依存ライブラリ

```
pygame>=2.1.0          # ゲームエンジン
pyyaml>=6.0            # YAML設定ファイル
numpy>=1.20.0          # 数値計算
pillow>=9.0.0          # 画像処理
pytest>=7.0.0          # テストフレームワーク
```

---

## 9. 開発フロー

### ブランチ戦略
```
main (リリース版)
 └─ develop (開発版)
     ├─ feature/map-system
     ├─ feature/building-system
     └─ feature/economy-system
```

### コミット規則
```
feat: 新機能
fix: バグ修正
refactor: リファクタリング
docs: ドキュメント
test: テスト追加
```

---

## 10. テスト戦略

### ユニットテスト
- 各クラスの個別テスト
- モックを使用した依存関係の分離

### 統合テスト
- システム全体の動作確認
- シミュレーション結果の妥当性検証

### 性能テスト
- FPS測定
- メモリ使用量測定
- 大規模マップでのパフォーマンス

---

このドキュメントは開発の進行に応じて更新されます。
