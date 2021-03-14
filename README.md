# Crypto Research

Historical crypto profitability and future modelling.

Start database:
* create empty folders:
  * `/home/marcin/mongodb/database`
  * `/home/marcin/mongodb/metabase_data`
* start docker compose file in `deployment/docker-compose.yaml`
* start jupyter with `scripts/run_jupyter.bash`

# VPN Test

Create `dotenv-vpn-test.env` with following content

```bash
VPN_USERNAME="myemail@gmail.com"
VPN_PASSWORD="mypassword"
VPN_NETWORK="10.42.0.0/24"
```

Start docker compose

```bash
docker-compose --env-file dotenv-vpn-test.env -f deployment/docker-compose-vpn-test.yaml up
```

Confirm nginx port fowarding works

```bash
http://localhost:8080
```

Attach another container (optional)

```bash
docker run -it --rm  --net=container:deployment_vpn_1 curlimages/curl ipinfo.io
```

Spin down docker compose

```bash
docker-compose -f deployment/docker-compose-vpn-test.yaml down
```

# TODO

* exact historical electricity cost
* look for cheaper electricity
* currency rates, at the moment:
  * historical data in USD only
  * electricity cost calculated GBP -> USD at today rate
* look into other coins
* look into why my righ digs at 90% compared to historical data plot?
