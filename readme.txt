Create artifacts:
1. Download dataset from https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset and place all files in data.
2. Run the notebook experiments/train_pipeline.ipynb

This will create the neccessary files and models to run recommender system.


Build Images:

UI
docker build -t recomm-ui -f .\uiDockerfile\Dockerfile .

API
docker build -t recomm-api -f .\apiDockerfile\Dockerfile .

Run application
docker compose -f .\docker-compose.yml up --detach