# CCDV-P official blueprint (Exam Guide v1.0, Nov 2026)

5. Exam Content Outline (Blueprint)
The exam blueprint defines the content domains and skills measured and the approximate weight of
each domain on the exam. Weights reflect the relative importance of each domain to competent
performance as determined through the job task analysis and content validation surveys. The
percentages indicate the approximate proportion of scored items drawn from each domain.

Domain Content Domain Weight
1 Advanced Agent Architecture and Orchestration 17%
2 Production Integration, Reliability, and Knowledge Grounding 20%
3 Observability and Production Monitoring 12%
4 Advanced Debugging and Incident Response 10%
5 Evaluation Engineering and Quality Assurance 12%
6 Cost and Latency Optimization at Scale 8%
7 Runtime Guardrails and Production Security 11%
8 Agent Fleet Operations for Software Delivery 10%
Total 100%
Detailed objectives by domain
Each domain below lists the skills against which exam items are written. Skill descriptions summarize
the knowledge and competencies measured.
Domain 1 Advanced Agent Architecture and Orchestration 17%
Multi-Agent Orchestration
Evaluating orchestration patterns for production multi-agent designs and inter-agent failures,
including supervisor/worker hierarchies, parallel subagent dispatch, delegation and context-isolation
boundaries, inter-agent communication, and human-in-the-loop and approval flows.
Durable Execution and State Management
Applying session persistence, checkpointing, resumability, and memory architecture patterns to long-
running agents that must survive interruption, restart, and model version change.
Architecture Selection at Scale
Evaluating production cost, reliability, and quality data to decide whether to evolve a running system
between workflow and agentic patterns, and selecting the agent harness, framework, and reusable-
pattern standards a team should adopt.

Context and Memory Architecture
Evaluating context-policy options for long-running agents approaching context limits or cost ceilings,
including context compaction and editing, persistent memory, cache-safe instruction changes mid-
conversation, and tool-use techniques that keep large tool catalogs out of the context window.
Domain 2 Production Integration, Reliability, and Knowledge Grounding 20%
Reliability Engineering for Claude Services
Evaluating and applying resilience patterns for production Claude integrations, including retry and
backoff design, circuit breakers, graceful degradation, and cross-model, cross-region, and cross-
platform fallbacks that distinguish rate limits from safety refusals from context-window stops while
respecting per-platform feature parity.
Scale and Throughput Management
Analyzing rate-limit strategy, queueing and backpressure, batch pipeline design, multi-tenant quota
and isolation, and capacity planning for high-volume Claude workloads, and identifying whether rate
limits, token throughput, or batch economics is the binding constraint.
Production MCP and Change Management
Applying production MCP operation and change-management practice to MCP server deployments,
model version migrations, and prompt updates, including remote MCP deployment and
authentication, tool and schema versioning, migration testing against breaking behavior changes,
platform-specific configuration parity and gateway/routing architectures, prompt versioning, and
progressive rollout with rollback.
Retrieval and Knowledge Grounding at Scale
Evaluating retrieval architecture for knowledge-grounded production applications, including agentic
search versus RAG tradeoffs, chunking and embedding strategy, hybrid search, and reranking, and
designing grounding practices such as source citation, uncertainty declaration, and confidence
signals, and diagnosing retrieval-quality failures by stage.

Domain 3 Observability and Production Monitoring 12%
Telemetry and Instrumentation
Applying instrumentation practice to production Claude systems under debuggability and privacy
requirements, including distributed traces for agent loops and tool calls, token and cost metrics,
cache-performance diagnostics, grounding and reasoning traceability, structured log events, and
content-capture configuration under privacy constraints such as zero-data-retention.
Production Monitoring and Alerting
Analyzing production signals from LLM-backed services to define service level indicators SLIs) and
SLOs, design alerting and dashboards (including token and cost telemetry), and detect quality drift,
behavioral regressions, and anomalous usage, including drift after model updates.
Trace Analysis at Scale
Analyzing high-volume trace data using sampling strategies, aggregation, and failure-cohort analysis
to surface and quantify systemic issues that are not visible in individual traces.
Domain 4 Advanced Debugging and Incident Response 10%
Complex Failure Diagnosis
Analyzing evidence from complex production failures, including multi-turn, multi-agent, and non-
deterministic failures, to isolate the problem origin among model output, agent harness, tools, and
data, including model refusals as a failure class and retrieval-grounding failures.
Incident Response and Learning Loops
Evaluating incident-response options during an LLM-system outage or quality regression, including
triage, mitigation, rollback, and communication, and converting the incident into regression
evaluations, monitoring coverage, and postmortem findings.
Domain 5 Evaluation Engineering and Quality Assurance 12%
Evaluation System Design
Evaluating and designing offline evaluation systems for Claude applications, including golden sets,
regression suites, behavioral checks, CI/CD evaluation gates, retrieval precision and groundedness
metrics, and release criteria for prompt, model, and agent changes, and maintaining suite validity
over time against contamination, saturation, and coverage gaps.

LLM-as-Judge Engineering
Analyzing LLM-as-judge evaluator quality against human-labeled data, including calibration, rubric
design, bias and position effects, inter-rater reliability, and judge drift across model versions.
Online Quality Measurement
Analyzing quality on live production traffic using online evaluation techniques, including live-traffic
sampling, A/B testing, feedback loops, and metric selection matched to task type (extraction,
generation, agentic, retrieval-grounded).
Domain 6 Cost and Latency Optimization at Scale 8%
Cost Architecture at Scale
Evaluating fleet-level optimization strategies using usage and cost data, including cost modeling and
forecasting, model routing and cascades across the Claude model family, caching strategy and
cache diagnostics, batch-versus-realtime economics, and per-tenant budget enforcement.
Latency Engineering
Analyzing the latency profile of a Claude application against a latency target, distinguishing time-to-
first-token from total latency, and applying streaming, parallel tool execution, cache checkpointing,
and effort-level tuning.
Domain 7 Runtime Guardrails and Production Security 11%
Runtime Guardrail Systems
Evaluating layered guardrail architectures against a production agentʼs risk profile, including
input/output filtering, PII redactors, hook-based policy enforcement, destructive-action prevention,
sandboxing that grants tool and web access without exposing production systems, approval gates,
refusal handling and safety fallbacks, deterministic enforcement for irreversible actions, and false-
positive/false-negative tuning.
Threat Defense and Adversarial Testing for Agentic Systems
Analyzing the attack surface of tool-using agents that process untrusted content, including prompt
injection, tool and memory poisoning, data exfiltration paths, unsafe-autonomy conditions, and the
high-risk combination of private data access, untrusted input, and external communication, and
applying defense-in-depth mitigations, red-team exercise design, and secure MCP configuration,
drawing on the OWASP Top 10 for LLM Applications and the NIST AI Risk Management Framework
and its Generative AI Profile.

Identity, Secrets, and Audit at Scale
Applying enterprise identity and secrets practice to production Claude deployments, including agent
identity, workload identity federation replacing static API keys, credential and secrets management,
least-privilege tool permissioning, and audit logging of security-relevant agent actions.
Domain 8 Agent Fleet Operations for Software Delivery 10%
Parallel Agent Orchestration for Engineering Work
Evaluating parallel fan-out patterns for large engineering tasks, including parallel agents on isolated
worktrees, task decomposition, and merge and conflict strategy, and diagnosing fleet-level failure
modes from fleet telemetry.
Verification and AI Code Review Operations
Analyzing verification operations in delivery pipelines where generation outpaces review, including AI
code review introduced in shadow mode, calibration against human review before merge gating, and
human oversight design.
Unattended and Event-Driven Agent Operations
Applying unattended-operation patterns to goal- or schedule-driven engineering tasks, including
agents running toward goals, on schedules, or as event-driven responders such as CI/CD incident
first response, with checkpointing, notification, and escalation design.
Organization-Wide Coding Agent Configuration
Applying enterprise configuration for organizations adopting coding agents, including managed
settings and policies, MCP allowlists, telemetry, gateway routing, and governance with a quality and
safety bar for sharing prompts, Skills, and MCP servers across teams.