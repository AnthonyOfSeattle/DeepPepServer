# DeepPepServer

A REST api endpoint to serve models for peptide properties.

### Deploying the application

First, clone the repository into a logical spot on the computer you want to run on.
```
git clone https://github.com/AnthonyOfSeattle/DeepPepServer.git
cd DeepPepServer
```

A  `docker-compose.template.yml` file can be found in the `deploy/` directory and should be all that you need to get the application started.
Here is the recommended series of commands

```
cd deploy

# Copy and edit the compose files
cp docker-compose.template.yml docker-compose.yml
vim docker-compose.yml

# Copy and edit environmental variables
cp .env.template .env
vim .env

# Build and deploy
docker compose build
docker compose up -d
```

Likely the only thing that you will want to change in the `docker-compose.yml` file is what port the server is listening on from the hosting computer.
I usually run it listening on port `8000` and so have the following line as default in the docker compose file.

```
ports:
  - "8000:80"
```

Assuming you also have the server running on port `8000`, the most consistent way to check if the server is running is to ask one of the default
models to give you predictions. Let's get some retention times using this curl command.

```
curl -X 'POST' \
  'http://localhost:8000/models/standard_rt/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "peptides": [
    {
      "sequence": "PEPTIDEK"
    }
  ]
}'
```

You can also go to `http://localhost:8000/docs/` if you are on a computer with an internet browser and see the documents page.
Most endpoints are still a work in progress though.

If you look at the line `http://localhost:8000/models/standard_rt/predict` above, you will see the name `standard_rt`.
This is the model name, and there are 4 different models that come pre-loaded into the server.

```
standard_rt
phopho_rt
standard_charge
phospho_charge
```

### Getting more models

I own a [second repository](https://github.com/AnthonyOfSeattle/PhosphopediaModels) with models which are designed to be used with the Phosphopedia database.
These models can be added into the server with the following actions

```
mkdir models
cd models
git clone https://github.com/AnthonyOfSeattle/PhosphopediaModels.git

cd ../
cd deploy
vim docker.compose.yml
```

Make sure the docker compose file looks something like this

```
version: "3.9"

services:

  app:
    build: ../
    env_file: .env
    deploy:
      restart_policy:
        max_attempts: 5
        window: 30s
    ports:
      - "8000:80"
    volumes:
      - './models/PhosphopediaModels/production:/models'
```

You will likely need to restart to get things working.

```
docker compose down
docker compose up -d
```

Then you can hit one of the new models

```
curl -X 'POST' \
  'http://localhost:8000/models/human_phosphopedia_rt/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "peptides": [
    {
      "sequence": "PEPTIDEK"
    }
  ]
}'
```
