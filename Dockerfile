FROM python:3.9-buster

# ファイルのマイグレーション
RUN mkdir /code
WORKDIR /code

# 必要なパッケージのインストール
RUN yes | curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        dialog openssh-server msodbcsql18 build-essential gcc unixodbc-dev \
    && echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc \
    && . ~/.bashrc \
    && dialog openssh-server

COPY ./requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN echo "${SSH_PASSWD}" | chpasswd
COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222

ENTRYPOINT ["/usr/local/bin/init.sh"]

