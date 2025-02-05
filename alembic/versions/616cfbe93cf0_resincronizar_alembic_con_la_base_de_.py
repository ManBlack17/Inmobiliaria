"""Resincronizar Alembic con la base de datos

Revision ID: 616cfbe93cf0
Revises: 
Create Date: 2025-02-02 02:15:34.223165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '616cfbe93cf0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA_NAME = "inmobiliaria"

def upgrade():
    """Agregar la columna usuario_id a puntos_interes sin afectar otras tablas."""
    op.add_column(
        "puntos_interes",
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey(f"{SCHEMA_NAME}.usuarios.id")),
        schema=SCHEMA_NAME
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    """Eliminar la columna usuario_id si es necesario hacer rollback."""
    op.drop_column("puntos_interes", "usuario_id", schema=SCHEMA_NAME)
    # ### end Alembic commands ###
