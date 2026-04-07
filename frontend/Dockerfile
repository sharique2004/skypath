# ---- Stage 1: Build the React App ----
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source code and build the production bundle
COPY . .
RUN npm run build

# ---- Stage 2: Serve with nginx ----
FROM nginx:alpine

# Copy our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built React app from Stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
