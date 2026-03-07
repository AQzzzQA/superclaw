// LemClaw Echo Skills - Echo 智能体自动化能力
// 基于 LemClaw API 实现自动修复、代码生成、文档生成等

use reqwest::Client;
use reqwest::Error;
use serde::{Deserialize, Serialize};
use serde_json::json;

#[get("/lemclaw")]
async fn lemlaw_handler(state: &State) -> Json<JsonValue> {
    let lemlaw_url = state.config.lemlaw_gateway.as_ref().ok_or_else(|| "http://localhost:8089".to_string());
    
    // 尝试获取健康状态
    match reqwest::Client::new(&lemclaw_url)
        Ok(client) => {
            // 获取 Token
            if let Some(token) = &state.config.lemlaw_gateway.auth_token.as_ref().ok_or_else(|| {
                eprintln!("LemClaw Token not configured");
                return Json(json!({"error": "LemClaw Token not configured"}));
            });
            
            // 发送 echo 消息
            let echo_payload = json!({
                "message": "Hello, LemClaw!",
            });
            
            match client
                .post(&format!("{}/api/agent/message", lemlaw_url))
                .header("Content-Type", "application/json")
                .header("Authorization", format!("Bearer {}", token))
                .json(&echo_payload)
                .await
                Ok(response) => {
                    if response.status().is_success() {
                        if let Some(data) = response.json() {
                            if let Some(text) = data["text"].as_str() {
                                return Json(json!({
                                    "success": true,
                                    "message": text,
                                }));
                            }
                        }
                        response.status().is_client_error() => {
                            return Json(json!({
                                "success": false,
                                "error": response.text().unwrap_or_else("Unknown error"),
                                }));
                        }
                    }
                    Err(e) => {
                        eprintln!("LemClaw request failed: {}", e);
                        return Json(json!({"success": false, "error": format!("{}", e)}));
                    }
                }
        Err(e) => {
            eprintln!("Failed to create LemClaw client: {}", e);
            return Json(json!({"success": false, "error": format!("{}", e)}));
        }
    };
}

#[get("/lemclaw/echo")]
async fn echo_handler(state: &State) -> Json<JsonValue> {
    let lemlaw_url = state.config.lemlaw_gateway.as_ref().ok_or_else(|| "http://localhost:8089".to_string());
    
    match reqwest::Client::new(&lemclaw_url) {
        Ok(client) => {
            // 返回简单的响应
            Json(json!({
                "message": "Echo Skills ready!",
                "echo_handler": "Echo Skills ready!",
                }))
        }
        Err(e) => {
            Json(json!({"error": format!("{}", e)}))
        }
    }
}

#[get("/lemclaw/code/format")]
async fn code_format_handler(state: &State) -> Json<JsonValue> {
    let lemlaw_url = state.config.lemlaw_gateway.as_ref().ok_or_else(|| "http://localhost:8089".to_string());
    
    match reqwest::Client::new(&lemclaw_url) {
        Ok(client) => {
            // 返回代码格式化示例
            Json(json!({
                "message": "Code format ready!",
                "code_format_handler": "Code format handler ready!",
                }))
        }
        Err(e) => {
            Json(json!({"error": format!("{}", e)}))
        }
    }
}

#[get("/lemclaw/changelog")]
async fn changelog_handler(state: &State) -> Json<JsonValue> {
    let lemlaw_url = state.config.lemlaw_gateway.as_ref().ok_or_else(|| "http://localhost:8089/api/v2");
    
    // 尝试获取 changelog
    match reqwest::Client::new(&lemlaw_url) {
        Ok(client) => {
            let token = state.config.lemlaw_gateway.auth_token.as_ref().ok_or_else(|| {
                return Json(json!({"error": "LemClaw Token not configured"});
            });
            
            match client
                .get(&format!("{}/api/changelog", lemlaw_url))
                .bearer_auth(state.config.lemlaw_gateway.auth_token.as_ref().ok_or_else(|| ""))
                .send().await
                .await
                Ok(response) => {
                    if response.status().is_success() {
                        if let Some(data) = response.json() {
                            // 解析 changelog
                            let changelog = data.as_array().unwrap_or_default(&[]);
                            
                            return Json(json!({
                                "success": true,
                                "changelog": changelog,
                                }));
                        }
                    }
                    
                    response.status().is_client_error() | response.status().is_server_error() => {
                        return Json(json!({
                            "success": false,
                            "error": response.text().unwrap_or_else("Unknown error"),
                            }));
                    }
                    
                    _ => {
                        return Json(json!({
                            "success": false,
                            "error": "HTTP {}", response.status()),
                            }));
                    }
                }
            Err(e) => {
                eprintln!("LemClaw changelog request failed: {}", e);
                return Json(json!({"success": false, "error": format!("{}", e)}));
            }
        }
        Err(e) => {
            Json(json!({"error": format!("{}", e)}))
        }
    }
}

#[get("/lemclaw/license")]
async fn license_handler(state: &State) -> Json<JsonValue> {
    let lemlaw_url = state.config.lemlaw_gateway.as_ref().ok_or_else(|| "http://localhost:8089/api/v2");
    
    match reqwest::Client::new(&lemclaw_url) {
        Ok(client) => {
            let token = state.config.lemlaw_gateway.auth_token.as_ref().ok_or_else(|| {
                return Json(json!({"error": "LemClaw Token not configured"}));
            });
            
            match client
                .get(&format!("{}/api/license", lemlaw_url))
                .bearer_auth(&state.config.lemlaw_gateway.auth_token.as_ref().ok_or_else(|| ""))
                .send().await
                .await
                Ok(response) => {
                    if response.status().is_success() {
                        if let Some(license_text) = response.text() {
                            return Json(json!({
                                "success": true,
                                "license": license_text,
                                }));
                        }
                    }
                    
                    response.status().is_client_error() | response.status().is_server_error() => {
                        return Json(json!({
                            "success": false,
                            "error": response.text().unwrap_or_else("Unknown error"),
                            }));
                    }
                    
                    _ => {
                        return Json(json!({
                            "success": false,
                            "error": "HTTP {}", response.status(),
                            }));
                    }
                }
            Err(e) => {
                eprintln!("LemClaw license request failed: {}", e);
                return Json(json!({"success": false, "error": format!("{}", e)}));
            }
        }
        Err(e) => {
            Json(json!({"error": format!("{}", e)}))
        }
    }
}