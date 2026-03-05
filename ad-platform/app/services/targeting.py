"""
定向投放业务逻辑服务
"""
import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.targeting import (
    AudienceTargeting,
    DeviceTargeting,
    GeoTargeting,
    TimeTargeting,
    EnvironmentTargeting
)
from app.schemas.targeting import (
    AudienceTargetingCreate,
    AudienceTargetingUpdate,
    DeviceTargetingCreate,
    DeviceTargetingUpdate,
    GeoTargetingCreate,
    GeoTargetingUpdate,
    TimeTargetingCreate,
    TimeTargetingUpdate,
    EnvironmentTargetingCreate,
    EnvironmentTargetingUpdate
)
from app.core.exceptions import ValidationError, NotFoundError


class AudienceTargetingService:
    """人群定向服务"""

    @staticmethod
    def create(db: Session, obj_in: AudienceTargetingCreate, tenant_id: int) -> AudienceTargeting:
        """创建人群定向"""
        try:
            # 将 JSON 对象转换为字符串存储
            targeting_value_json = json.dumps(obj_in.targeting_value, ensure_ascii=False)

            db_obj = AudienceTargeting(
                campaign_id=obj_in.campaign_id,
                tenant_id=tenant_id,
                targeting_type=obj_in.targeting_type,
                targeting_value=targeting_value_json,
                is_include=obj_in.is_include
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建人群定向失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[AudienceTargeting]:
        """获取单个人群定向"""
        return db.query(AudienceTargeting).filter(
            and_(
                AudienceTargeting.id == id,
                AudienceTargeting.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AudienceTargeting]:
        """获取人群定向列表"""
        query = db.query(AudienceTargeting).filter(
            AudienceTargeting.tenant_id == tenant_id
        )

        if campaign_id:
            query = query.filter(AudienceTargeting.campaign_id == campaign_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: AudienceTargeting,
        obj_in: AudienceTargetingUpdate
    ) -> AudienceTargeting:
        """更新人群定向"""
        try:
            update_data = obj_in.dict(exclude_unset=True)

            # 如果更新了 targeting_value，需要转换为 JSON 字符串
            if 'targeting_value' in update_data:
                update_data['targeting_value'] = json.dumps(
                    update_data['targeting_value'],
                    ensure_ascii=False
                )

            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新人群定向失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除人群定向"""
        db_obj = AudienceTargetingService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("人群定向不存在")

        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除人群定向失败: {str(e)}")


class DeviceTargetingService:
    """设备定向服务"""

    @staticmethod
    def create(db: Session, obj_in: DeviceTargetingCreate, tenant_id: int) -> DeviceTargeting:
        """创建设备定向"""
        try:
            db_obj = DeviceTargeting(
                campaign_id=obj_in.campaign_id,
                tenant_id=tenant_id,
                **obj_in.dict(exclude={'campaign_id'})
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建设备定向失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[DeviceTargeting]:
        """获取单个设备定向"""
        return db.query(DeviceTargeting).filter(
            and_(
                DeviceTargeting.id == id,
                DeviceTargeting.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[DeviceTargeting]:
        """获取设备定向列表"""
        query = db.query(DeviceTargeting).filter(
            DeviceTargeting.tenant_id == tenant_id
        )

        if campaign_id:
            query = query.filter(DeviceTargeting.campaign_id == campaign_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: DeviceTargeting,
        obj_in: DeviceTargetingUpdate
    ) -> DeviceTargeting:
        """更新设备定向"""
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新设备定向失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除设备定向"""
        db_obj = DeviceTargetingService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("设备定向不存在")

        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除设备定向失败: {str(e)}")


class GeoTargetingService:
    """地域定向服务"""

    @staticmethod
    def create(db: Session, obj_in: GeoTargetingCreate, tenant_id: int) -> GeoTargeting:
        """创建地域定向"""
        try:
            # 将地域列表转换为 JSON 字符串存储
            geo_list_json = json.dumps(obj_in.geo_list, ensure_ascii=False)

            db_obj = GeoTargeting(
                campaign_id=obj_in.campaign_id,
                tenant_id=tenant_id,
                targeting_type=obj_in.targeting_type,
                geo_level=obj_in.geo_level,
                geo_list=geo_list_json,
                is_exclude=obj_in.is_exclude,
                latitude=obj_in.latitude,
                longitude=obj_in.longitude,
                radius=obj_in.radius
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建地域定向失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[GeoTargeting]:
        """获取单个地域定向"""
        return db.query(GeoTargeting).filter(
            and_(
                GeoTargeting.id == id,
                GeoTargeting.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[GeoTargeting]:
        """获取地域定向列表"""
        query = db.query(GeoTargeting).filter(
            GeoTargeting.tenant_id == tenant_id
        )

        if campaign_id:
            query = query.filter(GeoTargeting.campaign_id == campaign_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: GeoTargeting,
        obj_in: GeoTargetingUpdate
    ) -> GeoTargeting:
        """更新地域定向"""
        try:
            update_data = obj_in.dict(exclude_unset=True)

            # 如果更新了 geo_list，需要转换为 JSON 字符串
            if 'geo_list' in update_data:
                update_data['geo_list'] = json.dumps(
                    update_data['geo_list'],
                    ensure_ascii=False
                )

            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新地域定向失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除地域定向"""
        db_obj = GeoTargetingService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("地域定向不存在")

        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除地域定向失败: {str(e)}")


class TimeTargetingService:
    """时间定向服务"""

    @staticmethod
    def create(db: Session, obj_in: TimeTargetingCreate, tenant_id: int) -> TimeTargeting:
        """创建时间定向"""
        try:
            # 将时间配置转换为 JSON 字符串存储
            time_config_json = json.dumps(obj_in.time_config, ensure_ascii=False)

            db_obj = TimeTargeting(
                campaign_id=obj_in.campaign_id,
                tenant_id=tenant_id,
                targeting_type=obj_in.targeting_type,
                time_config=time_config_json,
                timezone=obj_in.timezone
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建时间定向失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[TimeTargeting]:
        """获取单个时间定向"""
        return db.query(TimeTargeting).filter(
            and_(
                TimeTargeting.id == id,
                TimeTargeting.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[TimeTargeting]:
        """获取时间定向列表"""
        query = db.query(TimeTargeting).filter(
            TimeTargeting.tenant_id == tenant_id
        )

        if campaign_id:
            query = query.filter(TimeTargeting.campaign_id == campaign_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: TimeTargeting,
        obj_in: TimeTargetingUpdate
    ) -> TimeTargeting:
        """更新时间定向"""
        try:
            update_data = obj_in.dict(exclude_unset=True)

            # 如果更新了 time_config，需要转换为 JSON 字符串
            if 'time_config' in update_data:
                update_data['time_config'] = json.dumps(
                    update_data['time_config'],
                    ensure_ascii=False
                )

            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新时间定向失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除时间定向"""
        db_obj = TimeTargetingService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("时间定向不存在")

        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除时间定向失败: {str(e)}")


class EnvironmentTargetingService:
    """环境定向服务"""

    @staticmethod
    def create(db: Session, obj_in: EnvironmentTargetingCreate, tenant_id: int) -> EnvironmentTargeting:
        """创建环境定向"""
        try:
            db_obj = EnvironmentTargeting(
                campaign_id=obj_in.campaign_id,
                tenant_id=tenant_id,
                **obj_in.dict(exclude={'campaign_id'})
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"创建环境定向失败: {str(e)}")

    @staticmethod
    def get(db: Session, id: int, tenant_id: int) -> Optional[EnvironmentTargeting]:
        """获取单个环境定向"""
        return db.query(EnvironmentTargeting).filter(
            and_(
                EnvironmentTargeting.id == id,
                EnvironmentTargeting.tenant_id == tenant_id
            )
        ).first()

    @staticmethod
    def get_multi(
        db: Session,
        tenant_id: int,
        campaign_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EnvironmentTargeting]:
        """获取环境定向列表"""
        query = db.query(EnvironmentTargeting).filter(
            EnvironmentTargeting.tenant_id == tenant_id
        )

        if campaign_id:
            query = query.filter(EnvironmentTargeting.campaign_id == campaign_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        db_obj: EnvironmentTargeting,
        obj_in: EnvironmentTargetingUpdate
    ) -> EnvironmentTargeting:
        """更新环境定向"""
        try:
            update_data = obj_in.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise ValidationError(f"更新环境定向失败: {str(e)}")

    @staticmethod
    def delete(db: Session, id: int, tenant_id: int) -> bool:
        """删除环境定向"""
        db_obj = EnvironmentTargetingService.get(db, id, tenant_id)
        if not db_obj:
            raise NotFoundError("环境定向不存在")

        try:
            db.delete(db_obj)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValidationError(f"删除环境定向失败: {str(e)}")
