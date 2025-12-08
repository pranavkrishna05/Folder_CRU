# Advanced Node.js Backend Structure

This backend is structured for scalability and maintainability using **Node.js**, **Express**, and **MongoDB**.

## 📂 Folder Overview
- `src/config` → DB connection & environment configuration
- `src/controllers` → Handle HTTP requests
- `src/models` → MongoDB models (Mongoose)
- `src/routes` → API routes
- `src/services` → Business logic
- `src/middleware` → Middleware (auth, errorHandlers)
- `src/utils` → Helper functions
- `src/validations` → Schema validation

## 🚀 Setup
```bash
npm install
npm run dev
```

## 🧠 Notes
- Add new modules as separate folders under `src/`
- Keep business logic separated from request handling
