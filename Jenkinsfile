pipeline {
    agent any

    environment {
        // Service Account key stored in Jenkins credentials
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gke-sa-key')
        PROJECT_ID = "useful-variety-470306-n5"
        CLUSTER = "gke-sample-cluster"
        ZONE = "us-central1-c"
        REPO = "mydocker"
        APP_NAME = "gke-app"

        // SonarQube
        SCANNER_HOME = tool 'SonarQubeScanner'  // Configure in Jenkins Global Tools
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/NiranPrem/gke-sample-app.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQubeServer') { // Name from Jenkins SonarQube config
                    sh """
                        ${SCANNER_HOME}/bin/sonar-scanner \
                          -Dsonar.projectKey=${APP_NAME} \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=http://34.42.95.114:9000 \
                          -Dsonar.login=$SONAR_AUTH_TOKEN
                    """
                }
            }
        }

        stage('Auth to GCP') {
            steps {
                sh '''
                    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                    gcloud config set project $PROJECT_ID
                    gcloud config set compute/zone $ZONE
                    gcloud container clusters get-credentials $CLUSTER --zone $ZONE --project $PROJECT_ID
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    def imageTag = "us-central1-docker.pkg.dev/${PROJECT_ID}/${REPO}/${APP_NAME}:${env.BUILD_NUMBER}"

                    sh """
                        gcloud auth configure-docker us-central1-docker.pkg.dev -q
                        docker build -t ${imageTag} .
                        docker push ${imageTag}
                    """

                    env.IMAGE_TAG = imageTag
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                    kubectl apply -f k8s/
                    kubectl set image deployment/${APP_NAME} ${APP_NAME}=${IMAGE_TAG} --namespace=default
                """
            }
        }
    }
}
