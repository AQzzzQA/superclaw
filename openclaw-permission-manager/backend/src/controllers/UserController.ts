import { Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { User, UserCreate, UserUpdate, UserResponse } from '../models/User';
import { UserService } from '../services/UserService';
import { Logger } from '../utils/Logger';

export class UserController {
  private userService: UserService;
  private logger: Logger;

  constructor() {
    this.userService = new UserService();
    this.logger = new Logger('UserController');
  }

  // Get all users
  async getAllUsers(req: Request, res: Response): Promise<void> {
    try {
      const users = await this.userService.getAllUsers();
      const response: UserResponse[] = users.map(user => ({
        ...user,
        permissions: JSON.parse(user.permissions)
      }));
      
      res.json({
        success: true,
        data: response,
        count: users.length
      });
    } catch (error) {
      this.logger.error('Error getting all users:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get users'
      });
    }
  }

  // Get user by ID
  async getUserById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const user = await this.userService.getUserById(id);
      
      if (!user) {
        res.status(404).json({
          success: false,
          error: 'User not found'
        });
        return;
      }

      const response: UserResponse = {
        ...user,
        permissions: JSON.parse(user.permissions)
      };

      res.json({
        success: true,
        data: response
      });
    } catch (error) {
      this.logger.error('Error getting user by ID:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get user'
      });
    }
  }

  // Create user
  async createUser(req: Request, res: Response): Promise<void> {
    try {
      const userData: UserCreate = req.body;
      const userId = uuidv4();
      
      const user = await this.userService.createUser({
        ...userData,
        id: userId
      });

      const response: UserResponse = {
        ...user,
        permissions: JSON.parse(user.permissions)
      };

      res.status(201).json({
        success: true,
        data: response,
        message: 'User created successfully'
      });
    } catch (error) {
      this.logger.error('Error creating user:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to create user'
      });
    }
  }

  // Update user
  async updateUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const updateData: UserUpdate = req.body;
      
      const user = await this.userService.updateUser(id, updateData);

      if (!user) {
        res.status(404).json({
          success: false,
          error: 'User not found'
        });
        return;
      }

      const response: UserResponse = {
        ...user,
        permissions: JSON.parse(user.permissions)
      };

      res.json({
        success: true,
        data: response,
        message: 'User updated successfully'
      });
    } catch (error) {
      this.logger.error('Error updating user:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to update user'
      });
    }
  }

  // Delete user
  async deleteUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const deleted = await this.userService.deleteUser(id);
      
      if (!deleted) {
        res.status(404).json({
          success: false,
          error: 'User not found'
        });
        return;
      }

      res.json({
        success: true,
        message: 'User deleted successfully'
      });
    } catch (error) {
      this.logger.error('Error deleting user:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to delete user'
      });
    }
  }

  // Get user by QQ number
  async getUserByQQNumber(req: Request, res: Response): Promise<void> {
    try {
      const { qq_number } = req.params;
      const user = await this.userService.getUserByQQNumber(qq_number);
      
      if (!user) {
        res.status(404).json({
          success: false,
          error: 'User not found'
        });
        return;
      }

      const response: UserResponse = {
        ...user,
        permissions: JSON.parse(user.permissions)
      };

      res.json({
        success: true,
        data: response
      });
    } catch (error) {
      this.logger.error('Error getting user by QQ number:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get user'
      });
    }
  }
}