pipeline {
    agent any

    environment {
        // Service Account key stored in Jenkins credentials
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

                    # 🔄 Update to your new Project ID
                    gcloud config set project useful-variety-470306-n5

                    # 🔄 Update to your new Zone/Region
                    gcloud config set compute/zone us-central1-a

                    # 🔄 Update to your new Cluster name
                    gcloud container clusters get-credentials my-gke-cluster --zone us-central1-a --project useful-variety-470306-n5
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    // 🔄 Update project-id/registry/repo name if changed
                    def imageTag = "us-central1-docker.pkg.dev/useful-variety-470306-n5/mydocker/gke-app:${env.BUILD_NUMBER}"

                    sh """
                        gcloud auth configure-docker us-central1-docker.pkg.dev -q
                        docker build -t ${imageTag} .
                        docker push ${imageTag}
                    """

                    // Save the image tag for next stage
                    env.IMAGE_TAG = imageTag
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh """
                    # First time apply deployment & service (if not created yet)
                    kubectl apply -f k8s/

                    # Update only the image safely
                    kubectl set image deployment/gke-app gke-app=${IMAGE_TAG} --namespace=default
                """
            }
        }
    }
}
