import { User, UserCreate, UserUpdate } from '../models/User';
import { initDatabase, createTables } from '../config/database';
import { v4 as uuidv4 } from 'uuid';
import sqlite3 from 'sqlite3';
import path from 'path';

export class UserService {
  private db: sqlite3.Database;

  constructor() {
    this.db = new sqlite3.Database(path.join(__dirname, '../../data/permissions.db'));
  }

  // Initialize database tables
  async initializeDatabase(): Promise<void> {
    await initDatabase();
    await createTables();
  }

  // Get all users
  async getAllUsers(): Promise<User[]> {
    return new Promise((resolve, reject) => {
      this.db.all('SELECT * FROM users ORDER BY created_at DESC', (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  // Get user by ID
  async getUserById(id: string): Promise<User | null> {
    return new Promise((resolve, reject) => {
      this.db.get('SELECT * FROM users WHERE id = ?', [id], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row || null);
        }
      });
    });
  }

  // Get user by QQ number
  async getUserByQQNumber(qq_number: string): Promise<User | null> {
    return new Promise((resolve, reject) => {
      this.db.get('SELECT * FROM users WHERE qq_number = ?', [qq_number], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row || null);
        }
      });
    });
  }

  // Create user
  async createUser(userData: UserCreate): Promise<User> {
    return new Promise((resolve, reject) => {
      const id = uuidv4();
      const createdAt = new Date().toISOString();
      const updatedAt = createdAt;
      
      const sql = `
        INSERT INTO users (id, qq_number, nickname, avatar_url, role, permissions, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `;
      
      const params = [
        id,
        userData.qq_number,
        userData.nickname,
        userData.avatar_url || null,
        userData.role,
        JSON.stringify(userData.permissions),
        createdAt,
        updatedAt
      ];
      
      this.db.run(sql, params, function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({
            id,
            qq_number: userData.qq_number,
            nickname: userData.nickname,
            avatar_url: userData.avatar_url,
            role: userData.role,
            permissions: userData.permissions,
            created_at: createdAt,
            updated_at: updatedAt
          });
        }
      });
    });
  }

  // Update user
  async updateUser(id: string, updateData: UserUpdate): Promise<User | null> {
    return new Promise((resolve, reject) => {
      const fields = [];
      const values = [];
      const updatedAt = new Date().toISOString();
      
      if (updateData.nickname !== undefined) {
        fields.push('nickname = ?');
        values.push(updateData.nickname);
      }
      if (updateData.avatar_url !== undefined) {
        fields.push('avatar_url = ?');
        values.push(updateData.avatar_url);
      }
      if (updateData.role !== undefined) {
        fields.push('role = ?');
        values.push(updateData.role);
      }
      if (updateData.permissions !== undefined) {
        fields.push('permissions = ?');
        values.push(JSON.stringify(updateData.permissions));
      }
      
      if (fields.length === 0) {
        resolve(this.getUserById(id));
        return;
      }
      
      fields.push('updated_at = ?');
      values.push(updatedAt);
      values.push(id);
      
      const sql = `UPDATE users SET ${fields.join(', ')} WHERE id = ?`;
      
      this.db.run(sql, values, function(err) {
        if (err) {
          reject(err);
        } else {
          if (this.changes === 0) {
            resolve(null);
          } else {
            resolve(this.getUserById(id));
          }
        }
      });
    });
  }

  // Delete user
  async deleteUser(id: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      this.db.run('DELETE FROM users WHERE id = ?', [id], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes > 0);
        }
      });
    });
  }

  // Update user permissions
  async updatePermissions(id: string, permissions: string[]): Promise<User | null> {
    return this.updateUser(id, { permissions });
  }

  // Update user role
  async updateRole(id: string, role: string): Promise<User | null> {
    return this.updateUser(id, { role });
  }

  // Get users by role
  async getUsersByRole(role: string): Promise<User[]> {
    return new Promise((resolve, reject) => {
      this.db.all('SELECT * FROM users WHERE role = ?', [role], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  // Search users by nickname or QQ number
  async searchUsers(query: string): Promise<User[]> {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT * FROM users 
        WHERE nickname LIKE ? OR qq_number LIKE ?
        ORDER BY created_at DESC
      `;
      
      this.db.all(sql, [`%${query}%`, `%${query}%`], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }
}