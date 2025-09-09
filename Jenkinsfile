pipeline {
    agent any

    environment {
        PROJECT_ID   = "useful-variety-470306-n5"
        REGION       = "us-central1"
        REPO         = "mydocker"
        IMAGE_NAME   = "gke-app"
        CLUSTER      = "my-gke-cluster"
        CLUSTER_ZONE = "us-central1-a"
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-service-account') // Jenkins secret
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/NiranPrem/gke-sample-app.git'
            }
        }

        stage('Auth to GCP') {
            steps {
                sh """
                  gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                  gcloud config set project $PROJECT_ID
                  gcloud config set compute/zone $CLUSTER_ZONE
                  gcloud container clusters get-credentials $CLUSTER --zone $CLUSTER_ZONE --project $PROJECT_ID
                """
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                sh """
                  gcloud auth configure-docker ${REGION}-docker.pkg.dev -q
                  docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:${BUILD_NUMBER} .
                  docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                  sed -i "s|IMAGE_PLACEHOLDER|${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/${IMAGE_NAME}:${BUILD_NUMBER}|" k8s/deployment.yaml
                  kubectl apply -f k8s/
                """
            }
        }
    }
}
