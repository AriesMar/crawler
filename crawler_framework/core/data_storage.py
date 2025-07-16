"""
数据存储管理器
Data storage manager for the crawler framework
"""

import json
import os
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from ..config import Config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class DataStorage:
    """数据存储管理器"""
    
    def __init__(self, storage_type: str = 'json'):
        self.storage_type = storage_type
        self._setup_storage()
    
    def _setup_storage(self):
        """设置存储方式"""
        if self.storage_type == 'sqlite':
            self.engine = create_engine(Config.DATABASE_URL)
            self.Session = sessionmaker(bind=self.engine)
        elif self.storage_type == 'mongodb':
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.MONGO_DB]
        elif self.storage_type == 'json':
            os.makedirs('data', exist_ok=True)
        elif self.storage_type == 'csv':
            os.makedirs('data', exist_ok=True)
    
    def save(self, data: Dict[str, Any], collection: str = 'default') -> bool:
        """保存数据"""
        try:
            if self.storage_type == 'json':
                return self._save_json(data, collection)
            elif self.storage_type == 'csv':
                return self._save_csv(data, collection)
            elif self.storage_type == 'sqlite':
                return self._save_sqlite(data, collection)
            elif self.storage_type == 'mongodb':
                return self._save_mongodb(data, collection)
            else:
                logger.error(f"不支持的存储类型: {self.storage_type}")
                return False
        except Exception as e:
            logger.error(f"保存数据失败: {str(e)}")
            return False
    
    def save_batch(self, data_list: List[Dict[str, Any]], collection: str = 'default') -> bool:
        """批量保存数据"""
        try:
            if self.storage_type == 'json':
                return self._save_json_batch(data_list, collection)
            elif self.storage_type == 'csv':
                return self._save_csv_batch(data_list, collection)
            elif self.storage_type == 'sqlite':
                return self._save_sqlite_batch(data_list, collection)
            elif self.storage_type == 'mongodb':
                return self._save_mongodb_batch(data_list, collection)
            else:
                logger.error(f"不支持的存储类型: {self.storage_type}")
                return False
        except Exception as e:
            logger.error(f"批量保存数据失败: {str(e)}")
            return False
    
    def _save_json(self, data: Dict[str, Any], collection: str) -> bool:
        """保存为JSON文件"""
        filename = f"data/{collection}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"数据已保存到: {filename}")
        return True
    
    def _save_json_batch(self, data_list: List[Dict[str, Any]], collection: str) -> bool:
        """批量保存为JSON文件"""
        filename = f"data/{collection}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        logger.info(f"批量数据已保存到: {filename}")
        return True
    
    def _save_csv(self, data: Dict[str, Any], collection: str) -> bool:
        """保存为CSV文件"""
        filename = f"data/{collection}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df = pd.DataFrame([data])
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"数据已保存到: {filename}")
        return True
    
    def _save_csv_batch(self, data_list: List[Dict[str, Any]], collection: str) -> bool:
        """批量保存为CSV文件"""
        filename = f"data/{collection}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df = pd.DataFrame(data_list)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logger.info(f"批量数据已保存到: {filename}")
        return True
    
    def _save_sqlite(self, data: Dict[str, Any], collection: str) -> bool:
        """保存到SQLite数据库"""
        session = self.Session()
        try:
            # 这里需要根据具体的数据结构创建表
            # 简化处理，直接插入到通用表
            table_name = f"table_{collection}"
            columns = ', '.join([f'"{k}" TEXT' for k in data.keys()])
            values = ', '.join(['?' for _ in data])
            
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns},
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            session.execute(text(create_table_sql))
            
            insert_sql = f"INSERT INTO {table_name} ({', '.join([f'"{k}"' for k in data.keys()])}) VALUES ({values})"
            session.execute(text(insert_sql), list(data.values()))
            session.commit()
            
            logger.info(f"数据已保存到SQLite表: {table_name}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"SQLite保存失败: {str(e)}")
            return False
        finally:
            session.close()
    
    def _save_sqlite_batch(self, data_list: List[Dict[str, Any]], collection: str) -> bool:
        """批量保存到SQLite数据库"""
        if not data_list:
            return True
        
        session = self.Session()
        try:
            table_name = f"table_{collection}"
            columns = ', '.join([f'"{k}" TEXT' for k in data_list[0].keys()])
            values = ', '.join(['?' for _ in data_list[0]])
            
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns},
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            session.execute(text(create_table_sql))
            
            insert_sql = f"INSERT INTO {table_name} ({', '.join([f'"{k}"' for k in data_list[0].keys()])}) VALUES ({values})"
            
            for data in data_list:
                session.execute(text(insert_sql), list(data.values()))
            
            session.commit()
            logger.info(f"批量数据已保存到SQLite表: {table_name}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"SQLite批量保存失败: {str(e)}")
            return False
        finally:
            session.close()
    
    def _save_mongodb(self, data: Dict[str, Any], collection: str) -> bool:
        """保存到MongoDB"""
        try:
            data['created_at'] = datetime.now()
            self.db[collection].insert_one(data)
            logger.info(f"数据已保存到MongoDB集合: {collection}")
            return True
        except Exception as e:
            logger.error(f"MongoDB保存失败: {str(e)}")
            return False
    
    def _save_mongodb_batch(self, data_list: List[Dict[str, Any]], collection: str) -> bool:
        """批量保存到MongoDB"""
        try:
            for data in data_list:
                data['created_at'] = datetime.now()
            
            self.db[collection].insert_many(data_list)
            logger.info(f"批量数据已保存到MongoDB集合: {collection}")
            return True
        except Exception as e:
            logger.error(f"MongoDB批量保存失败: {str(e)}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.storage_type == 'mongodb':
            self.client.close()
        elif self.storage_type == 'sqlite':
            self.engine.dispose() 