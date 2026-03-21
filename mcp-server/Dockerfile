FROM node:22-alpine

WORKDIR /app

# Install dependencies first (layer caching)
COPY package.json ./
RUN npm install --omit=dev

# Copy application code
COPY index.js ./

ENTRYPOINT ["node", "index.js"]
