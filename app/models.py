from sqlalchemy import Column, Float, DateTime, JSON, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from database import Base
from sqlalchemy.orm import relationship

class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    prediction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_time = Column(DateTime, default=datetime.utcnow)
    risk_score = Column(Float, nullable=False)
    feature_input = Column(JSON, nullable=False)  # Stores input features
    shap_values = Column(JSON, nullable=False)    # Stores SHAP values
    recommendation = Column(String)               # Stores Gemini recommendation
    
    # Add relationship to User
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user = relationship("User", back_populates="predictions")

    def __repr__(self):
        return f"<PredictionLog(id={self.prediction_id}, risk_score={self.risk_score})>"