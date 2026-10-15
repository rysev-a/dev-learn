import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // API_URL — другой адрес бэкенда (например, для проверки на копии базы)
      "/api": process.env.API_URL || "http://localhost:8000",
    },
  },
});
