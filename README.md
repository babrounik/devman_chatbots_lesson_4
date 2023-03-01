# Telegram and VK bots with quizes

This scripts allows you to run your own telegram and VK bots with questions and answers.

## Download project

```
git clone https://github.com/babrounik/devman_chatbots_lesson_4.git
cd devman_chatbots_lesson_4
```

### Python interpreter

```
brew update & brew install pyenv
brew update && brew upgrade pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.zshrc
source ~/.zshrc
pyenv install 3.9.11
pyenv rehash
pyenv local 3.9.11
```

## Environment

```
pip3 install pipenv
pipenv shell $(which python3)
```

## Requirements

```
pipenv install -r requirements.txt
```

## Environment variables
You have to replace INSERT_YOUR_VALUE with your private credentials.
```
echo 'export TG_API_KEY=INSERT_YOUR_VALUE' >> ./.env
echo 'export VK_COM=INSERT_YOUR_VALUE' >> ./.env
echo 'export REDIS_HOST=INSERT_YOUR_VALUE' >> ./.env
echo 'export REDIS_PASSWORD=INSERT_YOUR_VALUE' >> ./.env
echo 'export REDIS_PORT=INSERT_YOUR_VALUE' >> ./.env
source ~/.zshrc
```

## Run
```
python3 main_tg.py
python3 main_vk.py
```


