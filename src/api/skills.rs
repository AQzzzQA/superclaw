// Skills API 路由 - Echo Skills 相关的 HTTP 端点

use rocket::State;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::RwLock;

// 导入 Echo Skills
use crate::skills::{CodeScanner, AutoFixer, SmartGenerator, ScanResult, FixResult, GenerationResult};

// ========== 请求/响应类型 ==========

#[derive(Debug, Deserialize)]
pub struct ScanRequest {
    pub workspace_path: String,
}

#[derive(Debug, Deserialize)]
pub struct FixRequest {
    pub workspace_path: String,
    pub issues: Vec<CodeIssue>,
}

#[derive(Debug, Deserialize)]
pub struct GenerateChangelogRequest {
    pub workspace_path: String,
    pub changes: Vec<String>,
}

// ========== 状态管理 ==========

pub struct SkillsState {
    pub scanner: Arc<RwLock<CodeScanner>>,
    pub fixer: Arc<RwLock<AutoFixer>>,
    pub generator: Arc<RwLock<SmartGenerator>>,
}

// ========== 路由处理函数 ==========

/// 健康检查
#[get("/api/skills/health")]
pub async fn skills_health() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "healthy",
        "service": "echo-skills",
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}

/// 扫描代码库
#[post("/api/skills/scan")]
pub async fn scan_workspace(
    request: Json<ScanRequest>,
) -> Json<ScanResult> {
    log::info!("Scanning workspace: {}", request.workspace_path);

    let scanner = CodeScanner::new(request.workspace_path.clone());
    
    match scanner.scan().await {
        Ok(result) => {
            log::info!("Scan completed: {} issues found", result.total_issues);
            Json(result)
        }
        Err(e) => {
            log::error!("Scan failed: {:?}", e);
            Json(ScanResult {
                success: false,
                issues: Vec::new(),
                total_issues: 0,
                scan_duration_ms: 0,
                timestamp: chrono::Utc::now().timestamp_millis(),
            })
        }
    }
}

/// 自动修复问题
#[post("/api/skills/fix")]
pub async fn fix_issues(
    request: Json<FixRequest>,
) -> Json<Vec<FixResult>> {
    log::info!("Fixing issues in workspace: {}", request.workspace_path);

    let fixer = AutoFixer::new(request.workspace_path.clone());
    let results = fixer.fix_issues(request.issues).await;
    
    log::info!("Fix completed: {} results", results.len());
    Json(results)
}

/// 生成 CHANGELOG
#[post("/api/skills/generate/changelog")]
pub async fn generate_changelog(
    request: Json<GenerateChangelogRequest>,
) -> Json<GenerationResult> {
    log::info!("Generating CHANGELOG for workspace: {}", request.workspace_path);

    let generator = SmartGenerator::new(request.workspace_path.clone());
    let result = generator.generate_changelog(request.changes).await;
    
    if result.success {
        log::info!("CHANGELOG generated successfully");
    } else {
        log::error!("CHANGELOG generation failed: {:?}", result.error);
    }
    
    Json(result)
}

/// 生成 LICENSE
#[get("/api/skills/generate/license")]
pub async fn generate_license(
    request: Json<ScanRequest>,
) -> Json<GenerationResult> {
    log::info!("Generating LICENSE for workspace: {}", request.workspace_path);

    let generator = SmartGenerator::new(request.workspace_path.clone());
    let result = generator.generate_license().await;
    
    if result.success {
        log::info!("LICENSE generated successfully");
    } else {
        log::error!("LICENSE generation failed: {:?}", result.error);
    }
    
    Json(result)
}
