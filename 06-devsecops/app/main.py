"""VitaClin appointments API (fictitious).

Small service used as the target of the DevSecOps pipeline. It keeps data in
memory and never logs personal data, following data minimisation (LGPD art. 6, III).
"""

import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger("vitaclin")

app = FastAPI(title="VitaClin Appointments API", version="1.0.0", docs_url=None, redoc_url=None)


class AppointmentIn(BaseModel):
    patient_ref: str = Field(pattern=r"^P-[0-9]{6}$", description="Pseudonymised patient reference")
    clinic_id: int = Field(gt=0)
    starts_at: datetime


class Appointment(AppointmentIn):
    id: UUID


_appointments: dict[UUID, Appointment] = {}


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/appointments", status_code=201)
def create_appointment(data: AppointmentIn) -> Appointment:
    if data.starts_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=422, detail="Appointment must be in the future")
    appointment = Appointment(id=uuid4(), **data.model_dump())
    _appointments[appointment.id] = appointment
    # Log only the technical identifier, never the patient reference
    logger.info("appointment created id=%s", appointment.id)
    return appointment


@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: UUID) -> Appointment:
    appointment = _appointments.get(appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Not found")
    return appointment
