FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies and Playwright
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install playwright
RUN playwright install chromium
RUN playwright install-deps

# Set up environment variables using secrets
RUN --mount=type=secret,id=OPENAI_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=OPENAI_ORGANIZATION_ID,mode=0444,required=true \
    --mount=type=secret,id=HF_API_KEY,mode=0444,required=true \
    --mount=type=secret,id=GOOGLE_API_KEY,mode=0444,required=true \
    echo "export OPENAI_API_KEY=$(cat /run/secrets/OPENAI_API_KEY)" >> /etc/profile && \
    echo "export OPENAI_ORGANIZATION_ID=$(cat /run/secrets/OPENAI_ORGANIZATION_ID)" >> /etc/profile && \
    echo "export HF_API_KEY=$(cat /run/secrets/HF_API_KEY)" >> /etc/profile && \
    echo "export GOOGLE_API_KEY=$(cat /run/secrets/GOOGLE_API_KEY)" >> /etc/profile

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Make sure the Playwright browser binaries are accessible
RUN mkdir -p /home/user/.cache && \
    cp -r /root/.cache/ms-playwright /home/user/.cache/ && \
    chmod -R 777 /home/user/.cache/ms-playwright

# Set other environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=$HOME/app \
    PYTHONUNBUFFERED=1 \
    GRADIO_ALLOW_FLAGGING=never \
    GRADIO_NUM_PORTS=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_THEME=huggingface \
    SYSTEM=spaces \
    USER_AGENT="MyApp/1.0"

# Switch to the "user" user
USER user

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# Source the profile to ensure environment variables are available
CMD ["/bin/bash", "-c", "source /etc/profile && python app.py"]