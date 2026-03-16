import type { Metadata } from "next";
import { ConfigProvider, App as AntdApp } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { Inter } from "next/font/google";
import "./globals.css";
import AppLayout from "@/components/Layout/AppLayout";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "DSP广告管理平台",
  description: "专业的DSP广告管理系统",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className={inter.className}>
        <ConfigProvider locale={zhCN}>
          <AntdApp>
            <AppLayout>
              {children}
            </AppLayout>
          </AntdApp>
        </ConfigProvider>
      </body>
    </html>
  );
}
