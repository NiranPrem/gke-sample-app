pipeline {
    agent any

    environment {
        PROJECT = "gke-sample-app"
        IMAGE = "gcr.io/useful-variety-470306-n5/gke-sample-app:${BUILD_NUMBER}"
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-creds') // Jenkins secret file ID
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/NiranPrem/gke-sample-app.git'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                sh """
                  gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                  gcloud auth configure-docker -q
                  docker build -t $IMAGE .
                  docker push $IMAGE
                """
            }
        }

        stage('Update Manifests') {
            steps {
                sh """
                  sed -i 's|image:.*|image: $IMAGE|' k8s/deployment.yaml
                  git config --global user.email "jenkins@ci.com"
                  git config --global user.name "Jenkins CI"
                  git commit -am "Update image to $IMAGE"
                  git push origin main
                """
            }
        }
    }
}
