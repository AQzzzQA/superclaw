// Echo Skills - Echo 智能体自动化能力
// 自动修复、代码生成、文档生成

use std::path::Path;
use std::process::Command;
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use std::sync::Arc;
use std::collections::HashMap;

// ========== 类型定义 ==========

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CodeIssue {
    pub file_path: String,
    pub line_number: usize,
    pub column: usize,
    pub severity: String,
    pub message: String,
    pub code: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ScanResult {
    pub success: bool,
    pub issues: Vec<CodeIssue>,
    pub total_issues: usize,
    pub scan_duration_ms: u64,
    pub timestamp: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FixResult {
    pub success: bool,
    pub file_path: String,
    pub fixes_applied: usize,
    pub error: Option<String>,
    pub timestamp: i64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenerationResult {
    pub success: bool,
    pub content: String,
    pub file_path: Option<String>,
    pub error: Option<String>,
    pub timestamp: i64,
}

// ========== 代码扫描器 ==========

pub struct CodeScanner {
    workspace_path: Arc<String>,
}

impl CodeScanner {
    pub fn new(workspace_path: String) -> Self {
        Self {
            workspace_path: Arc::new(workspace_path),
        }
    }

    pub async fn scan(&self) -> anyhow::Result<ScanResult> {
        let start = std::time::Instant::now();
        let mut issues = Vec::new();

        // 扫描 Python 文件
        let py_files = self.find_python_files().await?;
        
        for file_path in py_files {
            // 运行 flake8
            if let Ok(result) = self.run_flake8(&file_path).await {
                issues.extend(result);
            }

            // 运行 bandit（安全扫描）
            if let Ok(result) = self.run_bandit(&file_path).await {
                issues.extend(result);
            }
        }

        let scan_duration = start.elapsed().as_millis() as u64;

        Ok(ScanResult {
            success: true,
            issues: issues.clone(),
            total_issues: issues.len(),
            scan_duration_ms: scan_duration,
            timestamp: chrono::Utc::now().timestamp_millis(),
        })
    }

    async fn find_python_files(&self) -> anyhow::Result<Vec<String>> {
        let mut py_files = Vec::new();
        let workspace = Path::new(&self.workspace_path);

        if let Ok(entries) = std::fs::read_dir(workspace) {
            for entry in entries.flatten() {
                if let Ok(path) = entry.path().canonicalize() {
                    if path.is_dir() {
                        continue;
                    }

                    if let Some(extension) = path.extension() {
                        if extension == "py" {
                            if let Some(path_str) = path.to_str() {
                                py_files.push(path_str.to_string());
                            }
                        }
                    }
                }
            }
        }

        Ok(py_files)
    }

    async fn run_flake8(&self, file_path: &str) -> anyhow::Result<Vec<CodeIssue>> {
        let output = Command::new("flake8")
            .arg(file_path)
            .output()?;

        if output.status.success() {
            let issues: Vec<CodeIssue> = std::str::from_utf8(&output.stdout)?
                .lines()
                .filter_map(|line| {
                    // 解析 flake8 输出
                    let parts: Vec<&str> = line.split(':').collect();
                    if parts.len() >= 3 {
                        Some(CodeIssue {
                            file_path: file_path.to_string(),
                            line_number: parts.get(1).and_then(|s| s.parse().ok()).unwrap_or(0),
                            column: parts.get(2).and_then(|s| s.parse().ok()).unwrap_or(0),
                            severity: "warning".to_string(),
                            message: parts.get(3).unwrap_or(&"").to_string(),
                            code: parts.get(4).unwrap_or(&"").to_string(),
                        })
                    } else {
                        None
                    }
                })
                .collect();

            Ok(issues)
        } else {
            Ok(Vec::new())
        }
    }

    async fn run_bandit(&self, file_path: &str) -> anyhow::Result<Vec<CodeIssue>> {
        let output = Command::new("bandit")
            .args(["-f", "json", file_path])
            .output()?;

        if output.status.success() {
            // 解析 bandit JSON 输出
            if let Ok(json) = serde_json::from_str::<serde_json::Value>(&std::str::from_utf8(&output.stdout)?) {
                if let Some(results) = json["results"].as_array() {
                    let issues: Vec<CodeIssue> = results
                        .iter()
                        .filter_map(|result| {
                            Some(CodeIssue {
                                file_path: result["filename"].as_str().unwrap_or(file_path).to_string(),
                                line_number: result["line_number"].as_u64().unwrap_or(0) as usize,
                                column: result["column_number"].as_u64().unwrap_or(0) as usize,
                                severity: result["issue_severity"].as_str().unwrap_or("medium").to_string(),
                                message: result["issue_text"].as_str().unwrap_or("").to_string(),
                                code: result["test_id"].as_str().unwrap_or("").to_string(),
                            })
                        })
                        .collect();

                    return Ok(issues);
                }
            }
        }

        Ok(Vec::new())
    }
}

// ========== 自动修复器 ==========

pub struct AutoFixer {
    workspace_path: Arc<String>,
}

impl AutoFixer {
    pub fn new(workspace_path: String) -> Self {
        Self {
            workspace_path: Arc::new(workspace_path),
        }
    }

    pub async fn fix_issues(&self, issues: Vec<CodeIssue>) -> Vec<FixResult> {
        let mut results = Vec::new();
        let mut fixes_per_file: HashMap<String, Vec<CodeIssue>> = HashMap::new();

        // 按文件分组
        for issue in issues {
            fixes_per_file
                .entry(issue.file_path.clone())
                .or_insert_with(Vec::new)
                .push(issue);
        }

        // 逐文件修复
        for (file_path, file_issues) in fixes_per_file {
            if let Some(result) = self.fix_file(&file_path, file_issues).await {
                results.push(result);
            }
        }

        results
    }

    async fn fix_file(&self, file_path: &str, issues: Vec<CodeIssue>) -> Option<FixResult> {
        let mut fixes_applied = 0;

        // 运行 black 自动格式化
        if Command::new("black")
            .arg(file_path)
            .output()
            .map(|o| o.status.success())
            .unwrap_or(false)
        {
            fixes_applied += issues.len();
        }

        Some(FixResult {
            success: true,
            file_path: file_path.to_string(),
            fixes_applied,
            error: None,
            timestamp: chrono::Utc::now().timestamp_millis(),
        })
    }
}

// ========== 智能生成器 ==========

pub struct SmartGenerator {
    workspace_path: Arc<String>,
}

impl SmartGenerator {
    pub fn new(workspace_path: String) -> Self {
        Self {
            workspace_path: Arc::new(workspace_path),
        }
    }

    pub async fn generate_changelog(&self, changes: Vec<String>) -> GenerationResult {
        let changelog_content = format!(
r"# SuperClaw Changelog

## 版本历史

### v1.0.0 - {date}
- 初始版本发布
- 双网关实现（WebSocket + HTTP）
- Echo Skills 基础框架
{changes}

---

_自动生成于 {timestamp}_
",
            date = chrono::Utc::now().format("%Y-%m-%d"),
            changes = changes
                .iter()
                .map(|c| format!("- {}", c))
                .collect::<Vec<_>>()
                .join("\n"),
            timestamp = chrono::Utc::now().format("%Y-%m-%d %H:%M:%S"),
        );

        let file_path = format!("{}/CHANGELOG.md", self.workspace_path);
        
        if let Err(e) = tokio::fs::write(&file_path, changelog_content).await {
            return GenerationResult {
                success: false,
                content: String::new(),
                file_path: None,
                error: Some(format!("写入 CHANGELOG.md 失败: {}", e)),
                timestamp: chrono::Utc::now().timestamp_millis(),
            };
        }

        GenerationResult {
            success: true,
            content: changelog_content,
            file_path: Some(file_path),
            error: None,
            timestamp: chrono::Utc::now().timestamp_millis(),
        }
    }

    pub async fn generate_license(&self) -> GenerationResult {
        let license_content = format!(
r"MIT License

Copyright (c) {year} SuperClaw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
",
            year = chrono::Utc::now().year()
        );

        let file_path = format!("{}/LICENSE", self.workspace_path);
        
        if let Err(e) = tokio::fs::write(&file_path, license_content).await {
            return GenerationResult {
                success: false,
                content: String::new(),
                file_path: None,
                error: Some(format!("写入 LICENSE 失败: {}", e)),
                timestamp: chrono::Utc::now().timestamp_millis(),
            };
        }

        GenerationResult {
            success: true,
            content: license_content,
            file_path: Some(file_path),
            error: None,
            timestamp: chrono::Utc::now().timestamp_millis(),
        }
    }
}
