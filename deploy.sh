# Deploy Crawler
func_deployCrawler(){
    echo "Start Deploy Crawler";
    git pull
    docker-compose down
    docker-compose build
    docker system prune -f
    docker-compose up -d
}

func_buildCrawlerLocal(){
    docker-compose down
    docker-compose build
    docker system prune -f
    docker-compose up -d
}

# Deploy Heroku
func_deployHeroku(){
    git push heroku master:master
}

# Deploy Heroku staging
func_deployHerokuStage(){
    git push heroku-staging master:master
}

# Deploy Heroku production
func_deployHerokuProduction(){
    git push heroku-prod master:master
}


func_initData(){
    python init_database.py
    python init_redis.py
}

# Main
if [[ "$1" == "crawl" ]]; then
    echo "Deploy crawler"
    func_deployCrawler;

elif [[ "$1" == "local" ]]; then
    echo "Build crawler locally"
    func_buildCrawlerLocal

elif [[ "$1" == "stage" ]]; then
    echo "Deploy app to Heroku cpblbot-stage"
    func_deployHerokuStage

elif [[ "$1" == "prod" ]]; then
    echo "Deploy app to Heroku cpblbot-prod"
    func_deployHerokuProduction

elif [[ "$1" == "data" ]]; then
    echo  "Initialize database and redis"
    func_initData

else
#    echo "Not specify action. Deploy Crawler" >&2
    echo "Not specify action. Deploy Crawler"
fi
