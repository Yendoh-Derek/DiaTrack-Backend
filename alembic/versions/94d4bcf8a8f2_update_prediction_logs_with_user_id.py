"""update_prediction_logs_with_user_id

Revision ID: 94d4bcf8a8f2
Revises: 
Create Date: 2025-05-21 22:03:59.046787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94d4bcf8a8f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Import SQLAlchemy
    from sqlalchemy import inspect
    
    # Get inspector
    conn = op.get_bind()
    inspector = inspect(conn)
    existing_tables = inspector.get_table_names()

    # Create users table if it doesn't exist
    if 'users' not in existing_tables:
        op.create_table(
            'users',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('username', sa.String(), nullable=True),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('hashed_password', sa.String(), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Handle prediction_logs table
    if 'prediction_logs' in existing_tables:
        # Check if user_id column exists
        columns = [col['name'] for col in inspector.get_columns('prediction_logs')]
        if 'user_id' not in columns:
            op.add_column('prediction_logs',
                sa.Column('user_id', sa.UUID(), nullable=True))
            op.create_foreign_key(
                'fk_prediction_user',
                'prediction_logs', 'users',
                ['user_id'], ['id']
            )
    else:
        # Create prediction_logs table
        op.create_table(
            'prediction_logs',
            sa.Column('prediction_id', sa.UUID(), nullable=False),
            sa.Column('prediction_time', sa.DateTime(), nullable=True),
            sa.Column('risk_score', sa.Float(), nullable=False),
            sa.Column('feature_input', sa.JSON(), nullable=False),
            sa.Column('shap_values', sa.JSON(), nullable=False),
            sa.Column('recommendation', sa.String(), nullable=True),
            sa.Column('user_id', sa.UUID(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_prediction_user'),
            sa.PrimaryKeyConstraint('prediction_id')
        )


def downgrade() -> None:
    """Downgrade schema."""
    # First drop the foreign key if it exists
    try:
        op.drop_constraint('fk_prediction_user', 'prediction_logs', type_='foreignkey')
    except:
        pass  # Constraint might not exist

    # Then try to drop the user_id column if it exists
    try:
        op.drop_column('prediction_logs', 'user_id')
    except:
        pass  # Column might not exist
