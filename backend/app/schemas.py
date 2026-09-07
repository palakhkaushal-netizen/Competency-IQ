from pydantic import BaseModel, Field


class AssessmentAnswer(BaseModel):
    skill_name: str = Field(min_length=1, max_length=120)
    score: float = Field(ge=0, le=100)


class AssessmentSubmission(BaseModel):
    answers: list[AssessmentAnswer] = Field(min_length=1)
