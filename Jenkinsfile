pipeline {
    agent any

    environment {
        PROJECT_ID = "useful-variety-470306-n5"
        REGION = "us-central1"
        REPO = "mydocker"
        IMAGE = "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/gke-app"
        GKE_CLUSTER = "my-gke-cluster"
        GKE_ZONE = "us-central1-a"
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gke-sa-key')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/gke-sample-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER .'
            }
        }

        stage('Push to Artifact Registry') {
            steps {
                sh 'gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS'
                sh 'gcloud auth configure-docker ${REGION}-docker.pkg.dev -q'
                sh 'docker push $IMAGE:$BUILD_NUMBER'
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh 'gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS'
                sh 'gcloud container clusters get-credentials $GKE_CLUSTER --zone $GKE_ZONE --project $PROJECT_ID'
                sh "kubectl set image deployment/gke-app gke-app=$IMAGE:$BUILD_NUMBER --record"
            }
        }
    }
}
