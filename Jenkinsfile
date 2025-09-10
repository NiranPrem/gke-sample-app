pipeline {
    agent any

    environment {
        // GCP Service Account key stored in Jenkins credentials
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gke-sa-key')
        PROJECT_ID = "useful-variety-470306-n5"
        CLUSTER = "gke-sample-cluster"
        ZONE = "us-central1-c"
        REPO = "mydocker"
        APP_NAME = "gke-app"
    }

    tools {
        maven 'Maven'   // make sure Maven tool is configured in Jenkins
        jdk 'jdk17'     // make sure JDK 17 is configured in Jenkins
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

        stage('Build & Unit Test') {
            steps {
                sh 'mvn clean install'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQube') {   // Name must match Jenkins SonarQube config
                    sh 'mvn sonar:sonar -Dsonar.projectKey=gke-sample-app'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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
