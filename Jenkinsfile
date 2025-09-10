pipeline {
    agent any

    environment {
        // Service Account key stored in Jenkins credentials
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gke-sa-key')
        PROJECT_ID = "useful-variety-470306-n5"
        CLUSTER = "my-gke-cluster"
        ZONE = "us-central1-a"
        REPO = "mydocker"
        APP_NAME = "gke-app"
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

                    // Save for next stage
                    env.IMAGE_TAG = imageTag
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                    # Apply manifests (first-time deployment)
                    kubectl apply -f k8s/

                    # Update the deployment with the new image
                    kubectl set image deployment/${APP_NAME} ${APP_NAME}=${IMAGE_TAG} --namespace=default
                """
            }
        }
    }
}
