"""The DTOs the platform sends and the money formatting on the way out."""

from datetime import datetime

from refunds.models import TimeInterval, format_cents, utc


def test_an_interval_is_half_open_whole_minutes_and_timezone_aware(booking):
    interval = booking.interval
    assert interval.duration_minutes == 120
    assert interval.has_begun_by(interval.start)
    assert not interval.has_begun_by(utc(2026, 3, 10, 13, 59))
    assert interval.is_well_formed()
    assert not TimeInterval(datetime(2026, 3, 10, 14), datetime(2026, 3, 10, 16)).is_well_formed()


def test_a_booking_reads_back_its_room_organizer_and_price_as_booked(booking):
    assert booking.starts_at == utc(2026, 3, 10, 14, 0)
    assert booking.department == "Statistics"
    assert booking.describe() == "bk-2291 in Gates 4301 for Dana Alvarez"
    assert booking.price_summary() == "$120.00 as booked for 120 minutes"
    assert format_cents(75) == "$0.75"
    assert format_cents(-250) == "-$2.50"
