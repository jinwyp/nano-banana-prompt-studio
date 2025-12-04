"""AI API 配置管理"""
import yaml
from pathlib import Path
from utils.resource_path import get_resource_path


class AIConfigManager:
    """管理AI API配置的保存和加载"""
    
    DEFAULT_CONFIG = {
        "base_url": "https://api.openai.com/v1",
        "api_key": "",
        "model": "gpt-4o-mini",
        "gemini_base_url": "",
        "gemini_api_key": "",
        "gemini_model": "gemini-3-pro-image-preview",
    }
    
    def __init__(self):
        self.config_path = get_resource_path("config/ai_config.yaml")
        self._ensure_config_exists()
    
    def _ensure_config_exists(self):
        """确保配置文件目录存在"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> dict:
        """加载AI配置"""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data:
                        # 合并默认配置，确保所有字段都存在
                        return {**self.DEFAULT_CONFIG, **data}
        except Exception as e:
            print(f"加载AI配置失败: {e}")
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: dict, merge_existing: bool = True) -> bool:
        """保存AI配置，默认保留已有字段"""
        try:
            data_to_save = {}
            if merge_existing and self.config_path.exists():
                with open(self.config_path, "r", encoding="utf-8") as f:
                    existing = yaml.safe_load(f) or {}
                    if isinstance(existing, dict):
                        data_to_save.update(existing)
            data_to_save.update(config)

            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    data_to_save,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                )
            return True
        except Exception as e:
            print(f"保存AI配置失败: {e}")
            return False
    
    def is_configured(self) -> bool:
        """检查是否已配置API"""
        config = self.load_config()
        return bool(config.get("api_key"))
    
    def get_base_url(self) -> str:
        return self.load_config().get("base_url", self.DEFAULT_CONFIG["base_url"])
    
    def get_api_key(self) -> str:
        return self.load_config().get("api_key", "")
    
    def get_model(self) -> str:
        return self.load_config().get("model", self.DEFAULT_CONFIG["model"])

    def get_gemini_config(self) -> dict:
        config = self.load_config()
        return {
            "base_url": config.get("gemini_base_url", self.DEFAULT_CONFIG["gemini_base_url"]),
            "api_key": config.get("gemini_api_key", self.DEFAULT_CONFIG["gemini_api_key"]),
            "model": config.get("gemini_model", self.DEFAULT_CONFIG["gemini_model"]),
        }

    def get_gemini_base_url(self) -> str:
        return self.get_gemini_config().get("base_url", "")

    def get_gemini_api_key(self) -> str:
        return self.get_gemini_config().get("api_key", "")

    def get_gemini_model(self) -> str:
        return self.get_gemini_config().get("model", self.DEFAULT_CONFIG["gemini_model"])

