# GPU
FROM gcr.io/kaggle-gpu-images/python:latest 

# 環境変数の設定
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

SHELL ["/bin/bash", "-c"]

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    lsb-release \
    curl \
    wget \
    gnupg2 \
    software-properties-common \
    build-essential \
    cmake \
    git \
    libssl-dev \
    pkg-config \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Miniconda のインストール
WORKDIR /opt
RUN curl -sSLO "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    ./Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

# ユーザー情報を設定
ARG USER_NAME
ARG USER_ID
RUN useradd -m -s /bin/bash -u $USER_ID $USER_NAME && \
    echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ホストのフォルダにコピー
COPY --chown=takuya:takuya ./git_code /home/${USER_NAME}/git_code

# 権限を適切に設定
RUN chown -R $USER_NAME:$USER_NAME /home/$USER_NAME

# デフォルトのユーザー切り替え
USER $USER_NAME
WORKDIR /home/$USER_NAME

# Miniconda 環境変数
ENV PATH="/opt/miniconda/bin:$PATH"

RUN /opt/miniconda/bin/conda init bash

RUN source ~/.bashrc && \
    cd ~/git_code/PythonRobotics && \
    conda env create -f ./requirements/environment.yml

RUN source ~/.bashrc && \
    /opt/miniconda/bin/conda run -n python_robotics pip install gymnasium && \
    /opt/miniconda/bin/conda run -n python_robotics pip install highway-env && \
    /opt/miniconda/bin/conda run -n python_robotics pip install imitation
    

#======================================================#
CMD ["/bin/bash"]
