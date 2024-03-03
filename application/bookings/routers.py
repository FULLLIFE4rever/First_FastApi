from datetime import date

from fastapi import APIRouter, Depends

from bookings.schemes import SBooking
from tasks.tasks import send_confirm_email
from users.dependencies import get_current_user
from users.models import Users
from utils.exceptions import ConflictException

from .services import BookingsService

bookings_router = APIRouter(prefix="/booking", tags=["Booking"])


@bookings_router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[SBooking]:
    return await BookingsService.find_by_all(user_id=user.id)


@bookings_router.post("")
async def add_bookings(
    date_from: date,
    date_to: date,
    price: int,
    hotel_id: int,
    user: Users = Depends(get_current_user),
) -> None:
    if date_from >= date_to or date_from < date.today():
        raise ConflictException("Date from cannot be more then date to")
    booking = await BookingsService.add(
        date_from=date_from,
        date_to=date_to,
        price=price,
        user_id=user.id,
        hotel_id=hotel_id,
    )
    booking = SBooking.model_validate(booking["Bookings"]).model_dump()
    print("sending email")
    send_confirm_email.delay(booking, user.email)


@bookings_router.get("/expired")
async def get_expired_bookings(
    user: Users = Depends(get_current_user),
) -> list[SBooking]:
    return await BookingsService.find_by_all(user_id=user.id, before=True)


@bookings_router.delete("/{booking_id:int}")
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    return await BookingsService.delete(id=booking_id, user_id=user.id)
