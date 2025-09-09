pipeline {
    agent any

    environment {
        PROJECT_ID = 'useful-variety-470306-n5'
        CLUSTER = 'my-gke-cluster'
        ZONE = 'us-central1-a'
        REGION = 'us-central1'
        REPO = 'mydocker'
        IMAGE = 'gke-app'
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gke-sa-key')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/NiranPrem/gke-sample-app.git'
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
                sh '''
                  gcloud auth configure-docker $REGION-docker.pkg.dev -q
                  docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$BUILD_NUMBER .
                  docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$BUILD_NUMBER
                '''
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh '''
                  sed -i "s|IMAGE_PLACEHOLDER|$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:$BUILD_NUMBER|" k8s/deployment.yaml
                  kubectl apply -f k8s/
                '''
            }
        }
    }
}
