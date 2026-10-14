pipeline {
    agent any

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
                echo '📥  Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo '🧪  Creating virtual environment and running tests...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳  Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀  Deploying new container...'

                /* Stop and remove old container — ignore errors if it does not exist */
                sh """
                    echo 'Stopping previous container (if any)...'
                    docker stop ${CONTAINER_NAME} || true
                    docker rm   ${CONTAINER_NAME} || true
                """

                /* Run new container */
                sh """
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${HOST_PORT}:${CONTAINER_PORT} \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """

                echo "✅  Container '${CONTAINER_NAME}' started on port ${HOST_PORT}."
            }
        }

        stage('Health Check') {
            steps {
                echo '🏥  Verifying application health...'

                /*
                 * Use double-quoted sh so HOST_PORT is interpolated by Groovy.
                 * Escape the curl format placeholder (%{http_code}) with a
                 * backslash so Groovy does not treat it as a GString expression.
                 */
                sh """
                    MAX_RETRIES=10
                    WAIT_SECONDS=3
                    HEALTH_URL="http://127.0.0.1:${HOST_PORT}/health"

                    for i in \$(seq 1 \$MAX_RETRIES); do
                        STATUS=\$(curl -s -o /dev/null -w "\\\${http_code}" "\$HEALTH_URL" || true)
                        if [ "\$STATUS" = "200" ]; then
                            echo "✅  Health check passed (attempt \$i) — HTTP \$STATUS"
                            exit 0
                        fi
                        echo "⏳  Attempt \$i/\$MAX_RETRIES — HTTP \$STATUS. Retrying in \${WAIT_SECONDS}s..."
                        sleep \$WAIT_SECONDS
                    done

                    echo "❌  Health check failed after \$MAX_RETRIES attempts."
                    exit 1
                """
            }
        }
    }

    post {
        success {
            echo "🎉  Pipeline completed successfully! App running at http://<EC2-PUBLIC-IP>:${HOST_PORT}"
        }
        failure {
            echo '❌  Pipeline failed. Check the stage logs above for details.'
        }
        always {
            sh 'rm -rf venv'
        }
    }
}
