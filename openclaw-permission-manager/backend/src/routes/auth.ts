import { Router } from 'express';
import { AuthController } from '../controllers/AuthController';

const router = Router();
const authController = new AuthController();

// Login with QQ number
router.post('/login', authController.login.bind(authController));

// Get current user info
router.get('/me', authController.getCurrentUser.bind(authController));

// Update user profile
router.put('/profile', authController.updateProfile.bind(authController));

export default router;