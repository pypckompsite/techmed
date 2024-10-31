from datetime import timedelta, date
from typing import Union

from fastapi import APIRouter, Depends, Query
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
        Retrieve a list of events filtered by a date range and optional parameters.

        - **start_date**: The start date of the range. Defaults to today if not provided.
        - **end_date**: The end date of the range. Defaults to today + 3 months if not provided.
        - **appointment_status**: The status of the queried appointments. Defaults to Scheduled if not provided. If set to "Any" this returns all entries.

        ### Responses
        - **200 OK**: A list of appointments for the currently logged in doctor.

        ### Example Request
        ```http
        GET doctor/appointments/?start_date=2024-01-01&end_date=2024-10-31&appointment_status=Scheduled
        ```

        ### Example Response
        ```json

        ```
        """


    if not payload or payload["type"] != "Doctor":
        raise credentials_exception

    # Default values for date filters
    today = date.today()
    start_date = start_date or today
    end_date = end_date or (today + timedelta(days=90))  # 3 months ago
    appointment_status = appointment_status or AppointmentStatus.SCHEDULED

    query = select(Appointment)
    query = query.where(Appointment.doctor_id == payload["doctor_id"] )
    query = query.where(Appointment.date >= start_date)
    query = query.where(Appointment.date <= end_date)
    if appointment_status != "Any":
        query = query.where(Appointment.status == appointment_status)

    appointments = db.exec(query).fetchall()

    output = appointments


    for appointment in output:
        appointment.patient = appointment.patient

    return output


