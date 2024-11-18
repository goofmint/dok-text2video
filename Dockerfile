FROM nvidia/cuda:12.5.1-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージのインストール
# /appはアプリのディレクトリ、/opt/artifactはアウトプット先のディレクトリ
RUN apt-get update && \
    apt-get install -y \
        git \
        git-lfs \
        python3 \
        python3-pip \
	libgl1-mesa-glx \
	libgl1-mesa-dev \
	libglib2.0-0 \
      && \
    mkdir /app /opt/artifact && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# VALL-E Xのリポジトリをクローン
WORKDIR /app
# git-lfsのインストール
# 依存ライブラリのインストール
COPY * /app/
COPY annotator/ /app/annotator/
COPY __assets__/ /app/__assets__/
RUN pip install -r requirements.txt
# 出力データをオブジェクトストレージにアップロードするためのライブラリ
RUN pip cache purge

# 実行スクリプト（後で作成）
COPY runner.py /app/
# Dockerコンテナー起動時に実行するスクリプト（後で作成）
COPY docker-entrypoint.sh /
# 実行権限を付与
RUN chmod +x /docker-entrypoint.sh /

WORKDIR /
# Dockerコンテナー起動時に実行するスクリプトを指定して実行
CMD ["/bin/bash", "/docker-entrypoint.sh"]
