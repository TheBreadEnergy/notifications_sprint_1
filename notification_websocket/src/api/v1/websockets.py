from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.services.websockets import manager

router = APIRouter()


@router.post("/notify/{user_id}")
async def receive_notification(notification: dict, user_id: str):
    await manager.send_personal_message(notification["message"], user_id)
    return {"message": "Notification sent to the user"}


@router.websocket("/notify/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            message = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)
