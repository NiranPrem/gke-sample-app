pipeline {
    agent any

    environment {
        PROJECT_ID = "useful-variety-470306-n5"          // your GCP project
        REGION = "us-central1"
        IMAGE_NAME = "us-central1-docker.pkg.dev/${PROJECT_ID}/mydocker/gke-app"
        SONARQUBE_SERVER = "SonarQube"                  // Jenkins SonarQube server name (Manage Jenkins > Configure Systems)
        SONAR_SCANNER = "SonarScanner"                  // SonarQube Scanner tool name
        GITHUB_CREDENTIALS = "github-token"             // Jenkins credential for GitHub push
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh """
                        ${SONAR_SCANNER}/bin/sonar-scanner \
                        -Dsonar.projectKey=gke-sample-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Auth to GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh """
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project $PROJECT_ID
                        gcloud config set compute/zone us-central1-a
                    """
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    def IMAGE_TAG = "${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh """
                        gcloud auth configure-docker ${REGION}-docker.pkg.dev -q
                        docker build -t ${IMAGE_TAG} .
                        docker push ${IMAGE_TAG}
                    """

                    // Update image tag in k8s/deployment.yaml
                    sh """
                        sed -i 's|image: .*|image: ${IMAGE_TAG}|' k8s/deployment.yaml
                        git config user.email "jenkins@myci.com"
                        git config user.name "Jenkins CI"
                        git add k8s/deployment.yaml
                        git commit -m "Update image to ${IMAGE_TAG}"
                        git push https://github.com/NiranPrem/gke-sample-app.git HEAD:main
                    """
                }
            }
        }
    }
}
