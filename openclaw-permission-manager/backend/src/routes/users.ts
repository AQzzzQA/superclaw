import { Router } from 'express';
import { UserController } from '../controllers/UserController';
import { authMiddleware } from '../middleware/auth';

const router = Router();
const userController = new UserController();

// All routes require authentication
router.use(authMiddleware);

// Get all users
router.get('/', userController.getAllUsers.bind(userController));

// Get user by ID
router.get('/:id', userController.getUserById.bind(userController));

// Create user
router.post('/', userController.createUser.bind(userController));

// Update user
router.put('/:id', userController.updateUser.bind(userController));

// Delete user
router.delete('/:id', userController.deleteUser.bind(userController));

// Get user by QQ number
router.get('/qq/:qq_number', userController.getUserByQQNumber.bind(userController));

export default router;