from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Bike(db.Model):
    __tablename__ = "bikes"

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(100), nullable=True)
    current_mileage = db.Column(db.Integer, nullable=False)

    maintenance_records = db.relationship(
        "MaintenanceRecord",
        backref="bike",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def display_name(self):
        if self.nickname:
            return f"{self.nickname} ({self.year} {self.make} {self.model})"
        return f"{self.year} {self.make} {self.model}"


class MaintenanceRecord(db.Model):
    __tablename__ = "maintenance_records"

    id = db.Column(db.Integer, primary_key=True)
    bike_id = db.Column(db.Integer, db.ForeignKey("bikes.id"), nullable=False)
    maintenance_type = db.Column(db.String(100), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    next_due_date = db.Column(db.Date, nullable=True)
    next_due_mileage = db.Column(db.Integer, nullable=True)

    def is_overdue(self, today=None):
        today = today or date.today()

        by_date = self.next_due_date is not None and today > self.next_due_date
        by_mileage = (
            self.next_due_mileage is not None
            and self.bike is not None
            and self.bike.current_mileage >= self.next_due_mileage
        )

        return by_date or by_mileage

    def is_due_soon(self, today=None, days_threshold=30, mileage_threshold=500):
        today = today or date.today()

        if self.is_overdue(today=today):
            return True

        due_by_date = (
            self.next_due_date is not None
            and 0 <= (self.next_due_date - today).days <= days_threshold
        )

        due_by_mileage = (
            self.next_due_mileage is not None
            and self.bike is not None
            and 0 <= (self.next_due_mileage - self.bike.current_mileage) <= mileage_threshold
        )

        return due_by_date or due_by_mileage