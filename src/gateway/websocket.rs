// WebSocket Gateway - SuperClaw 的 WebSocket 网关
// 与 OpenClaw Gateway 兼容，支持实时消息推送

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{Mutex, broadcast};
use rocket::futures::{StreamExt, SinkExt};
use rocket::http::{Method, ContentType, Status};
use rocket::response::content::RawJson;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use tokio_tungstenite::tungstenite::Message;
use futures::lock::Mutex as FuturesMutex;
use std::pin::Pin;

// ========== 类型定义 ==========

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebSocketMessage {
    pub message_type: String,
    pub session_id: Option<String>,
    pub user_id: Option<String>,
    pub payload: serde_json::Value,
    pub timestamp: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebSocketResponse {
    pub success: bool,
    pub data: Option<serde_json::Value>,
    pub error: Option<String>,
    pub message_id: Option<String>,
}

// ========== 连接管理器 ==========

pub struct ConnectionManager {
    pub connections: Arc<Mutex<HashMap<String, tokio_tungstenite::WebSocketStream<tokio::net::TcpStream>>>>,
    pub broadcast_tx: broadcast::Sender<WebSocketMessage>,
}

impl ConnectionManager {
    pub fn new() -> Self {
        let (broadcast_tx, _) = broadcast::channel(1000);
        
        Self {
            connections: Arc::new(Mutex::new(HashMap::new())),
            broadcast_tx,
        }
    }

    pub async fn add_connection(&self, session_id: String, stream: tokio_tungstenite::WebSocketStream<tokio::net::TcpStream>) {
        let mut connections = self.connections.lock().await;
        connections.insert(session_id.clone(), stream);
        log::info!("WebSocket connection added: {}", session_id);
    }

    pub async fn remove_connection(&self, session_id: &str) {
        let mut connections = self.connections.lock().await;
        connections.remove(session_id);
        log::info!("WebSocket connection removed: {}", session_id);
    }

    pub async fn send_to_session(&self, session_id: &str, message: WebSocketMessage) -> anyhow::Result<()> {
        let connections = self.connections.lock().await;
        
        if let Some(stream) = connections.get(session_id) {
            let mut stream = stream.clone();
            let json = serde_json::to_string(&message)?;
            
            tokio::spawn(async move {
                let mut stream = stream;
                stream.send(Message::Text(json)).await.ok();
            });
            
            Ok(())
        } else {
            Err(anyhow::anyhow!("Session not found: {}", session_id))
        }
    }

    pub async fn broadcast(&self, message: WebSocketMessage) {
        let _ = self.broadcast_tx.send(message);
    }
}

// ========== WebSocket 处理器 ==========

pub async fn handle_websocket_connection(
    ws: tokio_tungstenite::WebSocketStream<tokio::net::TcpStream>,
    manager: Arc<ConnectionManager>,
    session_id: String,
) -> anyhow::Result<()> {
    log::info!("WebSocket connection established: {}", session_id);
    
    // 添加连接到管理器
    manager.add_connection(session_id.clone(), ws).await;
    
    // 接收消息循环
    let mut ws = ws;
    
    loop {
        tokio::select! {
            // 接收 WebSocket 消息
            message = ws.next() => {
                match message {
                    Some(Ok(msg)) => {
                        match msg {
                            Message::Text(text) => {
                                if let Ok(ws_message) = serde_json::from_str::<WebSocketMessage>(&text) {
                                    log::info!("Received message from session {}: {:?}", session_id, ws_message.message_type);
                                    
                                    // 处理消息
                                    handle_websocket_message(ws_message, &session_id, &manager).await;
                                }
                            }
                            Message::Ping(ping) => {
                                ws.send(Message::Pong(ping)).await?;
                            }
                            Message::Pong(_) => {
                                // 忽略 Pong
                            }
                            Message::Close(_) => {
                                log::info!("WebSocket connection closed by client: {}", session_id);
                                manager.remove_connection(&session_id).await;
                                break;
                            }
                            _ => {}
                        }
                    }
                    Some(Err(e)) => {
                        log::error!("WebSocket error: {:?}", e);
                        manager.remove_connection(&session_id).await;
                        break;
                    }
                    None => {
                        log::info!("WebSocket connection closed: {}", session_id);
                        manager.remove_connection(&session_id).await;
                        break;
                    }
                }
            }
        }
    }
    
    Ok(())
}

// ========== 消息处理 ==========

async fn handle_websocket_message(
    message: WebSocketMessage,
    session_id: &str,
    manager: &Arc<ConnectionManager>,
) {
    match message.message_type.as_str() {
        "ping" => {
            // 响应 ping
            let response = WebSocketMessage {
                message_type: "pong".to_string(),
                session_id: Some(session_id.to_string()),
                user_id: message.user_id,
                payload: serde_json::json!({}),
                timestamp: chrono::Utc::now().timestamp_millis(),
            };
            
            let _ = manager.send_to_session(session_id, response).await;
        }
        
        "message" => {
            // 处理用户消息
            let response = WebSocketResponse {
                success: true,
                data: Some(serde_json::json!({
                    "message": "Message received",
                    "session_id": session_id,
                })),
                error: None,
                message_id: None,
            };
            
            let ws_message = WebSocketMessage {
                message_type: "response".to_string(),
                session_id: Some(session_id.to_string()),
                user_id: message.user_id,
                payload: serde_json::to_value(response).unwrap(),
                timestamp: chrono::Utc::now().timestamp_millis(),
            };
            
            let _ = manager.send_to_session(session_id, ws_message).await;
        }
        
        "subscribe" => {
            // 订阅主题
            log::info!("Session {} subscribed to topics", session_id);
        }
        
        _ => {
            log::warn!("Unknown message type: {}", message.message_type);
        }
    }
}

// ========== 路由 ==========

#[get("/ws")]
pub async fn websocket_handler(
    ws: rocket::WebSocket,
    state: &rocket::State<Arc<ConnectionManager>>,
) -> rocket::response::Responder<'static, rocket::response::stream::ReaderStream<std::io::Cursor<()>>> {
    log::info!("WebSocket connection request");
    
    // 生成会话 ID
    let session_id = uuid::Uuid::new_v4().to_string();
    
    rocket::Response::build()
        .status(rocket::http::Status::SwitchingProtocols)
        .header(rocket::http::Header::new("Connection", "Upgrade"))
        .header(rocket::http::Header::new("Upgrade", "websocket"))
        .ok()
}

#[post("/api/websocket/message")]
pub async fn websocket_api_message(
    message: Json<WebSocketMessage>,
    state: &rocket::State<Arc<ConnectionManager>>,
) -> Json<WebSocketResponse> {
    log::info!("Received WebSocket API message");
    
    Json(WebSocketResponse {
        success: true,
        data: Some(serde_json::json!({
            "message": "Message received via API",
            "timestamp": chrono::Utc::now().timestamp_millis(),
        })),
        error: None,
        message_id: None,
    })
}

#[get("/api/websocket/connections")]
pub async fn list_connections(
    state: &rocket::State<Arc<ConnectionManager>>,
) -> Json<serde_json::Value> {
    let connections = state.connections.lock().await;
    
    Json(serde_json::json!({
        "connections": connections.len(),
        "session_ids": connections.keys().collect::<Vec<_>>(),
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}
