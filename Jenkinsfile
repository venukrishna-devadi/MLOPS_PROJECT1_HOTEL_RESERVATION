pipeline{
    agent any
    
    srages{
        stage('Cloning Github Repo to Jenkins ............'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins .........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/venukrishna-devadi/MLOPS_PROJECT1_HOTEL_RESERVATION.git']])
                }
            }
        }
        }

    }
}