# cicd-assignment-012

CSC418 Cloud Computing, Lab Assignment 3 (FA 2026): a CI/CD pipeline for a static site.

**Student:** Harris Ahmad, FA23-BCT-012, BCT 7th semester, COMSATS University Islamabad
**Instructor:** Maheen Gul

## What it does

Each push to `main` triggers Jenkins through a GitHub webhook. The pipeline then:

1. **Checkout**: clones this repository.
2. **Package**: builds the nginx image `cicd-012-site:<build number>`.
3. **Start Staging**: runs the image as `cicd-012-staging` on the `cicd-net` Docker network and waits until it answers.
4. **Test**: builds `tests/Dockerfile` (Python, Selenium, headless Chromium) and runs `pytest` against the staging container. JUnit results and `screenshot.png` are published.
5. **Deploy**: replaces `cicd-012-prod` (port 80) with the tested image. This stage only runs if every test passed.

## Files

| File | Purpose |
|---|---|
| `index.html` | The site. Inline CSS and JS, with a name heading, roll number, message button and text echo form |
| `Dockerfile` | Packages `index.html` into `nginx:alpine` |
| `tests/Dockerfile` | Selenium test agent (`python:3.12-slim` with Chromium, ChromeDriver, Selenium and pytest) |
| `tests/test_site.py` | Five Selenium UI tests |
| `Jenkinsfile` | Declarative pipeline: Checkout, Package, Start Staging, Test, Deploy |

## Run the tests by hand

```sh
docker network create cicd-net
docker build -t selenium-test-agent tests/
docker build -t cicd-012-site:manual .
docker run -d --name cicd-012-manual --network cicd-net cicd-012-site:manual
docker run --rm --network cicd-net -e HOME=/tmp -e BASE_URL=http://cicd-012-manual \
  -v "$PWD:/work" -w /work selenium-test-agent pytest tests/test_site.py -v
docker rm -f cicd-012-manual
```
