Bridge RNA Designer
===================

A command line and web interface for designing Bridge RNAs for Bridge Editing.

# CLI

## Installation

```bash
pip install -e .
```

## Usage

Command to design a Bridge RNA for a given target and donor sequence.
```bash
brna-design --target ATCGGGCCTACGCA --donor ACAGTATCTTGTAT
```

Example output:

```console
# STOCKHOLM 1.0
BridgeRNA_tgt_ATCGGGCCTACGCA_dnr_ACAGTATCTTGTAT     AGTGCAGAGAAAATCGGCCAGTTTTCTCTGCCTGCAGTCCGCATGCCGTATCGGGCCTTGGGTTCTAACCTGTTGCGTAGATTTATGCAGCGGACTGCCTTTCTCCCAAAGTGATAAACCGGACAGTATCATGGACCGGTTTTCCCGGTAATCCGTATTTACAAGGCTGGTTTCACT
#=GC bRNA_template                                  AGTGCAGAGAAAATCGGCCAGTTTTCTCTGCCTGCAGTCCGCATGCCGTNNNNNNNNNTGGGTTCTAACCTGTNNNNNNNNNTTATGCAGCGGACTGCCTTTCTCCCAAAGTGATAAACCGGNNNNNNNNATGGACCGGTTTTCCCGGTAATCCGTNNTTNNNNNNNTGGTTTCACT
#=GC guides                                         .................................................LLLLLLLCC...............RRRRRCCHH........................................lllllllc..........................rr..rrrcchh..........
#=GC SS                                             ((.(((((((((((......)))))))))))))(((((((((.(((.............<(((.<>.)))>...............))))))))))))...........((((...<(((..........<.(((((((.....)))))...))....>.........)))>.))))
//
```

# Web tool

## Deployment

Set parameters

```bash
PORT=8080
IMG_NAME=bridge-rna-designer
IMG_VERSION=0.1.0
GCP_PROJECT_ID="arc-hsulab-apps"
SERVICE_ACCOUNT_EMAIL="arc-hsulab-apps@arc-hsulab-apps.iam.gserviceaccount.com"
SERVICE_ACCOUNT_JSON="arc-hsulab-apps1.json"
```

### Docker


Build the container:

```bash
# set env vars

docker build --platform linux/amd64 -t ${IMG_NAME}:${IMG_VERSION} .
```

To run locally:

```bash
docker run -it --rm \
  -p 8080:8080 \
  --platform linux/amd64 \
  --env PORT=${PORT} \
  ${IMG_NAME}:${IMG_VERSION}
```

You can use `--entrypoint /bin/bash` to run the docker container in interactive mode.

### Artifact Registry

**If needed**, create Artifact Registry:

```bash
DESCRIPTION="Bridge RNA Designer web tool"
gcloud artifacts repositories create ${IMG_NAME} \
  --repository-format=docker \
  --project=${GCP_PROJECT_ID} \
  --location=us-west1 \
  --description="${DESCRIPTION}" \
  --async
```

Push to Artifact Registry:

```bash
docker tag ${IMG_NAME}:${IMG_VERSION} \
  us-west1-docker.pkg.dev/${GCP_PROJECT_ID}/${IMG_NAME}/${IMG_NAME}:${IMG_VERSION} \
  && docker push us-west1-docker.pkg.dev/${GCP_PROJECT_ID}/${IMG_NAME}/${IMG_NAME}:${IMG_VERSION}
```

### GCP Cloud Run

Deploy to Cloud Run:

```bash
gcloud run deploy ${IMG_NAME} \
  --service-account=${SERVICE_ACCOUNT_EMAIL} \
  --image=us-west1-docker.pkg.dev/${GCP_PROJECT_ID}/${IMG_NAME}/${IMG_NAME}:${IMG_VERSION} \
  --region=us-west1 \
  --project=${GCP_PROJECT_ID} \
  --cpu=2 \
  --memory=2Gi \
  --max-instances=1 \
  --concurrency=80 \
  --allow-unauthenticated \
  && gcloud run services update-traffic \
    --project=${GCP_PROJECT_ID} \
    --region=us-west1 \
    --to-latest \
    ${IMG_NAME}
```


