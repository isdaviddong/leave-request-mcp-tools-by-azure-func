# Leave Request Tools

這是一個以 Python Azure Functions 建立的測試專案，用於驗證 MCP Tool 的請假相關功能。服務提供請假天數查詢、請假申請與目前日期時間查詢，預設在本機 `http://localhost:7071` 執行。

## 功能

### `get_leave_record_amount`

查詢員工目前的請假天數。

參數：

| 名稱 | 類型 | 說明 |
| --- | --- | --- |
| `employeeName` | string | 員工姓名 |

目前內建資料：

- `david`：5 天
- `eric`：8 天
- 其他姓名：3 天（目前程式的預設值）

### `leave_request`

建立請假申請並回傳文字結果。

參數：

| 名稱 | 類型 | 必填 | 說明 |
| --- | --- | --- | --- |
| `startDate` | string | 是 | 請假起始日期，例如 `2026-09-28` |
| `days` | number | 否 | 請假天數 |
| `reason` | string | 是 | 請假事由 |
| `substitute` | string | 是 | 工作代理人 |
| `requesterName` | string | 是 | 請假者姓名 |

若缺少 `startDate`、`reason`、`substitute` 或 `requesterName`，會回傳請假失敗訊息。目前此功能只產生回覆，不會保存申請資料，也不會自動扣除請假天數。

### `get_current_date`

取得目前台灣時間，回傳格式為 `YYYY-MM-DD HH:MM:SS`。

## 環境需求

- Python 3.9 以上
- [Azure Functions Core Tools 下載與安裝](https://learn.microsoft.com/azure/azure-functions/functions-run-local)
- VS Code（可選）
- Python 虛擬環境（建議）

## 本機安裝

在專案根目錄執行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

若 PowerShell 不允許執行啟用腳本，也可以直接使用虛擬環境中的 Python：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 啟動服務

確認已安裝 Azure Functions Core Tools 後，在專案根目錄執行：

```powershell
func start
```

或在 VS Code 中執行工作 `func: host start`。

服務啟動後，MCP SSE 端點為：

```text
http://localhost:7071/runtime/webhooks/mcp/sse
```

VS Code 的 MCP 設定已放在 `.vscode/mcp.json`，設定名稱為 `Leave-Request-Tools-Local`。啟動 Azure Functions 後，即可透過支援 MCP 的用戶端連線並呼叫上述工具。

## 使用範例

透過 MCP 用戶端呼叫：

```json
{
  "tool": "get_leave_record_amount",
  "arguments": {
    "employeeName": "david"
  }
}
```

回傳內容：

```text
5
```

請假申請範例：

```json
{
  "tool": "leave_request",
  "arguments": {
    "startDate": "2026-09-28",
    "days": 2,
    "reason": "家庭事務",
    "substitute": "Eric",
    "requesterName": "David"
  }
}
```

回傳內容：

```text
David 請假 2天，從 2026-09-28 開始，事由為 家庭事務，代理人 Eric
```

## 專案檔案

- `function_app.py`：三個 MCP 工具的實作
- `host.json`：Azure Functions 主機設定；其中 `extensionBundle` 載入 MCP 擴充功能，`extensions.mcpToolTrigger` 設定 MCP 伺服器名稱、版本與工具說明
- `requirements.txt`：Python 相依套件
- `.vscode/mcp.json`：VS Code 的本機 MCP 用戶端設定；將 `Leave-Request-Tools-Local` 連線至 `http://localhost:7071/runtime/webhooks/mcp/sse`，讓支援 MCP 的用戶端可以使用本專案工具
- `.vscode/tasks.json`：VS Code 啟動工作
- `local.settings.json`：Azure Functions Core Tools 的本機設定檔；目前指定 Python worker、使用檔案儲存函式金鑰，並保留 `AzureWebJobsStorage` 為空值以供本機執行。若加入連線字串、金鑰或其他機密，請勿提交至版本庫

## 注意事項

- `local.settings.json` 未被 `.gitignore` 排除；若其中包含機密設定，請勿將檔案提交至版本庫。
- 目前請假資料為程式內的示範資料，服務重新啟動後不會保留新的請假申請。
- 正式環境部署前，應加入資料庫、身分驗證、輸入格式驗證與權限控管。
