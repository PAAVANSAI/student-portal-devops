
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        IMAGE_NAME     = 'student-portal'
        IMAGE_TAG      = '1.0'
        CONTAINER_NAME = 'student-portal'
        HOST_PORT      = '8081'
        CONTAINER_PORT = '8080'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Installing dependencies and running tests'
                sh '''
                    set -eu
                    python3 -m venv .venv-ci
                    . .venv-ci/bin/activate
                    python -m pip install -r requirements.txt
                    python -m pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                sh '''
                    set -eu
                    docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying Student Portal container'
                sh '''
                    set -eu

                    docker rm -f "$CONTAINER_NAME" || true

                    docker run -d \
                        --name "$CONTAINER_NAME" \
                        --restart unless-stopped \
                        -p "$HOST_PORT:$CONTAINER_PORT" \
                        "$IMAGE_NAME:$IMAGE_TAG"
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Checking application health'
                sh '''
                    set -eu

                    HEALTH_URL="http://127.0.0.1:${HOST_PORT}/health"
                    MAX_RETRIES=10
                    WAIT_SECONDS=3

                    for i in $(seq 1 "$MAX_RETRIES"); do
                        STATUS=$(curl -sS -o /dev/null \
                            -w '%{http_code}' "$HEALTH_URL" || true)

                        if [ "$STATUS" = "200" ]; then
                            echo "Health check passed: HTTP $STATUS"
                            exit 0
                        fi

                        echo "Attempt $i/$MAX_RETRIES: HTTP $STATUS"
                        sleep "$WAIT_SECONDS"
                    done

                    docker logs "$CONTAINER_NAME" || true
                    echo "Health check failed"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded: Student Portal is healthy.'
        }
        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }
        always {
            sh 'rm -rf .venv-ci'
        }
    }
}
