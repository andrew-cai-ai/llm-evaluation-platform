# LLM Evaluation & Reliability Platform

A lightweight platform for evaluating LLM behavior, reliability, and performance across model providers.

## Problem

LLM applications introduce system-level challenges that traditional backend services do not fully cover:

- non-deterministic outputs
- model behavior changes across prompt versions
- latency and token-cost tradeoffs
- failures caused by timeouts, retries, and provider errors
- lack of structured evaluation history

This project explores how production engineering ideas such as observability, retries, structured logging, and regression detection can be applied to LLM workflows.

## Current Features

- FastAPI service with `/evaluate` endpoint
- Request/response schema validation
- Latency measurement
- Structured JSON response
- Local interactive API docs via Swagger UI

## Planned Features

- OpenAI and Anthropic model adapters
- Token usage and cost tracking
- Retry and timeout handling
- Prompt versioning
- Consistency evaluation across repeated runs
- PostgreSQL metrics storage
- Basic dashboard for latency, failures, and consistency trends

## Architecture

```text
Client
  |
  v
FastAPI API Layer
  |
  v
Model Adapter Layer
  |----------------|
  | OpenAI         |
  | Anthropic      |
  |----------------|
  |
  v
Metrics Collector
  |
  v
PostgreSQL