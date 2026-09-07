"""Create core CompetencyIQ tables.

Revision ID: 001_initial_core
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial_core"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_table(
        "student_assessments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_student_assessments_student_id", "student_assessments", ["student_id"], unique=False)
    op.create_table(
        "student_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("skill_name", sa.String(length=120), nullable=False),
        sa.Column("competency_score", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_student_skills_student_id", "student_skills", ["student_id"], unique=False)
    op.create_table(
        "skill_gaps",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("skill_name", sa.String(length=120), nullable=False),
        sa.Column("current_score", sa.Float(), nullable=False),
        sa.Column("target_score", sa.Float(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_skill_gaps_student_id", "skill_gaps", ["student_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_skill_gaps_student_id", table_name="skill_gaps")
    op.drop_table("skill_gaps")
    op.drop_index("ix_student_skills_student_id", table_name="student_skills")
    op.drop_table("student_skills")
    op.drop_index("ix_student_assessments_student_id", table_name="student_assessments")
    op.drop_table("student_assessments")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
