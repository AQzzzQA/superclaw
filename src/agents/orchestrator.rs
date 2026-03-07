// Agent Orchestrator - 智能体编排器
// 支持并行、串行、任务分解、结果汇总

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{Mutex, Semaphore};
use tokio::task::JoinSet;
use serde::{Deserialize, Serialize};
use futures::future::join_all;
use chrono::{Utc, Duration};

// ========== 类型定义 ==========

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub name: String,
    pub description: String,
    pub input_data: serde_json::Value,
    pub dependencies: Vec<String>,
    pub timeout_ms: Option<u64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentType {
    pub id: String,
    pub name: String,
    pub capabilities: Vec<String>,
    pub model_provider: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionRequest {
    pub task_id: String,
    pub agent_type: AgentType,
    pub input: serde_json::Value,
    pub config: ExecutionConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionConfig {
    pub parallel: bool,
    pub timeout_ms: Option<u64>,
    pub max_retries: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionResult {
    pub task_id: String,
    pub agent_id: String,
    pub success: bool,
    pub output: Option<serde_json::Value>,
    pub error: Option<String>,
    pub execution_time_ms: u64,
    pub timestamp: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrchestratedResult {
    pub task_id: String,
    pub total_tasks: usize,
    pub completed_tasks: usize,
    pub results: Vec<ExecutionResult>,
    pub aggregated_output: serde_json::Value,
    pub total_execution_time_ms: u64,
    pub timestamp: i64,
}

// ========== 智能体池 ==========

pub struct AgentPool {
    agents: Arc<Mutex<HashMap<String, AgentType>>>,
    semaphore: Arc<Semaphore>,
}

impl AgentPool {
    pub fn new(max_concurrent: usize) -> Self {
        Self {
            agents: Arc::new(Mutex::new(HashMap::new())),
            semaphore: Arc::new(Semaphore::new(max_concurrent)),
        }
    }

    pub async fn register_agent(&self, agent: AgentType) -> Result<(), String> {
        let mut agents = self.agents.lock().await;
        
        if agents.contains_key(&agent.id) {
            return Err(format!("Agent {} already registered", agent.id));
        }
        
        agents.insert(agent.id.clone(), agent);
        Ok(())
    }

    pub async fn get_agent(&self, agent_id: &str) -> Option<AgentType> {
        let agents = self.agents.lock().await;
        agents.get(agent_id).cloned()
    }

    pub async fn execute_agent(
        &self,
        agent_type: &AgentType,
        input: serde_json::Value,
        timeout_ms: Option<u64>,
    ) -> ExecutionResult {
        let start_time = std::time::Instant::now();
        let agent_id = agent_type.id.clone();

        // 获取信号量许可
        let _permit = self.semaphore.acquire().await;

        // 模拟智能体执行
        let result = match self._execute_internal(agent_type, input, timeout_ms).await {
            Ok(output) => ExecutionResult {
                task_id: String::new(),
                agent_id: agent_id.clone(),
                success: true,
                output: Some(output),
                error: None,
                execution_time_ms: start_time.elapsed().as_millis() as u64,
                timestamp: Utc::now().timestamp_millis(),
            },
            Err(error) => ExecutionResult {
                task_id: String::new(),
                agent_id: agent_id.clone(),
                success: false,
                output: None,
                error: Some(error),
                execution_time_ms: start_time.elapsed().as_millis() as u64,
                timestamp: Utc::now().timestamp_millis(),
            },
        };

        // 释放信号量许可
        drop(_permit);

        result
    }

    async fn _execute_internal(
        &self,
        agent_type: &AgentType,
        input: serde_json::Value,
        timeout_ms: Option<u64>,
    ) -> Result<serde_json::Value, String> {
        // 模拟智能体执行（实际实现中会调用真实的智能体 API）
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        
        // 返回模拟结果
        Ok(serde_json::json!({
            "agent_name": agent_type.name,
            "result": "Task completed successfully",
            "data": input
        }))
    }
}

// ========== 编排器 ==========

pub struct Orchestrator {
    agent_pool: Arc<AgentPool>,
    max_parallel_tasks: usize,
}

impl Orchestrator {
    pub fn new(max_parallel_tasks: usize) -> Self {
        Self {
            agent_pool: Arc::new(AgentPool::new(max_parallel_tasks)),
            max_parallel_tasks,
        }
    }

    /// 并行执行
    pub async fn execute_parallel(
        &self,
        tasks: Vec<Task>,
        agent_types: Vec<AgentType>,
    ) -> OrchestratedResult {
        let start_time = std::time::Instant::now();
        
        log::info!("Starting parallel execution of {} tasks", tasks.len());

        // 并行执行所有任务
        let handles: Vec<_> = tasks
            .iter()
            .map(|task| {
                let agent_type = agent_types.get(0).cloned().unwrap_or_else(|| {
                    AgentType {
                        id: "default".to_string(),
                        name: "Default Agent".to_string(),
                        capabilities: vec![],
                        model_provider: "openai".to_string(),
                    }
                });
                
                let request = ExecutionRequest {
                    task_id: task.id.clone(),
                    agent_type: agent_type.clone(),
                    input: task.input_data.clone(),
                    config: ExecutionConfig {
                        parallel: true,
                        timeout_ms: task.timeout_ms,
                        max_retries: 3,
                    },
                };
                
                tokio::spawn(async move {
                    self.agent_pool.execute_agent(&request.agent_type, request.input, request.config.timeout_ms).await
                })
            })
            .collect();

        let results = join_all(handles).await;
        
        let total_execution_time = start_time.elapsed().as_millis() as u64;
        let completed_tasks = results.len();
        
        log::info!("Parallel execution completed: {} tasks in {} ms", completed_tasks, total_execution_time);

        OrchestratedResult {
            task_id: "parallel_batch".to_string(),
            total_tasks: tasks.len(),
            completed_tasks,
            results,
            aggregated_output: self._aggregate_results(&results),
            total_execution_time_ms: total_execution_time,
            timestamp: Utc::now().timestamp_millis(),
        }
    }

    /// 串行执行
    pub async fn execute_sequential(
        &self,
        tasks: Vec<Task>,
        agent_types: Vec<AgentType>,
    ) -> OrchestratedResult {
        let start_time = std::time::Instant::now();
        
        log::info!("Starting sequential execution of {} tasks", tasks.len());

        let mut results = Vec::new();
        let mut previous_output = None;

        for (i, task) in tasks.iter().enumerate() {
            log::info!("Executing task {}/{}: {}", i + 1, tasks.len(), task.name);
            
            let agent_type = agent_types.get(i % agent_types.len()).cloned().unwrap_or_else(|| {
                AgentType {
                    id: "default".to_string(),
                    name: "Default Agent".to_string(),
                    capabilities: vec![],
                    model_provider: "openai".to_string(),
                }
            });

            let input = if let Some(prev_output) = previous_output {
                serde_json::json!({
                    "current_task": task.input_data,
                    "previous_output": prev_output
                })
            } else {
                task.input_data.clone()
            };

            let result = self.agent_pool.execute_agent(&agent_type, input, task.timeout_ms).await;
            previous_output = result.output.clone();
            results.push(result);
        }

        let total_execution_time = start_time.elapsed().as_millis() as u64;
        let completed_tasks = results.len();
        
        log::info!("Sequential execution completed: {} tasks in {} ms", completed_tasks, total_execution_time);

        OrchestratedResult {
            task_id: "sequential_batch".to_string(),
            total_tasks: tasks.len(),
            completed_tasks,
            results,
            aggregated_output: self._aggregate_results(&results),
            total_execution_time_ms: total_execution_time,
            timestamp: Utc::now().timestamp_millis(),
        }
    }

    /// 任务分解
    pub fn decompose_task(&self, task: Task) -> Vec<Task> {
        log::info!("Decomposing task: {}", task.name);

        // 简单的任务分解逻辑
        let mut subtasks = Vec::new();

        // 根据任务复杂度分解
        if task.description.contains("复杂的") || task.description.contains("multi-step") {
            // 分解为多个子任务
            for i in 0..3 {
                subtasks.push(Task {
                    id: format!("{}-sub-{}", task.id, i),
                    name: format!("{} - Step {}", task.name, i + 1),
                    description: format!("Step {} of {}", i + 1, task.name),
                    input_data: task.input_data.clone(),
                    dependencies: if i > 0 {
                        vec![format!("{}-sub-{}", task.id, i - 1)]
                    } else {
                        vec![]
                    },
                    timeout_ms: Some(30000),
                });
            }
        } else {
            // 简单任务不需要分解
            subtasks.push(task);
        }

        subtasks
    }

    /// 结果汇总
    fn _aggregate_results(&self, results: &[ExecutionResult]) -> serde_json::Value {
        let successful_results: Vec<_> = results
            .iter()
            .filter(|r| r.success)
            .collect();

        let total_tasks = results.len();
        let successful_count = successful_results.len();
        let success_rate = if total_tasks > 0 {
            (successful_count as f64 / total_tasks as f64) * 100.0
        } else {
            0.0
        };

        serde_json::json!({
            "total_tasks": total_tasks,
            "successful_tasks": successful_count,
            "failed_tasks": total_tasks - successful_count,
            "success_rate": success_rate,
            "results": successful_results
        })
    }
}

// ========== 内置智能体类型 ==========

pub fn get_builtin_agents() -> Vec<AgentType> {
    vec![
        AgentType {
            id: "code_reviewer".to_string(),
            name: "代码审查员".to_string(),
            capabilities: vec![
                "code_scanning".to_string(),
                "lint_check".to_string(),
                "type_check".to_string(),
                "security_check".to_string(),
            ],
            model_provider: "openai".to_string(),
        },
        AgentType {
            id: "test_engineer".to_string(),
            name: "测试工程师".to_string(),
            capabilities: vec![
                "unit_testing".to_string(),
                "integration_testing".to_string(),
                "test_coverage".to_string(),
            ],
            model_provider: "openai".to_string(),
        },
        AgentType {
            id: "data_analyst".to_string(),
            name: "数据分析师".to_string(),
            capabilities: vec![
                "data_processing".to_string(),
                "statistical_analysis".to_string(),
                "report_generation".to_string(),
            ],
            model_provider: "claude".to_string(),
        },
        AgentType {
            id: "documentation_writer".to_string(),
            name: "文档编写员".to_string(),
            capabilities: vec![
                "doc_generation".to_string(),
                "api_docs".to_string(),
                "user_guide".to_string(),
            ],
            model_provider: "openai".to_string(),
        },
    ]
}
