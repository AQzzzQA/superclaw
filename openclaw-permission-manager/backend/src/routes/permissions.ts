import { Router } from 'express';
import { PermissionController } from '../controllers/PermissionController';
import { authMiddleware } from '../middleware/auth';
import { roleMiddleware } from '../middleware/role';

const router = Router();
const permissionController = new PermissionController();

// All routes require authentication
router.use(authMiddleware);

// Permission Templates (admin only)
router.get('/templates', permissionController.getAllTemplates.bind(permissionController));
router.get('/templates/:id', permissionController.getTemplateById.bind(permissionController));
router.post('/templates', roleMiddleware(['admin']), permissionController.createTemplate.bind(permissionController));
router.put('/templates/:id', roleMiddleware(['admin']), permissionController.updateTemplate.bind(permissionController));
router.delete('/templates/:id', roleMiddleware(['admin']), permissionController.deleteTemplate.bind(permissionController));

// OpenClaw Config (admin only)
router.get('/configs', permissionController.getAllConfigs.bind(permissionController));
router.get('/configs/:id', permissionController.getConfigById.bind(permissionController));
router.post('/configs', roleMiddleware(['admin']), permissionController.createConfig.bind(permissionController));
router.put('/configs/:id', roleMiddleware(['admin']), permissionController.updateConfig.bind(permissionController));
router.delete('/configs/:id', roleMiddleware(['admin']), permissionController.deleteConfig.bind(permissionController));

// Generate openclaw.json config
router.get('/generate/:userId', permissionController.generateOpenClawConfig.bind(permissionController));

export default router;