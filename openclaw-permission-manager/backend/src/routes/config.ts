import { Router } from 'express';
import { PermissionController } from '../controllers/PermissionController';
import { authMiddleware } from '../middleware/auth';
import { roleMiddleware } from '../middleware/role';

const router = Router();
const permissionController = new PermissionController();

// All routes require authentication
router.use(authMiddleware);

// OpenClaw Config routes
router.get('/', permissionController.getAllConfigs.bind(permissionController));
router.get('/:id', permissionController.getConfigById.bind(permissionController));
router.post('/', roleMiddleware(['admin']), permissionController.createConfig.bind(permissionController));
router.put('/:id', roleMiddleware(['admin']), permissionController.updateConfig.bind(permissionController));
router.delete('/:id', roleMiddleware(['admin']), permissionController.deleteConfig.bind(permissionController));
router.get('/generate/:userId', permissionController.generateOpenClawConfig.bind(permissionController));

export default router;