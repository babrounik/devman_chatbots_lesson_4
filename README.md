# Telegram and VK bots with quizes

This scripts allows you to run your own telegram and VK bots with questions and answers.

## How to run local script

### Download project

```
git clone https://github.com/babrounik/devman_chatbots_lesson_4.git
cd devman_chatbots_lesson_4
```

### Python interpreter



```
sudo apt update -y
sudo apt install build-essential
sudo apt install libssl-dev libffi-dev libncurses5-dev zlib1g zlib1g-dev libreadline-dev libbz2-dev libsqlite3-dev lzma make gcc
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $HOME/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $HOME/.bashrc
echo 'eval "$(pyenv init -)"' >> $HOME/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bashrc
source $HOME/.bashrc
pyenv install 3.10.10
# this operation can take a few minutes without any verbose log
pyenv global 3.10.10
```

### Environment

```
cd /opt
git clone git@github.com:babrounik/devman_chatbots_lesson_4.git
cd /opt/devman_chatbots_lesson_4
pip3 install pipenv
pipenv shell --python $(which python3)
```

### Requirements

```
pipenv install -r requirements.txt
```

### Environment variables
You have to replace INSERT_YOUR_VALUE with your private credentials.
```
echo 'export TG_API_KEY=INSERT_YOUR_VALUE' >> ./.env
echo 'export VK_COM=INSERT_YOUR_VALUE' >> ./.env
echo 'export REDIS_HOST=INSERT_YOUR_VALUE' >> ./.env
echo 'export REDIS_PASSWORD=INSERT_YOUR_VALUE' >> ./.env
echo 'export REDIS_PORT=INSERT_YOUR_VALUE' >> ./.env
source ~/.zshrc
```

### Run
```
python3 main_tg.py
python3 main_vk.py
```

## How to deploy script to Heroku
* create an account on https://id.heroku.com and create you app APP_NAME
* create an account on https://github.com
* add this code to repository and commit & push it
* go to Settings => Buildpacks and choose python for your project
* create variables in Settings => Config Vars: "TG_API_KEY", "VK_COM", "REDIS_HOST", "REDIS_PASSWORD", "REDIS_PORT"
* go to Deploy tab and add your github repo to heroku account
* connect github to heroku and press "Deploy Brunch"
* then go to Resources section and run your Free Dyno via Edit & switch slider to ON state
* NOTE: you must have Procfile inside your project

