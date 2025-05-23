"""Create tables

Revision ID: 24382d85abe1
Revises:
Create Date: 2025-05-10 09:16:03.372651

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "24382d85abe1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "file_resume",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_id", sa.Uuid(), nullable=False),
        sa.Column(
            "filename", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False
        ),
        sa.Column(
            "file_extension",
            sqlmodel.sql.sqltypes.AutoString(length=10),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_id"),
    )
    op.create_table(
        "ner_entity",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Uuid(), nullable=False),
        sa.Column("facts", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("entities", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["file_resume.file_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ner_entity_resume_id"), "ner_entity", ["resume_id"], unique=False
    )
    op.create_table(
        "ner_entity_selection",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Uuid(), nullable=False),
        sa.Column("entity", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("entity_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("researched", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["file_resume.file_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ner_entity_selection_resume_id"),
        "ner_entity_selection",
        ["resume_id"],
        unique=False,
    )
    op.create_table(
        "ner_entity_research",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("resume_id", sa.Uuid(), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("research", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["entity_id"], ["ner_entity_selection.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["file_resume.file_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("resume_id", "entity_id", name="uix_resume_id_entity_id"),
    )
    op.create_index(
        op.f("ix_ner_entity_research_resume_id"),
        "ner_entity_research",
        ["resume_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_ner_entity_research_resume_id"), table_name="ner_entity_research"
    )
    op.drop_table("ner_entity_research")
    op.drop_index(
        op.f("ix_ner_entity_selection_resume_id"), table_name="ner_entity_selection"
    )
    op.drop_table("ner_entity_selection")
    op.drop_index(op.f("ix_ner_entity_resume_id"), table_name="ner_entity")
    op.drop_table("ner_entity")
    op.drop_table("file_resume")
    # ### end Alembic commands ###
