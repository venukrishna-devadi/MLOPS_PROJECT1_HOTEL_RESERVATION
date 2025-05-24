pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
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

        }

    }