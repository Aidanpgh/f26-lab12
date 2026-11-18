"""Data the CampusReserve platform sends this service, and what it gets back.

Time semantics match the platform: instants are timezone-aware UTC, intervals
are half-open ``[start, end)``, and durations are whole minutes. Money is whole
cents. The price on a booking is the price as booked, snapshotted by the
platform's billing module when the reservation was confirmed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = 24 * MINUTES_PER_HOUR


@dataclass(frozen=True)
class Room:
    """A bookable room, identified the way the campus directory identifies it."""

    code: str
    building: str
    capacity: int

    @property
    def label(self) -> str:
        return f"{self.building} {self.code}"


@dataclass(frozen=True)
class Organizer:
    """The person who holds the booking, plus the department that pays for it."""

    organizer_id: str
    name: str
    department: str


@dataclass(frozen=True)
class TimeInterval:
    """A half-open interval of instants: start is included, end is not."""

    start: datetime
    end: datetime

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds()) // 60

    def has_begun_by(self, moment: datetime) -> bool:
        return moment >= self.start

    def is_well_formed(self) -> bool:
        if self.start.tzinfo is None or self.end.tzinfo is None:
            return False
        return self.end > self.start


@dataclass(frozen=True)
class BookingRecord:
    """A confirmed booking, as the platform holds it at cancellation time."""

    booking_id: str
    room: Room
    organizer: Organizer
    interval: TimeInterval
    price_as_booked_cents: int
    booked_at: datetime

    @property
    def starts_at(self) -> datetime:
        return self.interval.start

    @property
    def department(self) -> str:
        return self.organizer.department

    def describe(self) -> str:
        return f"{self.booking_id} in {self.room.label} for {self.organizer.name}"

    def price_summary(self) -> str:
        price = format_cents(self.price_as_booked_cents)
        return f"{price} as booked for {self.interval.duration_minutes} minutes"


@dataclass(frozen=True)
class CancellationRequest:
    """A cancellation the platform has accepted and now wants priced."""

    booking_id: str
    requested_at: datetime
    requested_by: str
    reason: str = ""


@dataclass(frozen=True)
class RefundStatement:
    """What this service hands back: an amount, the rule behind it, the notes."""

    booking_id: str
    price_as_booked_cents: int
    refund_cents: int
    tier_name: str
    adjustments: tuple[str, ...]

    @property
    def withheld_cents(self) -> int:
        return self.price_as_booked_cents - self.refund_cents

    @property
    def is_full_refund(self) -> bool:
        return self.refund_cents == self.price_as_booked_cents


def utc(year, month, day, hour=0, minute=0):
    """Build a UTC instant on whole minutes."""
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def format_cents(amount):
    """Render whole cents the way the platform's statements render money."""
    sign = "-" if amount < 0 else ""
    dollars, cents = divmod(abs(amount), 100)
    return f"{sign}${dollars}.{cents:02d}"
