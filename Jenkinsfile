// CSC418 Lab Assignment 3 - Harris Ahmad (FA23-BCT-012)
// Build -> stage -> test with Selenium -> deploy only if every test passes.
pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        skipDefaultCheckout()      // the explicit Checkout stage does it
        disableConcurrentBuilds()  // one staging/prod container name at a time
    }

    environment {
        IMAGE   = 'cicd-012-site'
        STAGING = 'cicd-012-staging'
        PROD    = 'cicd-012-prod'
        NET     = 'cicd-net'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f $STAGING 2>/dev/null || true
                    docker run -d --name $STAGING --network $NET $IMAGE:$BUILD_NUMBER
                    for i in $(seq 1 15); do
                        if curl -sf http://$STAGING/ > /dev/null; then
                            echo "Staging is up at http://$STAGING/ after ${i}s"
                            exit 0
                        fi
                        sleep 1
                    done
                    echo "Staging did not answer within 15s"
                    exit 1
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args "--network ${NET}"
                    reuseNode true
                }
            }
            environment {
                HOME     = '/tmp'
                BASE_URL = "http://${STAGING}"
            }
            steps {
                sh 'pytest tests/test_site.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f $PROD 2>/dev/null || true
                    docker run -d --name $PROD --restart unless-stopped -p 80:80 $IMAGE:$BUILD_NUMBER
                    echo "Deployed $IMAGE:$BUILD_NUMBER to http://localhost/"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $STAGING 2>/dev/null || true'
        }
        success {
            echo "Pipeline succeeded: build #${BUILD_NUMBER} is live at http://localhost/"
        }
        failure {
            echo "Pipeline failed: build #${BUILD_NUMBER} was NOT deployed; production is unchanged."
        }
    }
}
