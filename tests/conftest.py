"""Shared fixtures: one booking the platform sends us, and a request builder."""

import pytest

from refunds.models import BookingRecord, CancellationRequest, Organizer, Room, TimeInterval, utc

START = utc(2026, 3, 10, 14, 0)
END = utc(2026, 3, 10, 16, 0)


@pytest.fixture
def booking():
    return BookingRecord(
        booking_id="bk-2291",
        room=Room(code="4301", building="Gates", capacity=40),
        organizer=Organizer(organizer_id="u-118", name="Dana Alvarez", department="Statistics"),
        interval=TimeInterval(START, END),
        price_as_booked_cents=12000,
        booked_at=utc(2026, 2, 1, 9, 0),
    )


@pytest.fixture
def cancellation():
    def build(when, reason="", booking_id="bk-2291", requested_by="u-118"):
        return CancellationRequest(booking_id, when, requested_by, reason)

    return build
