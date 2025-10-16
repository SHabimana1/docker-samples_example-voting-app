# TAHAP 1: BUILDER
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install

# TAHAP 2: FINAL
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules /app/node_modules
COPY . .
CMD ["node", "server.js"]