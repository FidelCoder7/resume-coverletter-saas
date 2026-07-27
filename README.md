# resume-coverletter-saas

Production-ready AI Resume & Cover Letter SaaS built with FastAPI, React, PostgreSQL, Stripe, Docker, and modern DevOps practices.

## Current Status

**Current Version:** **v1.8.0**  
**Status:** Subscription & Usage Limits completed and frozen



## Features

### Authentication & User Management

* User registration
* JWT authentication
* Login / Logout
* Refresh tokens
* Email verification
* Password reset
* Google OAuth
* User profile management
* Role-based access
* Subscription plan support
* Rate limiting
* Security headers


### Resume Management

* Resume CRUD
* Experience management
* Education management
* Skills management
* Projects management
* Certifications management
* Default resume support
* Resume version snapshots
* Resume version history
* Automatic version creation
* Historical resume restoration
* Immutable historical versions
* Restore operations create new version history entries
* Full nested resume content restoration


### Resume Versioning & History

* Historical resume snapshots
* Sequential per-resume version numbering
* Version history retrieval
* Version ownership and access control
* Immutable historical snapshots
* Restore previous resume versions
* Restore complete resume state
* Restore experiences
* Restore education
* Restore skills
* Restore projects
* Restore certifications
* Automatic `RESTORE` version creation
* Internal service-layer version creation
* No public manual version creation endpoint


### Cover Letter Management

* Cover letter CRUD
* AI-powered cover letter generation
* AI cover letter regeneration


### AI Resume Features

* AI resume generation
* Resume formatting pipeline
* Prompt builder architecture
* Provider abstraction
* Retry and resilience support
* AI execution metadata
* AI usage tracking
* AI provider capability detection
* Structured AI logging and monitoring
* ATS resume optimization


### ATS Resume Optimization

* AI-powered resume optimization
* Keyword extraction
* ATS keyword matching
* ATS scoring engine
* Missing keyword detection
* Matched keyword reporting
* Optimization recommendations framework
* AI usage tracking for ATS optimization


### Subscription & Usage Limits

* Subscription plan architecture
* Free and Pro subscription plans
* Plan-specific AI feature limits
* Monthly usage periods
* Resume generation limits
* Cover letter generation limits
* Cover letter regeneration limits
* ATS optimization limits
* Plan limit persistence
* Plan limit repository
* Plan limit service layer
* Usage status calculation
* Current-period AI usage tracking
* Remaining usage calculation
* Subscription limit enforcement
* Feature-specific usage tracking
* Subscription limit exceeded handling
* Plan limit API endpoints
* Authenticated subscription limit access
* Database-seeded default plan limits
* Deterministic subscription and usage limit tests


### Platform Architecture

* Repository pattern
* Service layer architecture
* Dependency Injection
* SQLAlchemy 2.x
* Pydantic v2
* Alembic migrations
* Modular API architecture
* Provider-agnostic AI architecture
* Subscription-aware AI workflows


### Quality & Testing

* Comprehensive unit tests
* Integration tests
* End-to-end workflow tests
* Fake AI provider for deterministic testing
* Production-ready testing infrastructure
* Resume versioning and restore workflow tests
* Subscription and usage limit tests
* Plan limit repository tests
* Subscription service tests
* Subscription API tests
* AI usage tracking tests



## Technology Stack

### Backend

* FastAPI
* SQLAlchemy 2.x
* PostgreSQL
* Alembic
* Pydantic v2
* JWT Authentication

### AI

* OpenAI Provider
* Provider abstraction layer
* Retry framework
* AI usage analytics
* Prompt engineering
* AI observability
* ATS optimization

### Frontend

* React
* Vite

### Payments & Subscriptions

* Subscription plan architecture
* Usage-based feature limits
* Monthly quota enforcement
* Stripe integration (planned)
* Pesapal integration (planned)

### DevOps

* Docker
* Docker Compose
* GitHub Actions (planned)
* Production deployment (planned)



## Version History

| Version | Milestone                                      | Status |
| ------- | ---------------------------------------------- | ------ |
| v0.1.0  | Project Setup                                  | ✅      |
| v0.2.0  | Authentication Foundation                      | ✅      |
| v0.3.0  | User Management & Security                     | ✅      |
| v0.4.0  | Resume CRUD                                    | ✅      |
| v0.5.0  | Experience Management                          | ✅      |
| v0.6.0  | Education Management                           | ✅      |
| v0.7.0  | Skills Management                              | ✅      |
| v0.8.0  | Projects Management                            | ✅      |
| v0.9.0  | Certifications Management                      | ✅      |
| v1.0.0  | Cover Letter CRUD & AI Cover Letter Generation | ✅      |
| v1.1.0  | AI Resume Generation                           | ✅      |
| v1.2.0  | AI Platform Enhancements                       | ✅      |
| v1.3.0  | AI Platform Improvements                       | ✅      |
| v1.3.1  | AI Provider Architecture Refactor              | ✅      |
| v1.4.0  | AI Reliability & Resilience                    | ✅      |
| v1.5.0  | AI Observability & Monitoring                  | ✅      |
| v1.6.0  | ATS Resume Optimization Engine                 | ✅      |
| v1.7.0  | Resume Versioning & History                    | ✅      |
| v1.8.0  | Subscription & Usage Limits                    | ✅      |



## Testing

The project includes:

* Unit tests
* Integration tests
* End-to-end workflow tests
* Repository tests
* Service tests
* API endpoint tests
* AI provider tests
* Authentication tests
* Resume management tests
* Cover letter tests
* ATS optimization tests
* Resume versioning tests
* Resume restoration tests
* Subscription tests
* Plan limit tests
* Usage enforcement tests

The project is maintained with a focus on:

* Deterministic automated testing
* Service and repository separation
* Database transaction integrity
* API-level integration coverage
* AI provider isolation through fake providers
* Subscription limit enforcement
* Feature-specific usage tracking
* Test database isolation



## Roadmap

### Upcoming

* Billing & Payment Integration
* Pesapal payment integration
* Subscription lifecycle management
* Subscription activation and renewal
* Payment transaction tracking
* Resume Export (PDF/DOCX)
* Public Resume Sharing
* Recruiter Portal
* Admin Dashboard
* Docker Production Deployment
* CI/CD Pipeline
* Kubernetes Deployment



## Completed Milestones

The following major capabilities have been completed:

* Authentication & User Management
* Resume CRUD
* Resume Content Management
* AI Resume Generation
* AI Cover Letter Generation
* AI Provider Architecture
* AI Retry & Resilience
* AI Usage Tracking
* AI Observability & Monitoring
* ATS Resume Optimization
* Resume Versioning & History
* Subscription & Usage Limits

**Current milestone:** `v1.8.0`  
**Release status:** Complete and frozen