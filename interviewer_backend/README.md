# WesternPrep (BackEnd)
## Prerequisites

- Python 3.11
- Docker

## Launch

1) Navigate to the backend project folder

2) Create virtual environment and install the dependencies:
```bash
make venv
make configure
```

3) Create db and implement migrations:
```bash
make db
make migrate
```

4) Run the app
```bash
make run
```

## API Endpoints
The full list of endpoints can be found in auto-generated doc:
- For self-hosted api: ```localhost:8000/docs```

## Metrics

### Local run (backend + metrics stack)

From `interviewer_backend/`:

1) Build backend image:
```bash
docker build -t csus_backend:local .
```

2) Create Docker network:
```bash
docker network create web || true
```

3) Run backend container with metrics enabled:
```bash
docker rm -f csus_backend || true
docker run \
  --detach \
  --restart unless-stopped \
  --network web \
  --publish 8000:80 \
  --env DB_DSN='postgresql://postgres@host.docker.internal:5432/postgres' \
  --env ROOT_PATH='' \
  --env TWELVE_LABS_API_KEYS='your_TL_API_key' \
  --env METRICS_ENABLED='true' \
  --label logging='promtail' \
  --label job='interviewer_backend' \
  --name csus_backend \
  csus_backend:local
```
If `host.docker.internal` is unavailable on your Linux host, set `DB_DSN` to a database container on the same `web` network.

4) Run observability containers:
```bash
docker rm -f interviewer_prometheus interviewer_loki interviewer_promtail interviewer_grafana || true

docker run \
  --detach \
  --restart unless-stopped \
  --network web \
  --publish 9090:9090 \
  --volume "$(pwd)/observability/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  --volume interviewer_prometheus_data:/prometheus \
  --name interviewer_prometheus \
  prom/prometheus:latest \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.enable-lifecycle

docker run \
  --detach \
  --restart unless-stopped \
  --network web \
  --publish 3100:3100 \
  --volume "$(pwd)/observability/loki/loki-config.yml:/etc/loki/config.yml:ro" \
  --volume interviewer_loki_data:/loki \
  --name interviewer_loki \
  grafana/loki:2.9.8 \
  -config.file=/etc/loki/config.yml

docker run \
  --detach \
  --restart unless-stopped \
  --network web \
  --volume "$(pwd)/observability/promtail/promtail-config.yml:/etc/promtail/config.yml:ro" \
  --volume /var/log:/var/log:ro \
  --volume /var/lib/docker/containers:/var/lib/docker/containers:ro \
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \
  --name interviewer_promtail \
  grafana/promtail:3.6.7 \
  -config.file=/etc/promtail/config.yml

docker run \
  --detach \
  --restart unless-stopped \
  --network web \
  --publish 3000:3000 \
  --env GF_SECURITY_ADMIN_USER='admin' \
  --env GF_SECURITY_ADMIN_PASSWORD='admin' \
  --env GF_USERS_ALLOW_SIGN_UP='false' \
  --volume "$(pwd)/observability/grafana/provisioning/datasources/datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro" \
  --volume "$(pwd)/observability/grafana/provisioning/dashboards/dashboards.yml:/etc/grafana/provisioning/dashboards/dashboards.yml:ro" \
  --volume "$(pwd)/observability/grafana/dashboards:/etc/grafana/dashboards:ro" \
  --volume interviewer_grafana_data:/var/lib/grafana \
  --name interviewer_grafana \
  grafana/grafana:latest
```

Access:
- Backend docs: `http://localhost:8000/docs`
- Backend metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (`admin` / `admin`)

The provisioned dashboard **Backend Observability** includes:
- API request latency (p95)
- 5xx error rate
- webhook failure rate
- background task duration (p95)
- TwelveLabs external API failure rate
- main API container logs (`csus_backend`)


### Server run (CI/CD)

`METRICS_ENABLED` is deploy-time controlled:
- default: `true`
- set repo/environment variable `METRICS_ENABLED=false` to disable `/metrics`

Grafana is configured for subpath hosting on the API domain:
- default: `https://api.jobless.live/grafana/`
- override with repo/environment variable `GRAFANA_ROOT_URL` if your server URL is different

Grafana is configured for subpath hosting on the API domain:
- default: `https://api.jobless.live/grafana/`
- override with repo/environment variable `GRAFANA_ROOT_URL` if your server URL is different


To stop local observability containers:
```bash
docker rm -f csus_backend interviewer_prometheus interviewer_loki interviewer_promtail interviewer_grafana
```
