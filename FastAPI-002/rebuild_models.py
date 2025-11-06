"""
Script to rebuild Pydantic models and resolve forward references
"""

def rebuild_models():
    from schemas.category import CategoryResponse
    from schemas.product import ProductResponse
    
    # Rebuild models to resolve forward references
    CategoryResponse.model_rebuild()
    ProductResponse.model_rebuild()
    
    print("✅ Models rebuilt successfully!")

if __name__ == "__main__":
    rebuild_models()