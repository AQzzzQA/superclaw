// Agent Orchestrator API 路由
// 智能体编排的 HTTP 端点

use rocket::State;
use rocket::serde::json::Json;
use serde::{Deserialize, Serialize};
use std::sync::Arc;

// 导入 Orchestrator
use crate::agents::orchestrator::{
    Orchestrator,
    get_builtin_agents,
    Task,
    AgentType,
    ExecutionResult,
    OrchestratedResult,
};

// ========== 请求/响应类型 ==========

#[derive(Debug, Deserialize)]
pub struct ParallelExecutionRequest {
    pub tasks: Vec<Task>,
    pub agent_types: Vec<AgentType>,
}

#[derive(Debug, Deserialize)]
pub struct SequentialExecutionRequest {
    pub tasks: Vec<Task>,
    pub agent_types: Vec<AgentType>,
}

#[derive(Debug, Deserialize)]
pub struct TaskDecompositionRequest {
    pub task: Task,
}

#[derive(Debug, Deserialize)]
pub struct AgentRegistrationRequest {
    pub agent: AgentType,
}

// ========== 状态管理 ==========

pub struct OrchestratorState {
    pub orchestrator: Arc<Orchestrator>,
}

// ========== 路由处理函数 ==========

/// 获取可用智能体列表
#[get("/api/agents/list")]
pub async fn list_agents() -> Json<serde_json::Value> {
    log::info!("Listing available agents");

    let agents = get_builtin_agents();
    
    Json(serde_json::json!({
        "success": true,
        "agents": agents,
        "count": agents.len(),
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}

/// 并行执行任务
#[post("/api/agents/parallel")]
pub async fn execute_parallel(
    request: Json<ParallelExecutionRequest>,
    state: &State<OrchestratorState>,
) -> Json<OrchestratedResult> {
    log::info!("Received parallel execution request: {} tasks", request.tasks.len());

    if request.tasks.is_empty() {
        return Json(OrchestratedResult {
            task_id: String::new(),
            total_tasks: 0,
            completed_tasks: 0,
            results: vec![],
            aggregated_output: serde_json::json!({}),
            total_execution_time_ms: 0,
            timestamp: chrono::Utc::now().timestamp_millis(),
        });
    }

    let result = state.orchestrator.execute_parallel(
        request.tasks.clone(),
        request.agent_types.clone(),
    ).await;

    Json(result)
}

/// 串行执行任务
#[post("/api/agents/sequential")]
pub async fn execute_sequential(
    request: Json<SequentialExecutionRequest>,
    state: &State<OrchestratorState>,
) -> Json<OrchestratedResult> {
    log::info!("Received sequential execution request: {} tasks", request.tasks.len());

    if request.tasks.is_empty() {
        return Json(OrchestratedResult {
            task_id: String::new(),
            total_tasks: 0,
            completed_tasks: 0,
            results: vec![],
            aggregated_output: serde_json::json!({}),
            total_execution_time_ms: 0,
            timestamp: chrono::Utc::now().timestamp_millis(),
        });
    }

    let result = state.orchestrator.execute_sequential(
        request.tasks.clone(),
        request.agent_types.clone(),
    ).await;

    Json(result)
}

/// 分解任务
#[post("/api/agents/decompose")]
pub async fn decompose_task(
    request: Json<TaskDecompositionRequest>,
) -> Json<serde_json::Value> {
    log::info!("Decomposing task: {}", request.task.name);

    let orchestrator = Orchestrator::new(5);
    let subtasks = orchestrator.decompose_task(request.task);

    Json(serde_json::json!({
        "success": true,
        "task": request.task,
        "subtasks": subtasks,
        "subtask_count": subtasks.len(),
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}

/// 注册新智能体
#[post("/api/agents/register")]
pub async fn register_agent(
    request: Json<AgentRegistrationRequest>,
) -> Json<serde_json::Value> {
    log::info!("Registering new agent: {}", request.agent.name);

    let orchestrator = Orchestrator::new(5);

    match orchestrator.agent_pool.register_agent(request.agent).await {
        Ok(_) => {
            Json(serde_json::json!({
                "success": true,
                "message": format!("Agent {} registered successfully", request.agent.name),
                "agent": request.agent,
                "timestamp": chrono::Utc::now().timestamp_millis(),
            }))
        }
        Err(error) => {
            Json(serde_json::json!({
                "success": false,
                "error": error,
                "timestamp": chrono::Utc::now().timestamp_millis(),
            }))
        }
    }
}

/// 获取智能体状态
#[get("/api/agents/status")]
pub async fn get_agent_status(
    state: &State<OrchestratorState>,
) -> Json<serde_json::Value> {
    log::info!("Getting agent pool status");

    // 获取当前注册的智能体
    let agents = get_builtin_agents();

    Json(serde_json::json!({
        "success": true,
        "agents": agents,
        "max_concurrent": state.orchestrator.max_parallel_tasks,
        "timestamp": chrono::Utc::now().timestamp_millis(),
    }))
}
