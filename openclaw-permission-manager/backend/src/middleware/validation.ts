import { Request, Response, NextFunction } from 'express';
import Joi from 'joi';

export const validateRequest = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const { error } = schema.validate(req.body);
    
    if (error) {
      res.status(400).json({
        success: false,
        error: 'Validation error',
        details: error.details
      });
      return;
    }
    
    next();
  };
};

// User validation schemas
export const userCreateSchema = Joi.object({
  qq_number: Joi.string().required().min(1).max(20),
  nickname: Joi.string().required().min(1).max(50),
  avatar_url: Joi.string().uri().optional(),
  role: Joi.string().valid('admin', 'user', 'readonly').default('user'),
  permissions: Joi.array().items(Joi.string()).default(['read'])
});

export const userUpdateSchema = Joi.object({
  nickname: Joi.string().min(1).max(50).optional(),
  avatar_url: Joi.string().uri().optional(),
  role: Joi.string().valid('admin', 'user', 'readonly').optional(),
  permissions: Joi.array().items(Joi.string()).optional()
});

// Template validation schemas
export const templateCreateSchema = Joi.object({
  name: Joi.string().required().min(1).max(50),
  description: Joi.string().max(200).optional(),
  permissions: Joi.array().items(Joi.string()).min(1).required(),
  is_system: Joi.boolean().default(false),
  created_by: Joi.string().optional()
});

export const templateUpdateSchema = Joi.object({
  name: Joi.string().min(1).max(50).optional(),
  description: Joi.string().max(200).optional(),
  permissions: Joi.array().items(Joi.string()).min(1).optional(),
  is_system: Joi.boolean().optional(),
  created_by: Joi.string().optional()
});

// Config validation schemas
export const configCreateSchema = Joi.object({
  config_name: Joi.string().required().min(1).max(100),
  config_data: Joi.object().required(),
  created_by: Joi.string().optional()
});

export const configUpdateSchema = Joi.object({
  config_name: Joi.string().min(1).max(100).optional(),
  config_data: Joi.object().optional(),
  created_by: Joi.string().optional()
});

// Login validation schema
export const loginSchema = Joi.object({
  qq_number: Joi.string().required().min(1).max(20),
  password: Joi.string().optional().max(100)
});