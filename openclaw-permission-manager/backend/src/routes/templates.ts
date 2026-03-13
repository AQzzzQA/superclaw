import { Router } from 'express';
import { PermissionController } from '../controllers/PermissionController';
import { authMiddleware } from '../middleware/auth';
import { roleMiddleware } from '../middleware/role';

const router = Router();
const permissionController = new PermissionController();

// All routes require authentication
router.use(authMiddleware);

// Permission Templates routes
router.get('/', permissionController.getAllTemplates.bind(permissionController));
router.get('/:id', permissionController.getTemplateById.bind(permissionController));
router.post('/', roleMiddleware(['admin']), permissionController.createTemplate.bind(permissionController));
router.put('/:id', roleMiddleware(['admin']), permissionController.updateTemplate.bind(permissionController));
router.delete('/:id', roleMiddleware(['admin']), permissionController.deleteTemplate.bind(permissionController));

export default router;