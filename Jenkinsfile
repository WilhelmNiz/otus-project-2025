pipeline {
    agent any

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://ggr:4444/wd/hub', description: 'Адрес Selenoid хаба')
        string(name: 'OPENCART_URL', defaultValue: 'http://192.168.31.202:8081/', description: 'Адрес приложения OpenCart')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер для запуска тестов')
        string(name: 'BROWSER_VERSION', defaultValue: '128.0', description: 'Версия браузера')
        string(name: 'THREADS', defaultValue: '1', description: 'Количество потоков (workers) для pytest')
        booleanParam(name: 'HEADLESS', defaultValue: false, description: 'Запуск в headless-режиме')
        booleanParam(name: 'REMOTE', defaultValue: true, description: 'Использовать удаленный Selenoid')
        booleanParam(name: 'ENABLE_VNC', defaultValue: false, description: 'Включить VNC')
        booleanParam(name: 'ENABLE_VIDEO', defaultValue: false, description: 'Включить запись видео')
        string(name: 'DB_HOST', defaultValue: '192.168.31.202', description: 'Хост БД')
        string(name: 'DB_USER', defaultValue: 'bn_opencart', description: 'Пользователь БД')
        string(name: 'DB_PASSWORD', defaultValue: '', description: 'Пароль БД')
    }

    environment {
        PYTHON_VERSION = '3'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Otus_10',
                url: 'https://github.com/WilhelmNiz/Otus-selenium-2025.git'
            }
        }

        stage('Setup Python') {
            steps {
                script {
                     sh "python3 -m venv venv"
                     sh ". venv/bin/activate && pip install --upgrade pip"
                     sh ". venv/bin/activate && pip install -r requirements.txt"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def pytestCmd = ". venv/bin/activate && python -m pytest "

                    pytestCmd += " --browser ${params.BROWSER}"
                    pytestCmd += " --url ${params.OPENCART_URL}"
                    pytestCmd += " --browser_version ${params.BROWSER_VERSION}"
                    pytestCmd += " --db_host ${params.DB_HOST}"
                    pytestCmd += " --db_user ${params.DB_USER}"

                    if (params.DB_PASSWORD.trim()) {
                        pytestCmd += " --db_password '${params.DB_PASSWORD}'"
                    } else {
                        pytestCmd += " --db_password ''"
                    }

                    if (params.HEADLESS.toBoolean()) {
                        pytestCmd += " --headless"
                    }
                    if (params.REMOTE.toBoolean()) {
                        pytestCmd += " --remote"
                        pytestCmd += " --remote_url ${params.SELENOID_URL}"
                    }
                    if (params.ENABLE_VNC.toBoolean()) {
                        pytestCmd += " --enable_vnc"
                    }
                    if (params.ENABLE_VIDEO.toBoolean()) {
                        pytestCmd += " --enable_video"
                    }

                    // Allure результаты
                    pytestCmd += " --alluredir=${env.WORKSPACE}/allure-results"

                    echo "Запускаем команду: ${pytestCmd}"
                    sh pytestCmd
                }
            }

            post {
                always {
                    allure includeProperties: false,
                        jdk: '',
                        results: [[path: 'allure-results']],
                        reportBuildPolicy: 'ALWAYS'

                    archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh 'rm -rf venv || true'
                    echo "Очистка завершена"
                }
            }
        }
    }

    post {
        always {
            echo "Сборка завершена: ${currentBuild.result}"
        }
        success {
            echo "Тесты прошли успешно! Отчет Allure доступен."
        }
        failure {
            echo "В тестах найдены неудачи."
        }
        unstable {
            echo "Сборка помечена как нестабильная."
        }
    }
}