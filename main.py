from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from config import APP_NAME, APP_VERSION, FRONTEND_ORIGINS
from database import (
    create_tables,
    delete_project,
    get_project,
    list_projects,
    save_project,
)
from export_service import build_brand_pdf
from models import BuildRequest, ImproveRequest
from workflow import improve_project, run_workflow


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()


@app.get("/")
def root():
    return {
        "status": "online",
        "product": APP_NAME,
        "version": APP_VERSION,
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.post("/api/build-brand")
def build_brand(request: BuildRequest):
    try:
        project = run_workflow(request.profile.model_dump())
        project_id = save_project(project)
        project["project_id"] = project_id
        return project
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/improve-brand")
def improve_brand(request: ImproveRequest):
    try:
        project = improve_project(request.project)
        project_id = save_project(project)
        project["project_id"] = project_id
        return project
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/projects")
def projects():
    return {"projects": list_projects()}


@app.get("/api/projects/{project_id}")
def project(project_id: int):
    result = get_project(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@app.delete("/api/projects/{project_id}")
def remove_project(project_id: int):
    if not delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True}


@app.post("/api/projects/{project_id}/export.pdf")
def export_project_pdf(project_id: int):
    project = get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    pdf = build_brand_pdf(project)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="brandforge-{project_id}.pdf"'
        },
    )
