@Library('Shared') _

pipeline {
    agent { label 'tommy' }

    stages {
        stage('Code') {
            steps {
                script{
                clone('https://github.com/uzairhameed/fastapi-task-management-api.git','main')
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t fastapi-task-api:latest .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerHubCred',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker tag fastapi-task-api:latest "$DH_USER/fast-task-api:latest"
                        docker tag fastapi-task-api:latest "$DH_USER/fast-task-api:${BUILD_NUMBER}"
                        docker push "$DH_USER/fast-task-api:latest"
                        docker push "$DH_USER/fast-task-api:${BUILD_NUMBER}"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([file(credentialsId: 'fastapi-env', variable: 'ENV_FILE')]) {
                    sh '''
                        cp "$ENV_FILE" .env
                        chmod 600 .env
                        docker compose down --remove-orphans
                        docker compose up -d db
                        docker compose run --rm -T api alembic upgrade head
                        docker compose up -d
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'rm -f .env; docker logout || true'
        }
    }
}
