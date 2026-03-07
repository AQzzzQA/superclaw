// SuperClaw - Super Claw AI Platform
// 主入口和路由配置

#[macro_use] extern crate rocket;

use rocket::{State, Launch, routes, config::Config};
use rocket_cors::{Cors, CorsOptions};
use std::sync::Arc;
use tokio::sync::Mutex;

// 导入模块
mod gateway;
mod skills;
mod api;
mod agents;

// 导入 Gateway 类型
use gateway::{ConnectionManager, LemClawProxy, OpenClawProxy};

// ========== 配置 ==========

#[derive(Debug, Clone)]
pub struct AppConfig {
    pub lemlaw_url: String,
    pub lemlaw_token: String,
    pub openclaw_url: String,
    pub openclaw_token: String,
    pub bind_address: String,
    pub port: u16,
}

impl AppConfig {
    pub fn from_env() -> Self {
        use dotenv::dotenv;

        dotenv().ok();

        Self {
            lemlaw_url: std::env::var("LEMLAW_GATEWAY_URL")
                .unwrap_or_else(|_| "http://localhost:8089".to_string()),
            lemlaw_token: std::env::var("LEMLAW_AUTH_TOKEN")
                .unwrap_or_else(|_| "default_token".to_string()),
            openclaw_url: std::env::var("OPENCLAW_GATEWAY_URL")
                .unwrap_or_else(|_| "http://localhost:18789".to_string()),
            openclaw_token: std::env::var("OPENCLAW_GATEWAY_TOKEN")
                .unwrap_or_else(|_| "default_token".to_string()),
            bind_address: std::env::var("BIND_ADDRESS")
                .unwrap_or_else(|_| "0.0.0.0".to_string()),
            port: std::env::var("PORT")
                .unwrap_or_else(|_| "3000".to_string())
                .parse()
                .unwrap_or(3000),
        }
    }
}

// 导入 Orchestrator 状态管理
use agents::mod::{OrchestratorState};

// ========== 初始化函数 ==========

fn init_logger() {
    env_logger::Builder::from_default_env()
        .filter_level(log::LevelFilter::Info)
        .init();
}

// ========== 主函数 ==========

#[rocket::main]
async fn main() -> Launch<rocket::Rocket<rocket::Ignite>> {
    // 初始化日志
    init_logger();

    // 加载配置
    let config = AppConfig::from_env();

    log::info!("Starting SuperClaw...");
    log::info!("Config: {:?}", config);

    // 初始化连接管理器
    let connection_manager = Arc::new(ConnectionManager::new());

    // 初始化 LemClaw 代理
    let lemlaw_proxy = Arc::new(LemClawProxy::new(
        config.lemclaw_url.clone(),
        config.lemclaw_token.clone(),
    ));

    // 初始化 OpenClaw 代理
    let openclaw_proxy = Arc::new(OpenClawProxy::new(
        config.openclaw_url.clone(),
        config.openclaw_token.clone(),
    ));

    // 初始化 Orchestrator
    let orchestrator = Arc::new(Orchestrator::new(5));

    // 配置 CORS
    let cors = CorsOptions::default()
        .allowed_origins(
            rocket_cors::AllowedOrigins::all()
        )
        .allowed_methods(
            vec![Method::Get, Method::Post, Method::Options]
                .into_iter()
                .map(From::from)
                .collect(),
        )
        .allow_credentials(true)
        .to_cors()
        .expect("CORS configuration error");

    // 配置 Rocket
    let rocket_config = Config {
        address: config.bind_address.parse().unwrap(),
        port: config.port,
        ..Config::default()
    };

    // 构建并启动 Rocket
    rocket::custom(rocket_config)
        .manage(connection_manager)
        .manage(lemlaw_proxy)
        .manage(openclaw_proxy)
        .manage(orchestrator)
        .attach(cors)
        .mount(
            "/",
            routes![
                gateway::http::health_check,
                gateway::http::agent_message,
                gateway::http::gateway_status,
                gateway::websocket::websocket_handler,
                gateway::websocket::websocket_api_message,
                gateway::websocket::list_connections,
                api::skills::skills_health,
                api::skills::scan_workspace,
                api::skills::fix_issues,
                api::skills::generate_changelog,
                api::skills::generate_license,
                agents::list_agents,
                agents::execute_parallel,
                agents::execute_sequential,
                agents::decompose_task,
                agents::register_agent,
                agents::get_agent_status,
            ],
        )
        .launch()
}
