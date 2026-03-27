from datetime import date, datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Bike, MaintenanceRecord


# def create_app():
#     app = Flask(__name__)
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maintenance.db"
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["SECRET_KEY"] = "dev-secret-key"

#     db.init_app(app)

#     with app.app_context():
#         db.create_all()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maintenance.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        bikes = Bike.query.order_by(Bike.make.asc(), Bike.model.asc()).all()
        records = MaintenanceRecord.query.order_by(MaintenanceRecord.service_date.desc()).all()

        today = date.today()
        due_soon_records = []

        for record in records:
            if record.is_due_soon(today=today):
                due_soon_records.append(record)

        return render_template(
            "index.html",
            bikes=bikes,
            records=records,
            due_soon_records=due_soon_records,
            today=today,
        )

    @app.route("/bikes")
    def bikes():
        all_bikes = Bike.query.order_by(Bike.make.asc(), Bike.model.asc()).all()
        return render_template("bikes.html", bikes=all_bikes)

    @app.route("/bikes/add", methods=["GET", "POST"])
    def add_bike():
        if request.method == "POST":
            make = request.form.get("make", "").strip()
            model = request.form.get("model", "").strip()
            year = request.form.get("year", "").strip()
            nickname = request.form.get("nickname", "").strip()
            current_mileage = request.form.get("current_mileage", "").strip()

            if not make or not model or not year or not current_mileage:
                flash("Make, model, year, and current mileage are required.", "error")
                return render_template("add_bike.html")

            try:
                year = int(year)
                current_mileage = int(current_mileage)
            except ValueError:
                flash("Year and current mileage must be numbers.", "error")
                return render_template("add_bike.html")

            bike = Bike(
                make=make,
                model=model,
                year=year,
                nickname=nickname,
                current_mileage=current_mileage,
            )
            db.session.add(bike)
            db.session.commit()

            flash("Bike added successfully.", "success")
            return redirect(url_for("bikes"))

        return render_template("add_bike.html")

    @app.route("/bikes/<int:bike_id>/edit", methods=["GET", "POST"])
    def edit_bike(bike_id):
        bike = Bike.query.get_or_404(bike_id)

        if request.method == "POST":
            make = request.form.get("make", "").strip()
            model = request.form.get("model", "").strip()
            year = request.form.get("year", "").strip()
            nickname = request.form.get("nickname", "").strip()
            current_mileage = request.form.get("current_mileage", "").strip()

            if not make or not model or not year or not current_mileage:
                flash("Make, model, year, and current mileage are required.", "error")
                return render_template("edit_bike.html", bike=bike)

            try:
                bike.year = int(year)
                bike.current_mileage = int(current_mileage)
            except ValueError:
                flash("Year and current mileage must be numbers.", "error")
                return render_template("edit_bike.html", bike=bike)

            bike.make = make
            bike.model = model
            bike.nickname = nickname

            db.session.commit()
            flash("Bike updated successfully.", "success")
            return redirect(url_for("bikes"))

        return render_template("edit_bike.html", bike=bike)

    @app.route("/bikes/<int:bike_id>/delete", methods=["POST"])
    def delete_bike(bike_id):
        bike = Bike.query.get_or_404(bike_id)
        db.session.delete(bike)
        db.session.commit()
        flash("Bike deleted successfully.", "success")
        return redirect(url_for("bikes"))

    @app.route("/records")
    def records():
        bike_id = request.args.get("bike_id", type=int)
        maintenance_type = request.args.get("maintenance_type", "").strip()

        query = MaintenanceRecord.query

        if bike_id:
            query = query.filter_by(bike_id=bike_id)

        if maintenance_type:
            query = query.filter(MaintenanceRecord.maintenance_type.ilike(f"%{maintenance_type}%"))

        all_records = query.order_by(MaintenanceRecord.service_date.desc()).all()
        bikes = Bike.query.order_by(Bike.make.asc(), Bike.model.asc()).all()

        return render_template(
            "records.html",
            records=all_records,
            bikes=bikes,
            selected_bike_id=bike_id,
            selected_maintenance_type=maintenance_type,
        )

    @app.route("/records/add", methods=["GET", "POST"])
    def add_record():
        bikes = Bike.query.order_by(Bike.make.asc(), Bike.model.asc()).all()

        if not bikes:
            flash("Add a bike before adding maintenance records.", "error")
            return redirect(url_for("add_bike"))

        if request.method == "POST":
            bike_id = request.form.get("bike_id", "").strip()
            maintenance_type = request.form.get("maintenance_type", "").strip()
            service_date_str = request.form.get("service_date", "").strip()
            mileage = request.form.get("mileage", "").strip()
            cost = request.form.get("cost", "").strip()
            notes = request.form.get("notes", "").strip()
            next_due_date_str = request.form.get("next_due_date", "").strip()
            next_due_mileage = request.form.get("next_due_mileage", "").strip()

            if not bike_id or not maintenance_type or not service_date_str or not mileage:
                flash("Bike, maintenance type, service date, and mileage are required.", "error")
                return render_template("add_record.html", bikes=bikes)

            try:
                bike_id = int(bike_id)
                mileage = int(mileage)
                cost_value = float(cost) if cost else None
                next_due_mileage_value = int(next_due_mileage) if next_due_mileage else None
                service_date_value = datetime.strptime(service_date_str, "%Y-%m-%d").date()
                next_due_date_value = (
                    datetime.strptime(next_due_date_str, "%Y-%m-%d").date()
                    if next_due_date_str else None
                )
            except ValueError:
                flash("Please enter valid numeric and date values.", "error")
                return render_template("add_record.html", bikes=bikes)

            record = MaintenanceRecord(
                bike_id=bike_id,
                maintenance_type=maintenance_type,
                service_date=service_date_value,
                mileage=mileage,
                cost=cost_value,
                notes=notes,
                next_due_date=next_due_date_value,
                next_due_mileage=next_due_mileage_value,
            )

            db.session.add(record)
            db.session.commit()

            flash("Maintenance record added successfully.", "success")
            return redirect(url_for("records"))

        return render_template("add_record.html", bikes=bikes)

    @app.route("/records/<int:record_id>/edit", methods=["GET", "POST"])
    def edit_record(record_id):
        record = MaintenanceRecord.query.get_or_404(record_id)
        bikes = Bike.query.order_by(Bike.make.asc(), Bike.model.asc()).all()

        if request.method == "POST":
            bike_id = request.form.get("bike_id", "").strip()
            maintenance_type = request.form.get("maintenance_type", "").strip()
            service_date_str = request.form.get("service_date", "").strip()
            mileage = request.form.get("mileage", "").strip()
            cost = request.form.get("cost", "").strip()
            notes = request.form.get("notes", "").strip()
            next_due_date_str = request.form.get("next_due_date", "").strip()
            next_due_mileage = request.form.get("next_due_mileage", "").strip()

            if not bike_id or not maintenance_type or not service_date_str or not mileage:
                flash("Bike, maintenance type, service date, and mileage are required.", "error")
                return render_template("edit_record.html", record=record, bikes=bikes)

            try:
                record.bike_id = int(bike_id)
                record.mileage = int(mileage)
                record.cost = float(cost) if cost else None
                record.next_due_mileage = int(next_due_mileage) if next_due_mileage else None
                record.service_date = datetime.strptime(service_date_str, "%Y-%m-%d").date()
                record.next_due_date = (
                    datetime.strptime(next_due_date_str, "%Y-%m-%d").date()
                    if next_due_date_str else None
                )
            except ValueError:
                flash("Please enter valid numeric and date values.", "error")
                return render_template("edit_record.html", record=record, bikes=bikes)

            record.maintenance_type = maintenance_type
            record.notes = notes

            db.session.commit()
            flash("Maintenance record updated successfully.", "success")
            return redirect(url_for("records"))

        return render_template("edit_record.html", record=record, bikes=bikes)

    @app.route("/records/<int:record_id>/delete", methods=["POST"])
    def delete_record(record_id):
        record = MaintenanceRecord.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        flash("Maintenance record deleted successfully.", "success")
        return redirect(url_for("records"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)