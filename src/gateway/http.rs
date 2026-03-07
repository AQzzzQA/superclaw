// HTTP Gateway - SuperClaw 的 HTTP 网关
// 与 LemClaw Gateway 兼容，支持 RESTful API

use rocket::http::{Method, ContentType, Status};
use rocket::response::content::RawJson;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::Mutex;

// ========== 类型定义 ==========

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HttpRequest {
    pub method: String,
    pub path: String,
    pub headers: std::collections::HashMap<String, String>,
    pub body: Option<serde_json::Value>,
    pub query_params: Option<std::collections::HashMap<String, String>>,
    pub timestamp: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HttpResponse {
    pub success: bool,
    pub data: Option<serde_json::Value>,
    pub error: Option<String>,
    pub status_code: u16,
    pub timestamp: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentRequest {
    pub auth_code: String,
    pub message: String,
    pub model_provider: Option<String>,
    pub max_tokens: Option<usize>,
    pub temperature: Option<f32>,
    pub timeout_ms: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentResponse {
    pub success: bool,
    pub reply: Option<String>,
    pub model_used: Option<String>,
    pub tokens_used: Option<usize>,
    pub error: Option<String>,
    pub timestamp: i64,
}

// ========== LemClaw Gateway 代理 ==========

pub struct LemClawProxy {
    pub base_url: String,
    pub auth_token: String,
    pub client: Arc<reqwest::Client>,
}

impl LemClawProxy {
    pub fn new(base_url: String, auth_token: String) -> Self {
        Self {
            base_url,
            auth_token,
            client: Arc::new(reqwest::Client::new()),
        }
    }

    pub async fn send_message(&self, request: AgentRequest) -> anyhow::Result<AgentResponse> {
        let url = format!("{}/api/agent", self.base_url);
        
        let payload = serde_json::json!({
            "auth_code": request.auth_code,
            "message": request.message,
            "model_provider": request.model_provider,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "timeout_ms": request.timeout_ms,
        });

        let response = self.client
            .post(&url)
            .header("Authorization", format!("Bearer {}", self.auth_token))
            .header("Content-Type", "application/json")
            .json(&payload)
            .send()
            .await?;

        if response.status().is_success() {
            let json: serde_json::Value = response.json().await?;
            
            Ok(AgentResponse {
                success: true,
                reply: json["reply"].as_str().map(|s| s.to_string()),
                model_used: json["model_used"].as_str().map(|s| s.to_string()),
                tokens_used: json["tokens_used"].as_usize(),
                error: None,
                timestamp: chrono::Utc::now().timestamp_millis(),
            })
        } else {
            let error_text = response.text().await?;
            
            Ok(AgentResponse {
                success: false,
                reply: None,
                model_used: None,
                tokens_used: None,
                error: Some(format!("HTTP {}: {}", response.status(), error_text)),
                timestamp: chrono::Utc::now().timestamp_millis(),
            })
        }
    }

    pub async fn health_check(&self) -> anyhow::Result<bool> {
        let url = format!("{}/health", self.base_url);
        
        let response = self.client
            .get(&url)
            .header("Authorization", format!("Bearer {}", self.auth_token))
            .send()
            .await?;

        Ok(response.status().is_success())
    }
}

// ========== OpenClaw Gateway 代理 ==========

pub struct OpenClawProxy {
    pub base_url: String,
    pub gateway_token: String,
    pub client: Arc<reqwest::Client>,
}

impl OpenClawProxy {
    pub fn new(base_url: String, gateway_token: String) -> Self {
        Self {
            base_url,
            gateway_token,
            client: Arc::new(reqwest::Client::new()),
        }
    }

    pub async fn send_message(&self, request: AgentRequest) -> anyhow::Result<AgentResponse> {
        let url = format!("{}/api/agent", self.base_url);
        
        let payload = serde_json::json!({
            "auth_code": request.auth_code,
            "message": request.message,
            "model_provider": request.model_provider,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "timeout_ms": request.timeout_ms,
        });

        let response = self.client
            .post(&url)
            .header("Authorization", format!("Bearer {}", self.gateway_token))
            .header("Content-Type", "application/json")
            .json(&payload)
            .send()
            .await?;

        if response.status().is_success() {
            let json: serde_json::Value = response.json().await?;
            
            Ok(AgentResponse {
                success: true,
                reply: json["reply"].as_str().map(|s| s.to_string()),
                model_used: json["model_used"].as_str().map(|s| s.to_string()),
                tokens_used: json["tokens_used"].as_usize(),
                error: None,
                timestamp: chrono::Utc::now().timestamp_millis(),
            })
        } else {
            let error_text = response.text().await?;
            
            Ok(AgentResponse {
                success: false,
                reply: None,
                model_used: None,
                tokens_used: None,
                error: Some(format!("HTTP {}: {}", response.status(), error_text)),
                timestamp: chrono::Utc::now().timestamp_millis(),
            })
        }
    }

    pub async fn health_check(&self) -> anyhow::Result<bool> {
        let url = format!("{}/health", self.base_url);
        
        let response = self.client
            .get(&url)
            .header("Authorization", format!("Bearer {}", self.gateway_token))
            .send()
            .await?;

        Ok(response.status().is_success())
    }
}

// ========== 路由 ==========

#[get("/health")]
pub async fn health_check() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "healthy",
        "gateway": "http",
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}

#[post("/api/agent")]
pub async fn agent_message(
    request: Json<AgentRequest>,
    lemlaw_proxy: &rocket::State<Arc<LemClawProxy>>,
    openclaw_proxy: &rocket::State<Arc<OpenClawProxy>>,
) -> Json<AgentResponse> {
    log::info!("Received agent message request");

    // 尝试 LemClaw Gateway
    match lemlaw_proxy.send_message(request.into_inner()).await {
        Ok(response) => {
            if response.success {
                return Json(response);
            }
        }
        Err(e) => {
            log::error!("LemClaw Gateway error: {:?}", e);
        }
    }

    // LemClaw 失败，尝试 OpenClaw Gateway
    match openclaw_proxy.send_message(request.into_inner()).await {
        Ok(response) => {
            if response.success {
                return Json(response);
            }
        }
        Err(e) => {
            log::error!("OpenClaw Gateway error: {:?}", e);
        }
    }

    // 两个都失败
    Json(AgentResponse {
        success: false,
        reply: None,
        model_used: None,
        tokens_used: None,
        error: Some("Both LemClaw and OpenClaw gateways failed".to_string()),
        timestamp: chrono::Utc::now().timestamp_millis(),
    })
}

#[get("/api/status")]
pub async fn gateway_status(
    lemlaw_proxy: &rocket::State<Arc<LemClawProxy>>,
    openclaw_proxy: &rocket::State<Arc<OpenClawProxy>>,
) -> Json<serde_json::Value> {
    let lemlaw_health = lemlaw_proxy.health_check().await.unwrap_or(false);
    let openclaw_health = openclaw_proxy.health_check().await.unwrap_or(false);

    Json(serde_json::json!({
        "lemlaw_gateway": {
            "healthy": lemlaw_health,
            "url": lemlaw_proxy.base_url,
        },
        "openclaw_gateway": {
            "healthy": openclaw_health,
            "url": openclaw_proxy.base_url,
        },
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}
