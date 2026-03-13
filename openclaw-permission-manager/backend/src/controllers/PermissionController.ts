import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { PermissionTemplate, PermissionTemplateCreate, PermissionTemplateUpdate, OpenClawConfig, OpenClawConfigCreate, OpenClawConfigUpdate } from '../models/Permission';
import { PermissionService } from '../services/PermissionService';
import { Logger } from '../utils/Logger';

export class PermissionController {
  private permissionService: PermissionService;
  private logger: Logger;

  constructor() {
    this.permissionService = new PermissionService();
    this.logger = new Logger('PermissionController');
  }

  // Permission Templates
  async getAllTemplates(req: Request, res: Response): Promise<void> {
    try {
      const templates = await this.permissionService.getAllTemplates();
      const response = templates.map(template => ({
        ...template,
        permissions: JSON.parse(template.permissions)
      }));
      
      res.json({
        success: true,
        data: response,
        count: templates.length
      });
    } catch (error) {
      this.logger.error('Error getting all templates:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get templates'
      });
    }
  }

  async getTemplateById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const template = await this.permissionService.getTemplateById(id);
      
      if (!template) {
        res.status(404).json({
          success: false,
          error: 'Template not found'
        });
        return;
      }

      const response = {
        ...template,
        permissions: JSON.parse(template.permissions)
      };

      res.json({
        success: true,
        data: response
      });
    } catch (error) {
      this.logger.error('Error getting template by ID:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get template'
      });
    }
  }

  async createTemplate(req: Request, res: Response): Promise<void> {
    try {
      const templateData: PermissionTemplateCreate = req.body;
      const templateId = uuidv4();
      
      const template = await this.permissionService.createTemplate({
        ...templateData,
        id: templateId,
        is_system: templateData.is_system || false
      });

      const response = {
        ...template,
        permissions: JSON.parse(template.permissions)
      };

      res.status(201).json({
        success: true,
        data: response,
        message: 'Template created successfully'
      });
    } catch (error) {
      this.logger.error('Error creating template:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to create template'
      });
    }
  }

  async updateTemplate(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const updateData: PermissionTemplateUpdate = req.body;
      
      const template = await this.permissionService.updateTemplate(id, updateData);

      if (!template) {
        res.status(404).json({
          success: false,
          error: 'Template not found'
        });
        return;
      }

      const response = {
        ...template,
        permissions: JSON.parse(template.permissions)
      };

      res.json({
        success: true,
        data: response,
        message: 'Template updated successfully'
      });
    } catch (error) {
      this.logger.error('Error updating template:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to update template'
      });
    }
  }

  async deleteTemplate(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const deleted = await this.permissionService.deleteTemplate(id);
      
      if (!deleted) {
        res.status(404).json({
          success: false,
          error: 'Template not found'
        });
        return;
      }

      res.json({
        success: true,
        message: 'Template deleted successfully'
      });
    } catch (error) {
      this.logger.error('Error deleting template:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to delete template'
      });
    }
  }

  // OpenClaw Config
  async getAllConfigs(req: Request, res: Response): Promise<void> {
    try {
      const configs = await this.permissionService.getAllConfigs();
      const response = configs.map(config => ({
        ...config,
        config_data: JSON.parse(config.config_data)
      }));
      
      res.json({
        success: true,
        data: response,
        count: configs.length
      });
    } catch (error) {
      this.logger.error('Error getting all configs:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get configs'
      });
    }
  }

  async getConfigById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const config = await this.permissionService.getConfigById(id);
      
      if (!config) {
        res.status(404).json({
          success: false,
          error: 'Config not found'
        });
        return;
      }

      const response = {
        ...config,
        config_data: JSON.parse(config.config_data)
      };

      res.json({
        success: true,
        data: response
      });
    } catch (error) {
      this.logger.error('Error getting config by ID:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get config'
      });
    }
  }

  async createConfig(req: Request, res: Response): Promise<void> {
    try {
      const configData: OpenClawConfigCreate = req.body;
      const configId = uuidv4();
      
      const config = await this.permissionService.createConfig({
        ...configData,
        id: configId,
        version: 1
      });

      const response = {
        ...config,
        config_data: JSON.parse(config.config_data)
      };

      res.status(201).json({
        success: true,
        data: response,
        message: 'Config created successfully'
      });
    } catch (error) {
      this.logger.error('Error creating config:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to create config'
      });
    }
  }

  async updateConfig(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const updateData: OpenClawConfigUpdate = req.body;
      
      const config = await this.permissionService.updateConfig(id, updateData);

      if (!config) {
        res.status(404).json({
          success: false,
          error: 'Config not found'
        });
        return;
      }

      const response = {
        ...config,
        config_data: JSON.parse(config.config_data)
      };

      res.json({
        success: true,
        data: response,
        message: 'Config updated successfully'
      });
    } catch (error) {
      this.logger.error('Error updating config:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to update config'
      });
    }
  }

  async deleteConfig(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const deleted = await this.permissionService.deleteConfig(id);
      
      if (!deleted) {
        res.status(404).json({
          success: false,
          error: 'Config not found'
        });
        return;
      }

      res.json({
        success: true,
        message: 'Config deleted successfully'
      });
    } catch (error) {
      this.logger.error('Error deleting config:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to delete config'
      });
    }
  }

  // Generate openclaw.json format config
  async generateOpenClawConfig(req: Request, res: Response): Promise<void> {
    try {
      const { userId } = req.params;
      
      const config = await this.permissionService.generateOpenClawConfig(userId);
      
      res.json({
        success: true,
        data: config,
        message: 'OpenClaw config generated successfully'
      });
    } catch (error) {
      this.logger.error('Error generating OpenClaw config:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to generate config'
      });
    }
  }
}