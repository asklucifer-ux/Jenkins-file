pipeline {
  agent any

  environment {
    IMAGE_NAME = "simple_webapp:latest"   // change to your image or registry/image:tag
    TRIVY_JSON  = "trivy-report.json"
    TRIVY_HTML  = "trivy-report.html"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Pull/Build image (optional)') {
      steps {
        // If you build a local image from the repo, enable this. Otherwise comment out.
        // sh 'docker build -t ${IMAGE_NAME} .'
        echo "Assuming image ${IMAGE_NAME} already exists (or is pulled in the next step)"
      }
    }

    stage('Trivy Scan (JSON)') {
      steps {
        // Option A: run trivy binary (if installed on agent)
        // sh "trivy image --format json -o ${TRIVY_JSON} ${IMAGE_NAME}"

        // Option B: run Trivy as a Docker container (works if docker is available on agent). This will create trivy-report.json in workspace.
        sh """
          docker run --rm -v \$PWD:/workdir -w /workdir aquasec/trivy:latest \
            image --format json -o ${TRIVY_JSON} ${IMAGE_NAME}
        """
      }
    }

    stage('Generate HTML from JSON') {
      steps {
        // If python is available on the agent:
        // sh "python3 generate_trivy_html_report.py ${TRIVY_JSON} ${TRIVY_HTML}"

        // Or run Python inside container if python not installed on agent:
        sh """
          docker run --rm -v \$PWD:/workdir -w /workdir python:3.12-slim \
            bash -c "pip install jinja2 || true; python generate_trivy_html_report.py ${TRIVY_JSON} ${TRIVY_HTML}"
        """
      }
    }

    stage('Archive & Publish') {
      steps {
        archiveArtifacts artifacts: "${TRIVY_JSON}, ${TRIVY_HTML}", fingerprint: true

        // If HTML Publisher plugin installed, publish it:
        publishHTML (target: [
          allowMissing: false,
          alwaysLinkToLastBuild: true,
          keepAll: true,
          reportDir: '.',
          reportFiles: "${TRIVY_HTML}",
          reportName: 'Trivy Vulnerability Report'
        ])
      }
    }
  }

  post {
    always {
      // show workspace files for debugging
      sh 'ls -la'
    }
  }
}
