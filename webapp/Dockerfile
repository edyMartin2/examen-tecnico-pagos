FROM node:20-alpine

WORKDIR /app

# Copia los archivos de configuración
COPY package*.json ./

# Instala dependencias
RUN npm install

# Copia el código fuente
COPY . .

# Expone el puerto por defecto de Vite
EXPOSE 5173

# Inicia el servidor de desarrollo, exponiendo a todos los hosts
CMD ["npm", "run", "dev", "--", "--host"]
