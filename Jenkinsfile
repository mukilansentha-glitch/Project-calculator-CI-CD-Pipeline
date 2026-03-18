pipeline {
    agent any
    environment {
        IMAGE_NAME = 'calculator-app-project:v2'
        AWS_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "958006149889"
        REPO_NAME = "calculator"
    }

    stages {
        stage('Cloud') {
            steps {
                echo 'Cloud app deploy with CI/CD pipeline'
            }
        }

        stage('Git Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'git-tocken',
                    url: 'https://github.com/mukilansentha-glitch/cluad-app.git'
            }
        }

        stage('Trivy FS scanner') {
            steps {
                sh 'trivy fs --format table .'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    $SCANNER_HOME/opt/sonar-scanner/bin/sonar-scanner \
                    -Dsonar.projectName=calculator \
                    -Dsonar.projectKey=calculator \
                    -Dsonar.sources=.
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Trivy Image Scanner') {
            steps {
                sh 'trivy image --severity HIGH,CRITICAL $IMAGE_NAME'
            }
        }

        stage('ECR Push') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

                docker tag $IMAGE_NAME $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:v1

                docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:v1
                '''
            }
        }

        stage('K8s Deployment') {
            steps {
                withKubeConfig(
                    caCertificate: '', 
                    clusterName: 'mk1.k8s.local', 
                    contextName: '', 
                    credentialsId: 'k8s-token', 
                    namespace: 'default', 
                    restrictKubeConfigAccess: false, 
                    serverUrl: 'https://api-mk1-k8s-local-bm7bf5-901780fab18605bb.elb.ap-south-1.amazonaws.com'
                ) {
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/svc.yaml'
                }
            }
        }
    }
}
