# AutoDev-Agentic-Platform

**Collaborative Agentic Platform for Automated Full-Stack Development**

*Techfest 2025-26 AutoDev Hackathon | Team ID: Auto-250358*

## Overview

Autodev is a revolutionary multi-agent system that transforms Azure DevOps user stories into production-ready full-stack applications. By orchestrating specialized AI agents that work collaboratively, AutoDev drastically reduces development time while maintaining code quality and security standards.

### The Problem

Traditional software development faces critical bottlenecks:
- Manual coding and repetitive tasks
- Testing delays and integration complexities
- Difficulty maintaining code quality across teams
- Slow onboarding for legacy codebases

### Our Solution

Rather than relying on a monolithic "god agent", AutoDev uses **agent specialization and collaboration**—mimicking how human development teams divide work, communicate, and integrate their outputs.

## Architecture Overview

### System Components

Autodev comprises 8 specialized components:

#### 1. **ADO Connector & Parser Agent**
- Connects to Azure DevOps via REST API or accepts exported JSON/CSV files
- Uses NLP with LLM-powered analysis to extract requirements
- Outputs structured task objects with priority, type, and dependencies

#### 2. **Orchestrator/Coordinator Agent**
- Central brain managing workflow and creating build pipeline
- Assigns tasks to specialized agents based on capability matching
- Manages dependencies and implements parallel execution
- Uses state machine pattern for tracking progress

#### 3. **Code Generation Agents** (Layer-Specific)
- **Frontend Agent**: Generates React components with TypeScript, handles UI/UX
- **Backend Agent**: Creates Node.js/Express APIs or Python/Flask endpoints
- **Database Agent**: Designs schemas, creates migrations, generates ORM models
- Each uses LLM (GPT-4/Claude) with specialized prompts for quality code

#### 4. **Testing & Validation Agent**
- Automatically generates unit tests (Jest/Pytest)
- Creates integration tests for API endpoints
- Executes tests in isolated Docker environments
- Produces pass/fail reports with coverage metrics

#### 5. **Legacy Code Analyzer Agent**
- Scans existing codebases using AST (Abstract Syntax Tree) parsing
- Identifies architecture patterns, dependencies, and entry points
- Suggests integration strategies for new features
- Detects potential conflicts before code generation

#### 6. **Prompt Refinement Engine**
- Meta-improvement agent analyzing and refining prompts
- Improves quality and accuracy of generated code
- Feedback loop for continuous optimization

#### 7. **Monitoring & Communication Layer**
- Message queue system (Redis/RabbitMQ) for agent coordination
- Shared state management (PostgreSQL) for persistent state
- Event-driven architecture enabling async parallel processing

#### 8. **Monitoring Dashboard UI**
- Real-time visualization of agent activities
- Input interface for ADO project details
- Display of generated outputs and execution logs

## Data Flow: From User Story to Production Code

```
ADO User Story
    ↓
[ADO Parser Agent] → Extracts requirements, dependencies, acceptance criteria
    ↓
[Coordinator Agent] → Creates task pipeline, assigns priorities
    ↓
┌─────────────────────────────────────────┐
│         Parallel Agent Execution        │
├─────────────────────────────────────────┤
│ Frontend Agent │ Backend Agent │ DB Agent │
│ Database Agent │ Testing Agent │ Legacy   │
└─────────────────────────────────────────┘
    ↓
[Prompt Refinement Engine] → Quality feedback loop
    ↓
[Testing Agent] → Generates & executes tests
    ↓
Working Full-Stack Application ✓
```

## Key Features

### ✅ Parallel Execution
Frontend and backend agents work simultaneously, accelerating development

### ✅ Feedback Loops
Prompt refinement and test validation improve code quality iteratively

### ✅ Centralized Monitoring
Dashboard provides real-time visibility into agent collaboration

### ✅ State Management
All agents communicate through a message bus with persistent state tracking

### ✅ Automated Testing
Comprehensive test generation and execution for all generated code

### ✅ Legacy Integration
Safely add features to existing codebases without breaking functionality

## Technical Stack

### Orchestration Layer
- **Framework**: LangGraph / AutoGen
- **Language**: Python 3.11

### AI/ML Models
- **Primary LLM**: OpenAI GPT-4 Turbo (code generation & analysis)
- **Alternative**: Anthropic Claude 3.5 Sonnet (complex reasoning)
- **Fallback**: Open-source Llama 3.1 70B (cost optimization)
- **Embeddings**: OpenAI text-embedding-3-large (semantic search)

### Code Generation Target Stack
- **Frontend**: React 18 + TypeScript + TailwindCSS
- **Backend**: Node.js/Express.js OR Python/Flask
- **Database**: PostgreSQL + Prisma (Node.js) OR SQLAlchemy (Python)
- **ORM**: Prisma / SQLAlchemy

### Infrastructure
- **Message Queue**: Redis (agent communication)
- **State Management**: PostgreSQL (persistent agent state)
- **Testing**: Jest (frontend/backend), Pytest (Python), Playwright (E2E)
- **Code Execution**: Docker (isolated test environments)
- **Monitoring Dashboard**: React + WebSocket + Socket.io + Recharts

### Security
- **API Key Management**: HashiCorp Vault or environment variables
- **ADO Authentication**: OAuth 2.0 with token refresh
- **Code Sandboxing**: Docker resource limits
- **Static Analysis**: Snyk, SonarQube

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend/backend stacks)
- Docker & Docker Compose
- Git
- OpenAI API key (or alternative LLM provider)
- PostgreSQL 14+
- Redis 7+

### Installation

```bash
# Clone repository
git clone https://github.com/parth2152012/AutoDev-Agentic-Platform.git
cd AutoDev-Agentic-Platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration

# Start services with Docker Compose
docker-compose up -d

# Run migrations
python scripts/migrate.py

# Start the platform
python main.py
```

## Project Structure

```
Autodev-Agentic-Platform/
├── src/
│   ├── agents/
│   │   ├── ado_parser.py
│   │   ├── coordinator.py
│   │   ├── frontend_agent.py
│   │   ├── backend_agent.py
│   │   ├── database_agent.py
│   │   ├── testing_agent.py
│   │   ├── legacy_analyzer.py
│   │   └── prompt_refiner.py
│   ├── orchestration/
│   │   ├── workflow.py
│   │   ├── state_manager.py
│   │   └── event_bus.py
│   ├── infrastructure/
│   │   ├── redis_client.py
│   │   ├── database.py
│   │   └── docker_executor.py
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── routes.py
│   │   └── components/
│   └── utils/
│       ├── llm_client.py
│       ├── validators.py
│       └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Data Privacy & Security

### ADO Data Handling
- **Encryption in Transit**: All ADO API calls use TLS 1.3
- **Token Storage**: OAuth tokens encrypted in vault, never in code/logs
- **Data Minimization**: Only parse necessary fields from user stories
- **Temporary Processing**: ADO data cached only during active session, deleted after

### API Key Security
- **Environment Variables**: All LLM API keys in .env files (never committed)
- **Vault Integration**: Production uses HashiCorp Vault
- **Rotation Policy**: Automated key rotation every 90 days
- **Access Control**: Role-based access to sensitive components

### Generated Code Security
- **Static Analysis**: Automated security scanning (Snyk, SonarQube)
- **Dependency Auditing**: Check for vulnerable packages before generation
- **Secret Detection**: Prevent accidental hardcoding of credentials
- **Compliance**: No user story data sent to external services without consent

## Key Challenges & Solutions

### Challenge 1: Maintaining Code Quality Across Agents
**Strategy:**
- Shared code style guide (ESLint/Prettier configs)
- Coordinator performs sanity checks before merging
- Template library for pre-validated code patterns
- Testing feedback triggers re-generation if thresholds not met

### Challenge 2: Agent Coordination & Dependency Management
**Strategy:**
- Dependency graph parser extracts explicit dependencies
- Topological sort for execution order
- Smart parallelism for independent tasks
- Timeout fallback and state checkpointing

### Challenge 3: Legacy Code Integration Without Breaking
**Strategy:**
- Comprehensive AST analysis before modifications
- Non-invasive patterns (extend new modules vs. modifying core)
- Automated regression testing
- Incremental feature flags for safe rollout

## Success Metrics & Evaluation Criteria

1. **Functional Completeness**: % of features working correctly without manual fixes
2. **Full-Stack Scope**: Generate code for frontend, backend, and database layers
3. **Automated Testing**: Generate and execute validation tests with clear reports
4. **Legacy Code Understanding**: Analyze existing codebases and extract architecture
5. **Multi-Agent Parallelism**: Demonstrate specialized agents working in parallel
6. **Code Quality**: Modularity, cleanliness, and adherence to design principles
7. **UI/Monitoring**: Dashboard clarity and utility for monitoring agent activity
8. **Deliverables Completeness**: Working prototype, source code, demo, and report

## Demonstration Features

### Round 2 Deliverables
1. **ADO Requirement Ingestion** ✓
2. **Autonomous Agent Orchestration** ✓
3. **End-to-End Full-Stack Generation** ✓
4. **Automated Test Generation & Execution** ✓
5. **Parallel Processing for Speed** ✓
6. **Legacy Code Analysis & Integration** ✓
7. **Transparent Monitoring Dashboard** ✓

## Contributing

This is a hackathon project. For contributions or questions:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## License

MIT License - See LICENSE file for details

## Authors

**Team Auto-250358**
- **Lead**: Parth Bavale (parthbb21@gmail.com)
- Sponsor: Marsh McLennan
- Event: Techfest 2025-26 AutoDev Hackathon, IIT Bombay

## Acknowledgments

- Azure DevOps API team
- OpenAI / Anthropic for LLM APIs
- LangGraph/LangChain community
- IIT Bombay Techfest organizers

---

**Status**: 🚀 Development in Progress (Round 2 Submission)

**Last Updated**: December 1, 2025
