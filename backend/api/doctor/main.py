from datetime import timedelta, date
from typing import Union

from fastapi import APIRouter, Depends, Query, Body
from sqlmodel import Session, select

from api.functions import *
from api.models import *
from api.database import get_db
from api.security import credentials_exception
from api.schemas import *


doctor_router = APIRouter()

# To be developed further, functionality could be split into multiple files in this new directory. Like CRUD separate from more complicated actions.
# To use this router in more files just import it, and use as usual.


@doctor_router.get("/appointments", tags=["doctor"], response_model=List[AppointmentWithPatient])
def get_my_appointments(
                        start_date: Optional[date] = Query(None, description="Start date of the range"),
                        end_date: Optional[date] = Query(None, description="End date of the range"),
                        appointment_status: Optional[Union[AppointmentStatus, str]] = Query(None, description="Status of the queried appointments"),

                        db: Session = Depends(get_db),
                        payload: dict = Depends(get_my_info)
                        ):
    """
        Retrieve a list of appointments filtered by a date range and status.

        - **start_date**: The start date of the range. Defaults to today if not provided.
        - **end_date**: The end date of the range. Defaults to today + 3 months if not provided.
        - **appointment_status**: The status of the queried appointments. Defaults to Scheduled if not provided. If set to "Any" this returns all entries.
.

        ### Example Request
        ```http
        GET doctor/appointments/?start_date=2024-01-01&end_date=2024-10-31&appointment_status=Scheduled
        ```

        ### Example Response
        ```json
        [
          {
            "date": "2024-12-10T10:00:00",
            "reason": "Reason for appointment",
            "diagnosis": "Diagnosis",
            "status": "Scheduled",
            "patient": {
              "first_name": "PatientFirstName10",
              "middle_name": "PatientMiddleName0",
              "last_name": "PatientLastName10",
              "gender": "M"
            }
          },
          {
            "date": "2024-12-20T10:00:00",
            "reason": "Reason for appointment",
            "diagnosis": "Diagnosis",
            "status": "Scheduled",
            "patient": {
              "first_name": "PatientFirstName20",
              "middle_name": "PatientMiddleName0",
              "last_name": "PatientLastName20",
              "gender": "M"
            }
          }
        ]
        ```
        """


    if not payload or payload["type"] != "Doctor":
        raise credentials_exception

    today = date.today()

    start_date = start_date or today
    end_date = end_date or (today + timedelta(days=90))  # 3 months ago
    appointment_status = appointment_status or AppointmentStatus.SCHEDULED


    query = select(Appointment)
    query = query.where(Appointment.doctor_id == payload["doctor"].id )
    query = query.where(Appointment.date >= start_date)
    query = query.where(Appointment.date <= end_date)
    if appointment_status != "Any":
        query = query.where(Appointment.status == appointment_status)

    appointments = db.exec(query).fetchall()

    output = appointments


    for appointment in output:
        appointment.patient = appointment.patient

    return output


