import express from 'express';

const router = express.Router();

// Import route modules here (e.g., userRoutes, authRoutes)
// router.use('/users', userRoutes);

router.get('/', (req, res) => {
  res.json({ message: 'API working!' });
});

export default router;