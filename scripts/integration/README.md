# Integration Scripts

OpenClaw system integration and multi-user management scripts.

## Scripts

### System Integration
- **echo2_swarm.py**: Echo-2 swarm orchestration for multi-agent coordination
- **multi_user_permission.py**: Multi-user permission management system
- **openclaw_system.py**: Core OpenClaw system integration
- **openclaw-with-openviking.py**: OpenClaw + OpenViking integration
- **openclaw_memory_integration.py**: Memory service integration with OpenClaw
- **openviking-memory-plugin.py**: OpenViking memory plugin implementation

## Usage

### Echo-2 Swarm
```bash
python scripts/integration/echo2_swarm.py --config swarm-config.json
```

### Multi-User Permission
```bash
python scripts/integration/multi_user_permission.py --user admin --action grant
```

### OpenClaw System
```bash
python scripts/integration/openclaw_system.py --init
```

## Features

- Multi-agent orchestration (Echo-2 swarm)
- User permission management (RBAC)
- Memory service integration
- OpenViking compatibility
- Session management

## Requirements

- Python 3.11+
- OpenClaw SDK
- FastAPI
- SQLAlchemy

## Notes

- Multi-user permission system is production-ready (v1.0.0)
- Memory integration supports long-term storage
- OpenViking integration for advanced capabilities
