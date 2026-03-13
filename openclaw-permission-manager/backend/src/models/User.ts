export interface User {
  id: string;
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: string;
  permissions: string[];
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: string;
  permissions: string[];
}

export interface UserUpdate {
  nickname?: string;
  avatar_url?: string;
  role?: string;
  permissions?: string[];
}

export interface UserResponse {
  id: string;
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: string;
  permissions: string[];
  created_at: string;
  updated_at: string;
}