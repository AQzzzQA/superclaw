"""
批量上传转化 API
"""
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException
import pandas as pd
import io

router = APIRouter()


class ConversionData(BaseModel):
    """转化数据"""
    click_id: str
    conversion_type: str
    conversion_time: str
    value: float = 0.0


class BatchUploadResult(BaseModel):
    """批量上传结果"""
    total: int
    success: int
    failed: int
    errors: List[str] = []


@router.post("/conversion/batch-upload")
async def batch_upload_conversion(file: UploadFile = File(...)):
    """批量上传转化数据"""
    if not file.filename.endswith(('.xlsx', '.csv')):
        raise BadRequestException("仅支持 xlsx 或 csv 格式")

    try:
        # 读取文件
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content), engine='openpyxl') if file.filename.endswith('.xlsx') else pd.read_csv(io.BytesIO(content))

        # 验证必需列
        required_columns = ['click_id', 'conversion_type', 'conversion_time']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise BadRequestException(f"缺少必需列: {', '.join(missing_columns)}")

        # 处理数据
        result = BatchUploadResult(
            total=len(df),
            success=0,
            failed=0,
            errors=[]
        )

        for index, row in df.iterrows():
            try:
                # 验证数据
                if not row['click_id']:
                    raise ValueError("click_id 不能为空")
                if not row['conversion_type']:
                    raise ValueError("conversion_type 不能为空")
                if not row['conversion_time']:
                    raise ValueError("conversion_time 不能为空")

                # 实际应保存到数据库
                result.success += 1

            except Exception as e:
                result.failed += 1
                result.errors.append(f"第 {index + 1} 行: {str(e)}")

        return APIResponse.success(
            data={
                "total": result.total,
                "success": result.success,
                "failed": result.failed,
                "errors": result.errors[:10]  # 只返回前10个错误
            },
            message=f"上传完成：成功 {result.success} 条，失败 {result.failed} 条"
        )

    except Exception as e:
        raise BadRequestException(f"文件处理失败: {str(e)}")


@router.post("/conversion/batch-create")
async def batch_create_conversions(data: List[ConversionData]):
    """批量创建转化"""
    if not data:
        raise BadRequestException("数据不能为空")

    result = BatchUploadResult(
        total=len(data),
        success=0,
        failed=0,
        errors=[]
    )

    for index, item in enumerate(data):
        try:
            # 验证数据
            if not item.click_id:
                raise ValueError("click_id 不能为空")
            if not item.conversion_type:
                raise ValueError("conversion_type 不能为空")
            if not item.conversion_time:
                raise ValueError("conversion_time 不能为空")

            # 实际应保存到数据库
            result.success += 1

        except Exception as e:
            result.failed += 1
            result.errors.append(f"第 {index + 1} 条: {str(e)}")

    return APIResponse.success(
        data={
            "total": result.total,
            "success": result.success,
            "failed": result.failed,
            "errors": result.errors
        },
        message=f"创建完成：成功 {result.success} 条，失败 {result.failed} 条"
    )
