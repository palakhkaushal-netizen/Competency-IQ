from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .auth import require_government_admin, require_student
from .config import settings
from .db import database_is_available, get_db
from .models import Assessment, SkillGap, StudentSkill, User

app = FastAPI(title="CompetencyIQ API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"api": "healthy", "database": "healthy" if database_is_available() else "unconfigured"}


@app.get("/api/auth/me")
def auth_me(user: User = Depends(require_student)) -> dict:
    return {"id": str(user.id), "email": user.email, "full_name": user.full_name, "role": user.role}


@app.get("/api/analytics/student")
def student_analytics(user: User = Depends(require_student), db: Session = Depends(get_db)) -> dict:
    skill_rows = db.execute(
        select(StudentSkill.skill_name, func.avg(StudentSkill.competency_score))
        .where(StudentSkill.student_id == user.id)
        .group_by(StudentSkill.skill_name)
    ).all()
    gap_count = db.scalar(
        select(func.count(SkillGap.id)).where(
            SkillGap.student_id == user.id,
            SkillGap.severity.in_(["CRITICAL", "HIGH"]),
        )
    ) or 0
    assessment_count = db.scalar(select(func.count(Assessment.id)).where(Assessment.student_id == user.id)) or 0
    skills = [{"name": name, "score": round(float(score), 1)} for name, score in skill_rows]
    readiness = round(sum(item["score"] for item in skills) / len(skills), 1) if skills else None
    return {
        "live_data": bool(assessment_count),
        "overall_readiness": readiness,
        "assessed_skills": len(skills),
        "critical_gaps": gap_count,
        "skills": skills,
        "message": None if assessment_count else "No live data available yet. Complete an assessment to begin.",
    }


@app.get("/api/government/overview")
def government_overview(_: User = Depends(require_government_admin), db: Session = Depends(get_db)) -> dict:
    students = db.scalar(select(func.count(func.distinct(Assessment.student_id)))) or 0
    assessments = db.scalar(select(func.count(Assessment.id))) or 0
    return {"live_data": bool(assessments), "student_responses": assessments, "students_assessed": students, "message": None if assessments else "No live data available yet."}


@app.exception_handler(RuntimeError)
def runtime_error_handler(_: Request, __: RuntimeError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"success": False, "message": "Service configuration is incomplete", "error_code": "SERVICE_UNCONFIGURED"})
