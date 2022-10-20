from .example import example_bp

# 允许访问的API版本
VERSIONS_ALLOWED = ['example_api']

# API版本映射
API_VERSION_MAPPING = {
    'example_api': example_bp
}
