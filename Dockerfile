# 1. Imagem base com a versão do Python que você precisa
FROM python:3.13-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia os arquivos de dependências para o contêiner
COPY pyproject.toml uv.lock ./

# 4. Instala as dependências do sistema necessárias para o pyppeteer
RUN apt-get update && apt-get install -y \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    lsb-release \
    wget \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 5. Instala as dependências do Python
# (Usando o uv.lock para garantir as mesmas versões)
RUN pip install --no-cache-dir uv
RUN uv pip install --no-cache --system -e .

# 6. Copia o resto do código do seu projeto para o contêiner
COPY . .

# 7. Comando para rodar a aplicação quando o contêiner iniciar
CMD ["python", "-m", "src.main"]