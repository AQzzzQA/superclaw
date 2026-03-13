import { Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';
import { UserService } from '../services/UserService';
import { Logger } from '../utils/Logger';

export class AuthController {
  private userService: UserService;
  private logger: Logger;

  constructor() {
    this.userService = new UserService();
    this.logger = new Logger('AuthController');
  }

  // Login with QQ number
  async login(req: Request, res: Response): Promise<void> {
    try {
      const { qq_number, password } = req.body;
      
      if (!qq_number) {
        res.status(400).json({
          success: false,
          error: 'QQ number is required'
        });
        return;
      }

      // Find user by QQ number
      const user = await this.userService.getUserByQQNumber(qq_number);
      
      if (!user) {
        // Create new user if not exists (auto-registration)
        const newUser = await this.userService.createUser({
          id: uuidv4(),
          qq_number,
          nickname: `User_${qq_number}`,
          role: 'user',
          permissions: JSON.stringify(['read'])
        });
        
        const token = this.generateToken(newUser);
        
        res.json({
          success: true,
          message: 'User created and logged in successfully',
          data: {
            token,
            user: {
              id: newUser.id,
              qq_number: newUser.qq_number,
              nickname: newUser.nickname,
              role: newUser.role,
              permissions: JSON.parse(newUser.permissions)
            }
          }
        });
      } else {
        // User exists, generate token
        const token = this.generateToken(user);
        
        res.json({
          success: true,
          message: 'Login successful',
          data: {
            token,
            user: {
              id: user.id,
              qq_number: user.qq_number,
              nickname: user.nickname,
              role: user.role,
              permissions: JSON.parse(user.permissions)
            }
          }
        });
      }
    } catch (error) {
      this.logger.error('Error in login:', error);
      res.status(500).json({
        success: false,
        error: 'Login failed'
      });
    }
  }

  // Get current user info from token
  async getCurrentUser(req: Request, res: Response): Promise<void> {
    try {
      const token = req.headers.authorization?.replace('Bearer ', '');
      
      if (!token) {
        res.status(401).json({
          success: false,
          error: 'No token provided'
        });
        return;
      }

      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key') as any;
      const user = await this.userService.getUserById(decoded.userId);
      
      if (!user) {
        res.status(404).json({
          success: false,
          error: 'User not found'
        });
        return;
      }

      res.json({
        success: true,
        data: {
          id: user.id,
          qq_number: user.qq_number,
          nickname: user.nickname,
          role: user.role,
          permissions: JSON.parse(user.permissions),
          created_at: user.created_at,
          updated_at: user.updated_at
        }
      });
    } catch (error) {
      this.logger.error('Error getting current user:', error);
      res.status(401).json({
        success: false,
        error: 'Invalid token'
      });
    }
  }

  // Update user profile
  async updateProfile(req: Request, res: Response): Promise<void> {
    try {
      const token = req.headers.authorization?.replace('Bearer ', '');
      
      if (!token) {
        res.status(401).json({
          success: false,
          error: 'No token provided'
        });
        return;
      }

      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key') as any;
      const { nickname, avatar_url, role, permissions } = req.body;
      
      const updateData: any = {};
      if (nickname) updateData.nickname = nickname;
      if (avatar_url) updateData.avatar_url = avatar_url;
      if (role) updateData.role = role;
      if (permissions) updateData.permissions = JSON.stringify(permissions);
      
      const updatedUser = await this.userService.updateUser(decoded.userId, updateData);
      
      if (!updatedUser) {
        res.status(404).json({
          success: false,
          error: 'User not found'
        });
        return;
      }

      res.json({
        success: true,
        data: {
          id: updatedUser.id,
          qq_number: updatedUser.qq_number,
          nickname: updatedUser.nickname,
          role: updatedUser.role,
          permissions: JSON.parse(updatedUser.permissions),
          updated_at: updatedUser.updated_at
        },
        message: 'Profile updated successfully'
      });
    } catch (error) {
      this.logger.error('Error updating profile:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to update profile'
      });
    }
  }

  // Generate JWT token
  private generateToken(user: any): string {
    const payload = {
      userId: user.id,
      qq_number: user.qq_number,
      role: user.role
    };
    
    return jwt.sign(payload, process.env.JWT_SECRET || 'your-secret-key', {
      expiresIn: process.env.JWT_EXPIRES_IN || '7d'
    });
  }
}