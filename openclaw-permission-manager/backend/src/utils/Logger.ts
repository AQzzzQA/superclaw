export class Logger {
  private context: string;

  constructor(context: string) {
    this.context = context;
  }

  log(message: string, data?: any): void {
    console.log(`[${new Date().toISOString()}] [${this.context}] [LOG] ${message}`, data || '');
  }

  error(message: string, error?: any): void {
    console.error(`[${new Date().toISOString()}] [${this.context}] [ERROR] ${message}`, error || '');
  }

  warn(message: string, data?: any): void {
    console.warn(`[${new Date().toISOString()}] [${this.context}] [WARN] ${message}`, data || '');
  }

  info(message: string, data?: any): void {
    console.info(`[${new Date().toISOString()}] [${this.context}] [INFO] ${message}`, data || '');
  }
}