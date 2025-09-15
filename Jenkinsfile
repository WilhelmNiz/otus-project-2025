pipeline {
    agent any

    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://ggr:4444/wd/hub', description: 'Адрес Selenoid хаба')
        string(name: 'OPENCART_URL', defaultValue: 'http://192.168.31.202:8081/', description: 'Адрес приложения OpenCart')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер для запуска тестов')
        choice(name: 'BROWSER_VERSION', choices: ['128.0', '127.0'], description: 'Версия браузера, передается только в случае REMOTE=true')
        string(name: 'THREADS', defaultValue: '1', description: 'Количество потоков (workers) для pytest')
        booleanParam(name: 'HEADLESS', defaultValue: false, description: 'Запуск в headless-режиме')
        booleanParam(name: 'REMOTE', defaultValue: true, description: 'Использовать удаленный Selenoid (ВКЛЮЧЕНО)')
        booleanParam(name: 'ENABLE_VNC', defaultValue: false, description: 'Включить VNC')
        choice(name: 'TEST_MARK', choices: ['all', 'booking', 'auth', 'backend', 'frontend'], description: 'Марка тестов для запуска')
    }

    environment {
        PYTHON_VERSION = '3'
        // Явно указываем, что используется удаленный запуск
        EXECUTION_MODE = 'REMOTE_SELENOID'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'Otus_project_2025',
                url: 'https://github.com/WilhelmNiz/otus-project-2025'
            }
        }

        stage('Clean Allure Results') {
            steps {
                script {
                    sh 'rm -rf allure-results || true'
                    sh 'mkdir -p allure-results'
                }
            }
        }

        stage('Setup Python') {
            steps {
                script {
                     sh 'rm -rf venv || true'
                     sh "python3 -m venv venv"
                     sh ". venv/bin/activate && pip install --upgrade pip"
                     sh ". venv/bin/activate && pip install -r requirements.txt"
                     sh ". venv/bin/activate && pip install pytest-xdist"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "ЗАПУСК ТЕСТОВ В РЕЖИМЕ REMOTE SELENOID"
                    echo "Selenoid Hub: ${params.SELENOID_URL}"
                    echo "Браузер: ${params.BROWSER} ${params.BROWSER_VERSION}"

                    def pytestCmd = ". venv/bin/activate && python -m pytest "

                    // Принудительно используем многопоточность для remote
                    pytestCmd += " -n ${params.THREADS}"

                    def marks = ""
                    if (params.TEST_MARK != 'all') {
                        marks = params.TEST_MARK
                    }

                    if (marks) {
                        pytestCmd += " -m \"${marks}\""
                    }

                    pytestCmd += " --browser ${params.BROWSER}"
                    pytestCmd += " --url ${params.OPENCART_URL}"
                    pytestCmd += " --browser_version ${params.BROWSER_VERSION}"

                    if (params.HEADLESS.toBoolean()) {
                        pytestCmd += " --headless"
                    }

                    pytestCmd += " --remote"
                    pytestCmd += " --remote_url ${params.SELENOID_URL}"

                    if (params.ENABLE_VNC.toBoolean()) {
                        pytestCmd += " --enable_vnc"
                    }

                    pytestCmd += " --alluredir=${env.WORKSPACE}/allure-results"

                    echo "🔧 Команда запуска: ${pytestCmd}"
                    sh pytestCmd
                }
            }

            post {
                always {
                    allure includeProperties: false,
                        jdk: '',
                        results: [[path: 'allure-results']],
                        reportBuildPolicy: 'ALWAYS'

                    script {
                        def resultsExist = fileExists('allure-results')
                        if (resultsExist) {
                            archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: false
                        }
                    }
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
            echo "Режим выполнения: ${env.EXECUTION_MODE}"
        }
        success {
            echo "✅ Тесты успешно выполнены ! Отчет Allure доступен."
        }
        failure {
            echo "❌ В тестах найдены неудачи."
        }
        unstable {
            echo "⚠️ Сборка помечена как нестабильная."
        }
    }
}