# lifx-mcp

LIFXスマート電球をRGB値で制御するMCPサーバー

## 要件

- LIFX電球が同じローカルネットワーク上にあること
- Python 3.12以上
- ネットワークでUDPポート56700が開放されていること

## 機能

- RGB値(0-255)に基づいてLIFX電球の色を変更
- 入力値のバリデーション(0-255の範囲チェック)
- RGB値をLIFX形式に自動変換

## 使用方法

1. 依存関係をインストール:
```bash
uv pip install -e .
```

2. MCPサーバーを起動:
```bash
uv run src/lifx_mcp/server.py
```

3. `control_light_by_rgb`ツールを使用:
```json
{
  "red": 255,
  "green": 100,
  "blue": 50
}
```

4. 電球が応答しない場合:
- 電球の電源を確認
- 同じネットワークに接続されているか確認
- ファイアウォール設定を確認
