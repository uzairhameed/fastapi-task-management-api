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
                script{
                 docker_build("fastapi-task-api","latest","uzairhameed")
                               }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script{
                       docker_push('fastapi-task-api', 'fast-task-api', ['latest', env.BUILD_NUMBER]) 
                      }

            }
        }

        stage('Deploy') {
            steps {
                script{
                      docker_compose()
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
