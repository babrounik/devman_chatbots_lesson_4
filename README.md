# Telegram and VK bots with quizes

This scripts allows you to run your own telegram and VK bots with questions and answers.

## Prepare environment

Login into remote machine.

### Python interpreter

```
sudo apt update -y
sudo apt install build-essential
sudo apt install libssl-dev libffi-dev libncurses5-dev zlib1g zlib1g-dev libreadline-dev libbz2-dev libsqlite3-dev lzma liblzma-dev libbz2-dev make gcc
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $HOME/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $HOME/.bashrc
echo 'eval "$(pyenv init -)"' >> $HOME/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bashrc
source $HOME/.bashrc
pyenv install 3.9.16
# this operation can take a few minutes without any verbose log
pyenv global 3.9.16
```

### Download project

Note that you need to upload .env file and quiz-questions to the directory with the project.

```
cd /opt
git clone https://github.com/babrounik/devman_chatbots_lesson_4.git
cd devman_chatbots_lesson_4
```

### Environment

```
pip3 install pipenv
pipenv shell --python $(which python3.9)
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
source ~/.bashrc
```

### Processes demonization

```
cd /opt/devman_chatbots_lesson_4
pipenv shell
which python3.9
# copy path 
/root/.local/share/virtualenvs/devman_chatbots_lesson_4-kfTXzYwK/bin/python3.9
cd /etc/systemd/system
touch tg_bot.service
touch vk_bot.service

vim tg_bot.service
i
[Service]
ExecStart=YOU_PYTHON_PATH PY_FILE_PATH
Restart=always
Environment=TG_API_KEY=YOUR_TG_API_KEY
Environment=REDIS_HOST=YOUR_REDIS_HOST
Environment=REDIS_PASSWORD=YOUR_REDIS_PASSWORD
Environment=REDIS_PORT=YOUR_REDIS_PORT

[Install]
WantedBy=multi-user.target
:wq

systemctl enable tg_bot.service

vim tg_bot.service
i
[Service]
ExecStart=YOU_PYTHON_PATH PY_FILE_PATH
Restart=always
Environment=VK_COM=YOUR_VK_COM_API_KEY
Environment=REDIS_HOST=YOUR_REDIS_HOST
Environment=REDIS_PASSWORD=YOUR_REDIS_PASSWORD
Environment=REDIS_PORT=YOUR_REDIS_PORT

[Install]
WantedBy=multi-user.target
:wq

systemctl enable vk_bot.service
```

### Run

```
systemctl start tg_bot.service
systemctl start vk_bot.service
```

## Example

You may play with bot in telegram: https://t.me/dvmn_cb_lesson_3_bot
You may play with bot in vk.com: https://vk.com/public217898435
