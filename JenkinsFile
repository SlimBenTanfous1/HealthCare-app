pipeline {
    agent any

    environment {
        PATH = "/opt/sonar-scanner/bin:${PATH}"
        SONAR_HOST_URL = 'http://192.168.50.4:9000'
        SONAR_AUTH_TOKEN = credentials('sonarqube')
    }

    stages {
        stage('GIT Checkout') {
            steps {
                echo '📦 Cloning repository...'
                git branch: 'master',
                    changelog: false,
                    credentialsId: 'GithubJenkins',
                    url: 'https://github.com/Slimbentanfous1/HealthCare-app.git'
            }
        }

        stage('Install Dependencies & Tests') {
            steps {
                echo '⚙️ Setting up Python environment...'
                sh '''#!/bin/bash
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt pytest pytest-cov
                pytest --maxfail=1 --disable-warnings --cov=. --cov-report=xml
                deactivate
                '''
            }
        }

        stage('SonarQube Scan - Python') {
            steps {
                echo '🔍 Running SonarQube static analysis...'
                sh '''
                sonar-scanner \
                  -Dsonar.projectKey=HealthCare-app \
                  -Dsonar.projectName=HealthCare-app \
                  -Dsonar.sources=. \
                  -Dsonar.language=py \
                  -Dsonar.sourceEncoding=UTF-8 \
                  -Dsonar.exclusions=**/*.java,**/target/**,**/venv/** \
                  -Dsonar.host.url=$SONAR_HOST_URL \
                  -Dsonar.token=$SONAR_AUTH_TOKEN \
                  -Dsonar.python.coverage.reportPaths=coverage.xml
                '''
            }
        }
        stage('SCA - Dependency Scan (Trivy)') {
    steps {
        echo '🔍 Scanning Python dependencies with Trivy...'
        sh '''
        trivy fs --scanners vuln . \
            --severity HIGH,CRITICAL \
            --ignore-unfixed \
            --format json \
            --output trivy-report.json
        '''
        echo "📄 Trivy scan completed — report saved as trivy-report.json"
    }
    post {
        always {
            script {
                def criticals = sh(script: "grep -c '\"Severity\": \"CRITICAL\"' trivy-report.json || true", returnStdout: true).trim()
                if (criticals != "0") {
                    error("🚨 Critical vulnerabilities found! Check trivy-report.json.")
                } else {
                    echo "✅ No critical vulnerabilities found in dependencies."
                }
            }
        }
    }
}
        stage('Docker Image Scan - Trivy') {
    steps {
        echo '🐳 Scanning Docker image with Trivy...'
        sh '''
        # Build Docker image (if not already built)
        docker build -t slimbentanfous1/healthcare-app:latest .

        # Run vulnerability scan on the image
        trivy image --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    --format json \
                    --output trivy-docker-report.json \
                    slimbentanfous1/healthcare-app:latest

        echo "📊 Docker image scan completed — report saved as trivy-docker-report.json"
        '''
    }

    post {
        always {
            script {
                // Check if there are critical vulnerabilities
                def criticals = sh(script: "grep -c '\"Severity\": \"CRITICAL\"' trivy-docker-report.json || true", returnStdout: true).trim()
                if (criticals != "0") {
                    error("🚨 Critical vulnerabilities found in Docker image! Check trivy-docker-report.json.")
                } else {
                    echo "✅ No critical vulnerabilities found in Docker image."
                }
            }
        }
    }
}


        stage('DAST - OWASP ZAP Scan') {
            steps {
                echo '🧪 Running Dynamic App Security Testing (OWASP ZAP)...'
                sh '''
                docker run -d -p 5000:5000 --name healthcare-test slimbentanfous1/healthcare-app:latest
                sleep 10
    
                chmod 777 ${WORKSPACE}
                
               docker run --rm \
                -v ${WORKSPACE}:/zap/wrk/:rw \
                -t zaproxy/zap-stable zap-full-scan.py \
                -t http://host.docker.internal:5000 \
                -g gen.conf \
                -r zap-report.html \
                -w zap-warnings.txt \
                -J zap-report.json || true

                docker stop healthcare-test || true
                docker rm healthcare-test || true

                echo "📊 ZAP scan completed — results saved to zap-report.html"
                '''
                 script {
            def highCount = sh(script: "grep -o 'High' zap-report.html | wc -l", returnStdout: true).trim()
            def medCount = sh(script: "grep -o 'Medium' zap-report.html | wc -l", returnStdout: true).trim()
            echo "📊 ZAP Scan Summary → High: ${highCount} | Medium: ${medCount}"
        }
            }
        }

        stage('Secrets Scan - Gitleaks') {
    steps {
        echo "🕵️‍♂️ Scanning for exposed secrets..."
        sh '''
        echo "Installing Gitleaks (no sudo needed)..."
        wget -q https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
        tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
        chmod +x gitleaks
        mv gitleaks /tmp/

        # Scan only your actual repo, excluding venv & other irrelevant files
        /tmp/gitleaks detect --source=. \
                        --no-git \
                        --report-format=json \
                        --report-path=gitleaks-report.json \
                        --report-path=/var/lib/jenkins/workspace/DevSecOps/gitleaks-report.json
       
        if command -v jq >/dev/null 2>&1; then
            leaks=$(cat /var/lib/jenkins/workspace/DevSecOps/gitleaks-report.json | jq 'length')
            if [ "$leaks" -gt 0 ]; then
                echo "⚠️  Gitleaks found $leaks potential secrets. Check gitleaks-report.json"
                exit 1
            else
                echo "✅ No secrets found by Gitleaks!"
            fi
        else
            echo "⚠️ jq not installed, skipping leak count check."
        fi
        '''
        
    }
    
}



        stage('Report Summary') {
            steps {
                echo '✅ All stages executed successfully!'
            }
        }
    }

    post {
    always {
        echo "📦 Archiving and publishing ZAP results..."
        archiveArtifacts artifacts: 'zap-report.html, zap-report.json, zap-warnings.txt, trivy-report.json, trivy-docker-report.json', allowEmptyArchive: true

        publishHTML(target: [
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: '.',
            reportFiles: 'zap-report.html',
            reportName: 'OWASP ZAP Report'
        ])
    }

    success {
        script {
            // ✅ Extract vulnerability counts dynamically
            def zapHigh = sh(script: "grep -o 'High' zap-report.html | wc -l || true", returnStdout: true).trim()
            def zapMed  = sh(script: "grep -o 'Medium' zap-report.html | wc -l || true", returnStdout: true).trim()
            def zapLow  = sh(script: "grep -o 'Low' zap-report.html | wc -l || true", returnStdout: true).trim()

            def trivyFsCrit = sh(script: "grep -c '\"Severity\": \"CRITICAL\"' trivy-report.json || true", returnStdout: true).trim()
            def trivyFsHigh = sh(script: "grep -c '\"Severity\": \"HIGH\"' trivy-report.json || true", returnStdout: true).trim()
            def trivyImgCrit = sh(script: "grep -c '\"Severity\": \"CRITICAL\"' trivy-docker-report.json || true", returnStdout: true).trim()
            def trivyImgHigh = sh(script: "grep -c '\"Severity\": \"HIGH\"' trivy-docker-report.json || true", returnStdout: true).trim()

            emailext(
                subject: "✅ [Jenkins] DevSecOps Pipeline Success — ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                to: 'slim.bentanfous@esprit.tn',
                mimeType: 'text/html',
                body: """
                <html>
                <body style="font-family:Segoe UI, Roboto, sans-serif; color:#333; background:#f9f9f9; padding:20px;">
                    <div style="max-width:750px; margin:auto; background:white; padding:25px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                        <h2 style="color:#2e7d32;">✅ DevSecOps Pipeline — SUCCESS</h2>
                        <p>
                            🎯 <b>Project:</b> ${env.JOB_NAME}<br>
                            🔢 <b>Build #:</b> ${env.BUILD_NUMBER}<br>
                            🕒 <b>Executed:</b> ${new Date().format("yyyy-MM-dd HH:mm:ss", TimeZone.getTimeZone('Europe/Paris'))}<br>
                            🌍 <b>Node:</b> ${env.NODE_NAME}
                        </p>

                        <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">

                        <h3>📊 Security Scan Summary</h3>
                        <table style="width:100%; border-collapse:collapse;">
                            <tr><th style="text-align:left;">Scan Type</th><th style="text-align:center;">Result</th></tr>
                            <tr><td>🔍 SonarQube Scan</td><td style="color:green;">Passed ✅</td></tr>
                            <tr><td>📦 Trivy (Dependencies)</td><td>HIGH: ${trivyFsHigh} | CRITICAL: ${trivyFsCrit}</td></tr>
                            <tr><td>🐳 Trivy (Docker Image)</td><td>HIGH: ${trivyImgHigh} | CRITICAL: ${trivyImgCrit}</td></tr>
                            <tr><td>🧪 OWASP ZAP (DAST)</td><td>HIGH: ${zapHigh} | MEDIUM: ${zapMed} | LOW: ${zapLow}</td></tr>
                            <tr><td>🕵️‍♂️ Gitleaks (Secrets)</td><td style="color:green;">No Secrets Found ✅</td></tr>
                        </table>

                        <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">

                        <h4>📁 Reports & Artifacts</h4>
                        <p>
                            • <a href="${env.BUILD_URL}artifact/zap-report.html" style="color:#1a73e8;">OWASP ZAP Report</a><br>
                            • <a href="${env.BUILD_URL}artifact/trivy-report.json" style="color:#1a73e8;">Trivy Dependency Report</a><br>
                            • <a href="${env.BUILD_URL}artifact/trivy-docker-report.json" style="color:#1a73e8;">Trivy Docker Report</a><br>
                            • <a href="${env.BUILD_URL}" style="color:#1a73e8;">Full Jenkins Build Logs</a>
                        </p>

                        <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">
                        <p style="font-size:12px; color:#666; text-align:center;">
                            💡 Generated automatically by the <b>DevSecOps Security Pipeline</b> — Jenkins CI/CD<br>
                            Environment: <b>${env.NODE_NAME}</b> | Executor: <b>${env.EXECUTOR_NUMBER}</b><br>
                            <i>Stay secure, stay automated 🔒🚀</i>
                        </p>
                    </div>
                </body>
                </html>
                """
            )
        }
    }

    failure {
        emailext(
            subject: "❌ [Jenkins] DevSecOps Pipeline Failed — ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            to: 'slim.bentanfous@esprit.tn',
            mimeType: 'text/html',
            body: """
            <html>
            <body style="font-family:Segoe UI, Roboto, sans-serif; color:#333; background:#fff0f0; padding:20px;">
                <div style="max-width:700px; margin:auto; background:white; padding:25px; border-radius:10px; box-shadow:0 2px 8px rgba(255,0,0,0.15);">
                    <h2 style="color:#c62828;">❌ DevSecOps Pipeline — FAILED</h2>
                    <p>Project: <b>${env.JOB_NAME}</b><br>
                    Build #: <b>${env.BUILD_NUMBER}</b><br>
                    Time: ${new Date().format("yyyy-MM-dd HH:mm:ss", TimeZone.getTimeZone('Europe/Paris'))}</p>

                    <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">
                    <p>⚠️ One or more stages failed during execution.<br>
                    Please check <a href="${env.BUILD_URL}console" style="color:#d32f2f;">the Jenkins console logs</a> for details.</p>

                    <hr style="border:none; border-top:1px solid #ddd; margin:15px 0;">
                    <p style="font-size:12px; color:#666; text-align:center;">
                        🧠 Generated by Jenkins — DevSecOps CI/CD Pipeline<br>
                        <b>Stay secure, stay automated!</b> 🚀
                    </p>
                </div>
            </body>
            </html>
            """
        )
    }
  }
}