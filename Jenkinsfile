pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'sincere-octane-455720-d4'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }
    
    stages{
        stage('Cloning Github Repo to Jenkins ............'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins .........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/venukrishna-devadi/MLOPS_PROJECT1_HOTEL_RESERVATION.git']])
                }
            }
        }

        stage('Setting up venv and installing dependicies ............'){
            steps{
                script{
                    echo 'Setting up venv and installing dependicies .........'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''

                }
            }
        }

        stage('Building and pushing docker image to gcr ............'){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                    echo 'Building and pushing docker image to gcr .........'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet

                    docker build -t gcr.io/${GCP_POJECT}/ml-project:latest .
                    docker push gcr.io/${GCP_POJECT}/ml-project:latest
                    '''}

                }
            }
        }

        }

    }