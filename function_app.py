import azure.functions as func
from datetime import datetime, timezone, timedelta
import json
import logging

app = func.FunctionApp()

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="get_leave_record_amount",
    description="取得請假天數",
    toolProperties='[{"propertyName": "employeeName", "propertyType": "string", "description": "要查詢請假天數的員工名稱"}]'
)
def get_leave_record_amount(context: str) -> str:
    request = json.loads(context)
    arguments = request.get("arguments", {})
    employee_name = str(arguments.get("employeeName", ""))

    leave_days = {"david": 5, "eric": 8}.get(employee_name.lower(), 3)
    return json.dumps({"content": str(leave_days)})

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="leave_request",
    description="進行請假，回傳結果",
    toolProperties='[{"propertyName": "startDate", "propertyType": "string", "description": "請假起始日期"}, {"propertyName": "days", "propertyType": "number", "description": "請假天數"}, {"propertyName": "reason", "propertyType": "string", "description": "請假事由"}, {"propertyName": "substitute", "propertyType": "string", "description": "代理人"}, {"propertyName": "requesterName", "propertyType": "string", "description": "請假者姓名"}]'
)
def leave_request(context: str) -> str:
    request = json.loads(context)
    arguments = request.get("arguments", {})
    start_date = str(arguments.get("startDate", ""))
    days = arguments.get("days", 0)
    reason = str(arguments.get("reason", ""))
    substitute = str(arguments.get("substitute", ""))
    requester_name = str(arguments.get("requesterName", ""))

    if not all([start_date, reason, substitute, requester_name]):
        result = "請假失敗，請確認所有必填欄位已填寫。"
    else:
        result = (
            f"{requester_name} 請假 {days}天，從 {start_date} 開始，"
            f"事由為 {reason}，代理人 {substitute}"
        )

    return json.dumps({"content": result})


@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="get_current_date",
    description="取得今天日期",
    toolProperties="[]"
)
def get_current_date(context: str) -> str:
    del context
    taiwan_time = datetime.now(timezone.utc) + timedelta(hours=8)
    return json.dumps({"content": taiwan_time.strftime("%Y-%m-%d %H:%M:%S")})