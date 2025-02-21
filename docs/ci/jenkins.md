# Jenkins Pipeline Integration

## Overview

This guide explains how to integrate ARIA with Jenkins Pipeline for automated policy validation and deployment.

## Pipeline Example

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.8'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install aria-policy'
            }
        }
        
        stage('Validate') {
            when {
                changeset 'policies/**'
            }
            steps {
                sh 'aria validate policies/'
            }
        }
        
        stage('Test Templates') {
            when {
                changeset 'templates/**'
            }
            steps {
                sh 'aria test-templates templates/'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                input 'Deploy policies?'
                sh 'aria deploy policies/'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
```

## Setup Instructions

1. Create `Jenkinsfile`
2. Configure Jenkins
3. Set up credentials
4. Enable pipeline

## Best Practices

1. Pipeline organization
2. Error handling
3. Deployment strategy
4. Documentation

## See Also

- [GitHub Actions](github-actions.md)
- [GitLab CI](gitlab-ci.md)
- [Deployment Guide](../technical/deployment.md)
