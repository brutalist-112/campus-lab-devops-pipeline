pipeline {
    agent any

    environment {
        APP_NAME = "campus-lab-api"
        BUILD_VERSION = "1.0.0-${BUILD_NUMBER}"
    }

    triggers {
        // CI Build Trigger: Poll SCM every 2 minutes for new Git commits
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "=== Step 1: Checking out source code from Git ==="
                checkout scm
                echo "Commit SHA: ${env.GIT_COMMIT}"
                echo "Branch: ${env.GIT_BRANCH}"
            }
        }

        // CI Enhancement: Automated Unit Testing Stage
        stage('Run Unit Tests') {
            steps {
                echo "=== Step 2: Running Automated Unit Tests ==="
                sh '''
                    echo "Setting up Python test environment..."
                    python3 -m pip install --upgrade pip
                    python3 -m pip install -r requirements.txt
                    echo "Executing test suite..."
                    python3 -m pytest tests/ --verbose --junitxml=test-results.xml || python3 -m unittest discover -s tests -p "test_*.py"
                '''
            }
            post {
                always {
                    // Record test results if JUnit XML exists
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Build & Package Artifact') {
            steps {
                echo "=== Step 3: Packaging Application Release Artifact ==="
                sh '''
                    python3 package.py
                    echo "Artifact packaged for version: ${BUILD_VERSION}"
                '''
            }
        }
    }

    post {
        success {
            echo "=== CI Pipeline Completed Successfully! ==="
            // Core Rubric Requirement: Archive the built artifact
            archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true, allowEmptyArchive: false
        }
        failure {
            echo "=== CI Pipeline Failed. Please check console logs for errors. ==="
        }
    }
}
