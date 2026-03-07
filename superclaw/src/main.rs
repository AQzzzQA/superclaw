// SuperClaw - Super Claw AI Platform
// 超爪 v1.0.0
// 双网关：OpenClaw Gateway (WebSocket) + LemClaw Gateway (HTTP)

use rocket::State;
use rocket::fs::{File, NamedFile};
use rocket::http::{Method, ContentType, Status};
use rocket::serde::{json, Deserialize};
use rocket::request::FromRequest;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;
use std::env;

#[macro_use] extern crate rocket;
#[get]
use rocket::State;
use rocket::http::Method;
use rocket::fs::{File, NamedFile};
use rocket::http::{Method, ContentType, Status};
use rocket::serde::{json, Deserialize};
use rocket::request::FromRequest;
use rocket::futures::TryStreamExt;
use std::sync::Arc;
use tokio::sync::Mutex;
use std::collections::HashMap;
use std::env;

// ========== 常量定义 ==========

const API_VERSION: &str = env!("CARGO_PKG_VERSION");
const AUTHOR: &str = env!("CARGO_PKG_AUTHOR");
const HOMEPAGE: &str = env!("CARGO_PKG_HOMEPAGE");

// ========== 状态管理 ==========

#[derive(Debug, Clone)]
pub struct AppState {
    pub gateway_status: GatewayStatus,
    pub lemlaw_status: GatewayStatus,
    pub last_health_check: Option<i64>,
}

#[derive(Debug)]
pub enum GatewayStatus {
    Healthy,
    Degraded,
    Disconnected,
}

// ========== Gateway 配置 ==========

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GatewayConfig {
    pub openclaw_gateway: Option<String>,
    pub lemlaw_gateway: Option<String>,
    pub secret_token: Option<String>,
    pub bind_address: String,
    pub port: u16,
}

// ========== LemClaw 配置 ==========

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LemClawConfig {
    pub gateway_url: String,
    pub auth_token: String,
    pub client_name: String,
    pub enabled: bool,
}

// ========== 数据库配置 ==========

#[derive(Debug, Clone)]
pub struct DbConfig {
    pub database_url: String,
    pub max_connections: u32,
    pub min_connections: u32,
}

// ========== 配置 ==========

pub struct AppConfig {
    pub gateway: GatewayConfig,
    pub lemlaw: LemClawConfig,
    pub database: DbConfig,
    pub bind_address: String,
    pub port: u16,
    pub secret_token: Option<String>,
    pub app_env: String,
}

impl AppState {
    pub fn load() -> Self {
        let config = Self::load_from_env();
        
        Self {
            gateway_status: GatewayStatus::Healthy,
            lemlaw_status: GatewayStatus::Healthy,
            last_health_check: Some(0),
        }
    }
    
    fn load_from_env() -> Self {
        use std::env;

        Self {
            gateway_status: Self::check_openclaw_gateway(),
            lemlaw_status: Self::check_lemclaw_gateway(),
            last_health_check: Some(0),
        }
    }
    
    fn check_openclaw_gateway() -> GatewayStatus {
        // 检查 OpenClaw Gateway
        // 实现中...
        GatewayStatus::Healthy
    }
    
    fn check_lemclaw_gateway() -> GatewayStatus {
        // 检查 LemClaw Gateway
        // 实现中...
        GatewayStatus::Healthy
    }
    
    fn health_check_interval(&self) -> i64 {
        self.last_health_check.unwrap_or(0) + 300_000 // 5 分钟
    }
}

// ========== 路由 ==========

#[get("/")]
async fn index(state: &State, _config: AppState) -> Json<JsonValue> {
    state.gateway_status = GatewayStatus::Healthy;
    
    Json(json!({
        "status": "healthy",
        "version": env!("CARGO_PKG_VERSION"),
        "timestamp": chrono::Utc::now().to_rfc3339(),
        "openclaw_gateway": state.gateway_status.to_string(),
        "lemclaw_gateway": state.lemclaw_status.to_string(),
    }))
}

#[get("/health")]
async fn health(state: &State) -> Json<JsonValue> {
    let _ = state.health_check_interval(&state);
    
    Json(json!({
        "status": state.gateway_status.to_string(),
        "lemclaw_health": "ok",
        "timestamp": chrono::Utc::now().to_rfc3339(),
    }))
}

// ========== 双网关代理 ==========

#[post("/api/gateway")]
async fn proxy_to_openclaw(
    state: &State,
    req: Json<Value>,
) -> Json<JsonValue> {
    let auth_code = req.get("auth_code").and_then(|code| {
        match code {
            Some(code) => {
                // 转发到 OpenClaw Gateway
                match req.get("message").and_then(|msg| {
                    Some(msg) => {
                        let openclaw_url = state.config.openclaw_gateway.as_ref().ok_or_else(|| {
                            "http://localhost:18789/api".to_string()
                        });
                        
                        let response = reqwest::Client::new()
                            .post(openclaw_url)
                            .json(&serde_json::json!({
                                "auth_code": code,
                                "message": msg,
                            }))
                            .send()
                            .await;
                        
                        match response.status() {
                            rocket::http::Status::Ok => {
                                // 成功
                                if let Some(data) = response.json() {
                                    let reply_text = extract_reply_text(&data);
                                    return Json(json!({
                                        "success": true,
                                        "reply": reply_text
                                    });
                                }
                                _ => {
                                    return Json(json!({
                                        "success": false,
                                        "error": response.status().to_string(),
                                    }));
                                }
                            }
                    }
                    None => {
                        return Json(json!({"error": "No message provided"}));
                    }
                }
            }
            None => {
                return Json(json!({"error": "Authorization code is required"}));
            }
        }
    }).await
}

#[post("/api/lemclaw")]
async fn proxy_to_lemclaw(
    state: &State,
    req: Json<Value>,
) -> Json<JsonValue> {
    let auth_token = state.config.lemlaw_gateway.as_ref().ok_or_else(|| {
        "http://localhost:8089/api".to_string()
    });
    
    let lemlaw_url = state.config.lemlaw_gateway.as_ref().ok_or_else(|| {
        "http://localhost:8089/api".to_string()
    });
    
    match req.get("auth_token").and_then(|token| {
        Some(token) => {
            match req.get("message").and_then(|msg| {
                Some(msg) => {
                    // 转发到 LemClaw Gateway
                    let response = reqwest::Client::new()
                        .post(lemclaw_url)
                        .header("Authorization", format!("Bearer {}", token))
                        .json(&serde_json::json!({
                            "auth_token": token,
                            "message": msg,
                        }))
                        .send()
                        .await;
                        
                        match response.status() {
                            rocket::http::Status::Ok => {
                                if let Some(data) = response.json() {
                                    let reply_text = extract_reply_text(&data);
                                    return Json(json!({
                                        "success": true,
                                        "reply": reply_text,
                                    });
                                }
                                _ => {
                                    return Json(json!({
                                        "success": false,
                                        "error": response.status().to_string(),
                                    }));
                                }
                            }
                    }
                    None => {
                        return Json(json!({"error": "No message provided"}));
                    }
                }
            }
            None => {
                return Json(json!({"error": "LemClaw token is required"}));
            }
        }
    }).await
}

// ========== 辅助函数 ==========

fn extract_reply_text(data: &Json) -> Option<String> {
    // 从 LemClaw/OpenClaw 的响应中提取回复文本
    // 实现中...
    None
}