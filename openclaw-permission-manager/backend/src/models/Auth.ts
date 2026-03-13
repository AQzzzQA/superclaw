export interface UserCredentials {
  qq_number: string;
  password?: string;
}

export interface AuthResponse {
  token: string;
  user: {
    id: string;
    qq_number: string;
    nickname: string;
    role: string;
    permissions: string[];
  };
}

export interface LoginResponse extends AuthResponse {
  message: string;
}

export interface RegisterResponse {
  message: string;
  user: {
    id: string;
    qq_number: string;
    nickname: string;
    role: string;
  };
}