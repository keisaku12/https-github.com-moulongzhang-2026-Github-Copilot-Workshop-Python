# ポモドーロタイマー Web アプリケーション アーキテクチャ案

目的
------
- このドキュメントは、本プロジェクトで作成するポモドーロタイマー（Flask + HTML/CSS/JS）の構成、主要コンポーネント、設計上の方針、およびユニットテストしやすくするための改善点をまとめたものです。

概要（ハイレベル）
-----------------
- バックエンド: `Flask` を用いた REST API と静的資産配信。
- データストア: `SQLite`（開発／軽量運用向け） + `SQLAlchemy` を想定。
- フロントエンド: サーバーで配信する静的 HTML/CSS/JS。UI ロジックは Vanilla JS（必要なら Vue 等を追加検討）。
- タイマー実行: クライアント側で実行（`Web Worker` 推奨）、重要イベントはサーバーへ記録。

推奨フォルダ構成
-----------------
- `1.pomodoro/`
  - `app.py` — アプリファクトリ（エントリ）
  - `config.py` — 設定（開発 / テスト / 本番）
  - `models.py` — DB モデル（`SQLAlchemy`）
  - `services/` — ビジネスロジック（TimerService 等）
  - `repositories/` — DB 操作（SessionRepository 等）
  - `templates/` — `index.html` など
  - `static/`
    - `css/` — スタイル
    - `js/` — `timerEngine.js`, `worker.js`, `ui.js`
    - `images/`
  - `tests/` — Python 側テスト（`unit/`, `integration/`）

バックエンド設計（責務分割）
---------------------------
- アプリファクトリパターン: `create_app(config_name)` を実装し、テストで設定を差し替え可能にします（`TESTING=True` と in-memory DB を使用）。
- ルーティングは薄く保ち、リクエスト検証と `Service` 呼び出しだけを行う（Thin Controllers）。
- `Service` 層: ビジネスロジック（セッション集計、開始/終了判定、設定管理）を `TimerService` / `SessionService` に集約。
- `Repository` 層: DB の CRUD を `SessionRepository` などに切り出し、モック注入でテスト可能にする。
- 依存性注入: 変数やコンストラクタで `service` / `repo` を注入できるようにし、テストで差し替えられる形に。
- 時刻抽象化: 実時間呼び出しを `Clock` インターフェースで隠蔽（テスト時は固定時刻や制御可能な Clock を注入）。

代表 API（例）
----------------
- `GET /api/status` — 現在設定・簡易ステータス取得
- `POST /api/session` — セッション完了を記録（{type, duration_seconds, started_at, finished_at}）
- `GET /api/sessions?date=YYYY-MM-DD` — 日別の履歴・集計を返す
- `PUT /api/settings` — ユーザー設定更新

データモデル（簡略）
--------------------
- `Session`:
  - `id`, `type` (work|break), `duration_seconds`, `started_at`, `finished_at`
- `Settings`:
  - `work_minutes`, `short_break_minutes`, `long_break_minutes`, `cycles_until_long_break`

フロントエンド設計
-----------------
- UI 構成:
  - ヘッダー（タイトル）
  - ドーナツタイマー（SVG + `stroke-dasharray`）
  - 中央の時間表示（`MM:SS`、`aria-live` を付与）
  - 操作ボタン（開始 / 一時停止 / リセット）
  - 今日の進捗カード（完了数、合計集中時間）
- タイマーエンジン:
  - コアな時間計測ロジックを `static/js/timerEngine.js` に純粋関数として実装。
  - 実際のカウントは `worker.js`（Web Worker）で行い、UI と `postMessage` で連携。
  - 時刻差は `Date.now()` の差分で計測し、`setInterval` の遅延に依存しない実装にする。
- オフライン対策:
  - ネットワーク不通時は `localStorage` / `IndexedDB` にイベントをキューし、復帰時に同期。

テスト方針（ユニットテスト容易化のための具体策）
-------------------------------------------
- Python 側:
  - `pytest` を利用。
  - `create_app`（アプリファクトリ）で `TESTING` 設定と in-memory SQLite を差し替え、DB フィクスチャを用意する（`tests/conftest.py`）。
  - ルートは `Flask.test_client()` で API テスト。ビジネスロジックは `Service` クラス単体でテスト。
  - 時刻依存は `freezegun` を使い安定化。
  - DB 操作は `Repository` をモックしてユニットテストし、統合テストで実 DB を使う。
- JavaScript 側:
  - ロジックは `timerEngine.js` の純粋関数で書き、`jest` + `jsdom` で単体テスト。
  - Web Worker ロジックはモジュール化し、Worker 本体は統合テストで検証。
  - 時間依存は `sinon` の Fake Timers を利用。
- テスト分類:
  - `unit/`（純粋ロジック）: 高速で細かく。
  - `integration/`（API と DB 組合せ）: `Flask.test_client()` + テスト DB。
  - `e2e/`（ユーザーフロー）: Playwright 等で主要な操作を確認。

CI と品質
-----------
- `pytest --cov`（`pytest-cov`）で Python カバレッジを計測。
- `eslint`/`prettier`（JS）で静的解析と整形。
- GitHub Actions でテストとリンティングを実行。

デプロイ
------
- 本番構成例: `Docker` イメージ（`gunicorn` 起動） + `nginx`（静的資産の最適配信・プロキシ）。
- 簡易デプロイ: `gunicorn "app:create_app('production')"` を想定。

テスト容易化のための改善点（要約）
--------------------------------
- アプリファクトリを必須にする。
- ルーティングを薄くし `Service` 層に分離する。
- DB 操作を `Repository` に切り出し、依存注入で差し替え可能にする。
- 時刻操作を抽象化する `Clock` インターフェースを導入する。
- フロントのコアロジックを純粋関数に分離して単体テスト可能にする。

次のステップ（提案）
------------------
1. `1.pomodoro` にアプリファクトリと最小ルーティングのスキャフォールドを作成。
2. `services/` と `repositories/` の雛形を追加。
3. `static/js/timerEngine.js` にコアロジックの初版を作る。

必要であれば、上記を自動でスキャフォールドしてコミットします。どのステップを先に進めますか？
