import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: string;
  nickname: string;
  role: 'admin' | 'advanced' | 'normal' | 'readonly';
  permissions: string[];
  avatar?: string;
}

interface LoginContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
  hasPermission: (permission: string) => boolean;
}

const LoginContext = createContext<LoginContextType>({
  user: null,
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
  hasPermission: () => false,
});

export const useLogin = () => {
  return useContext(LoginContext);
};

export const LoginProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // 模拟从localStorage获取用户信息
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      setIsAuthenticated(true);
    }
  }, []);

  const login = (userData: User) => {
    setUser(userData);
    setIsAuthenticated(true);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
  };

  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    
    // 超级管理员拥有所有权限
    if (user.role === 'admin' || user.permissions.includes('*')) {
      return true;
    }
    
    // 检查具体权限
    return user.permissions.includes(permission);
  };

  return (
    <LoginContext.Provider value={{
      user,
      isAuthenticated,
      login,
      logout,
      hasPermission,
    }}>
      {children}
    </LoginContext.Provider>
  );
};

export default LoginContext;