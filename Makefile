include .env
GOOGLE_REGION=asia-northeast1
DOCKER_BASE_URL=${GOOGLE_REGION}-docker.pkg.dev
SERVICE_NAME=sakamomo-service-creator
DOCKER_URL=${DOCKER_BASE_URL}/${GOOGLE_CLOUD_PROJECT}/${SERVICE_NAME}

setup:
	gcloud auth configure-docker ${DOCKER_BASE_URL}

build:
	docker build -t ${DOCKER_URL}:latest .

push_image:
	docker push ${DOCKER_URL}:latest

run_local:
	docker run --env GEMINI_API_KEY=${GEMINI_API_KEY} --env GOOGLE_API_KEY=${GOOGLE_API_KEY} --env GOOGLE_CSE_ID=${GOOGLE_CSE_ID}
