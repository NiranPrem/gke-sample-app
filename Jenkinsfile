pipeline {
    agent any

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gke-sa-key')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github-token', url: 'https://github.com/NiranPrem/gke-sample-app.git'
            }
        }

        stage('Auth to GCP') {
            steps {
                sh '''
                    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                    gcloud config set project useful-variety-470306-n5
                    gcloud config set compute/zone us-central1-a
                    gcloud container clusters get-credentials my-gke-cluster --zone us-central1-a --project useful-variety-470306-n5
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    def imageTag = "us-central1-docker.pkg.dev/useful-variety-470306-n5/mydocker/gke-app:${env.BUILD_NUMBER}"
                    sh """
                        gcloud auth configure-docker us-central1-docker.pkg.dev -q
                        docker build -t ${imageTag} .
                        docker push ${imageTag}
                        sed -i 's|IMAGE_PLACEHOLDER|${imageTag}|g' k8s/deployment.yaml
                    """
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
