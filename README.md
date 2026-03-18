DevSecOps CI/CD Pipeline Project

This project demonstrates a complete CI/CD pipeline for a Python-based calculator application

Tools Used

Tool	              Purpose
GitHub	            Source Code Management (SCM)
Jenkins	            CI/CD Pipeline Automation
Trivy	              Vulnerability Scanning
SonarQube	          Code Quality Analysis
Docker	            Containerization
AWS ECR	            Container Image Repository
Kubernetes	        Container Orchestration

Pipeline Stages

1. Code checkout from GitHub
2. Trivy filesystem scan
3. SonarQube code analysis
4. Docker image build
5. Trivy image scan
6. Push image to AWS ECR
7. Deploy to Kubernetes

Security

* Vulnerability scanning at code and container level
* Secure image deployment

Outcome

Fully automated DevSecOps pipeline with security and quality gates.
