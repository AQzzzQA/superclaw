# Utility Scripts

Testing, demos, and utility scripts for development and debugging.

## Scripts

### OpenClaw Utilities
- **simple_openclaw.py**: Simplified OpenClaw API wrapper
- **test_integration.py**: Integration tests for various components
- **test-memory-service.py**: Memory service unit tests
- **manage-memory-service.sh**: Memory service management script
- **start-memory-service.py**: Memory service startup script

### Demo Scripts
- **web_search_demo.py**: Web search API demonstration
- **web_search_test.py**: Web search testing script

## Usage

### Simple OpenClaw
```bash
python scripts/utils/simple_openclaw.py --help
```

### Integration Tests
```bash
python scripts/utils/test_integration.py --verbose
```

### Memory Service
```bash
# Start memory service
python scripts/utils/start-memory-service.py

# Test memory service
python scripts/utils/test-memory-service.py

# Manage memory service
bash scripts/utils/manage-memory-service.sh status
```

### Web Search Demo
```bash
python scripts/utils/web_search_demo.py --query "AI agents"
```

## Features

- Simplified API wrappers
- Comprehensive test coverage
- Memory service management
- Demo examples
- Debugging utilities

## Requirements

- Python 3.11+
- pytest (for testing)
- requests
- OpenClaw SDK

## Notes

- All test scripts use pytest framework
- Memory service requires proper configuration
- Demo scripts are for educational purposes
