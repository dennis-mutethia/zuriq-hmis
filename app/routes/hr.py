from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import (
    Employee, Department, EmploymentType, IdType,
    PayrollParameterCategory, PayrollParameter, EmployeePayrollParameter,
    PayslipPeriod, Payslip, PayslipItem,
)
from app.routes.auth import admin_required

hr_bp = Blueprint("hr", __name__, url_prefix="/hr")


# ── Employees ────────────────────────────────────────────────────────────

@hr_bp.route("/")
@hr_bp.route("/employees")
@login_required
def list_employees():
    q = request.args.get("q", "").strip()
    query = Employee.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Employee.surname.ilike(like), Employee.other_names.ilike(like), Employee.staff_no.ilike(like)))
    employees = query.order_by(Employee.surname).all()
    return render_template("hr/employees.html", employees=employees, q=q)


@hr_bp.route("/employees/new", methods=["GET", "POST"])
@login_required
def new_employee():
    if request.method == "POST":
        employee = Employee(
            staff_no=request.form.get("staff_no") or None,
            surname=request.form["surname"].strip(),
            other_names=request.form["other_names"].strip(),
            id_type_id=request.form.get("id_type_id") or None,
            id_no=request.form.get("id_no") or None,
            telephone1=request.form.get("telephone1") or None,
            department_id=request.form.get("department_id") or None,
            designation=request.form.get("designation") or None,
            employment_type_id=request.form.get("employment_type_id") or None,
            date_employed=request.form.get("date_employed") or None,
            payroll_no=request.form.get("payroll_no") or None,
            pin_no=request.form.get("pin_no") or None,
            nhif_no=request.form.get("nhif_no") or None,
            nssf_no=request.form.get("nssf_no") or None,
            bank_name=request.form.get("bank_name") or None,
            bank_account_no=request.form.get("bank_account_no") or None,
        )
        db.session.add(employee)
        db.session.commit()
        flash(f"Employee {employee.full_name} added.", "success")
        return redirect(url_for("hr.list_employees"))

    return render_template(
        "hr/employee_form.html",
        employee=None,
        departments=Department.query.order_by(Department.name).all(),
        employment_types=EmploymentType.query.order_by(EmploymentType.name).all(),
        id_types=IdType.query.all(),
    )


@hr_bp.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
@login_required
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)

    if request.method == "POST":
        for field in ["staff_no", "surname", "other_names", "id_no", "telephone1",
                      "designation", "date_employed", "payroll_no", "pin_no",
                      "nhif_no", "nssf_no", "bank_name", "bank_account_no"]:
            setattr(employee, field, request.form.get(field) or None)
        employee.id_type_id = request.form.get("id_type_id") or None
        employee.department_id = request.form.get("department_id") or None
        employee.employment_type_id = request.form.get("employment_type_id") or None
        db.session.commit()
        flash(f"Employee {employee.full_name} updated.", "success")
        return redirect(url_for("hr.view_employee", employee_id=employee.employee_id))

    return render_template(
        "hr/employee_form.html",
        employee=employee,
        departments=Department.query.order_by(Department.name).all(),
        employment_types=EmploymentType.query.order_by(EmploymentType.name).all(),
        id_types=IdType.query.all(),
    )


@hr_bp.route("/employees/<int:employee_id>")
@login_required
def view_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template(
        "hr/employee_detail.html",
        employee=employee,
        parameters=PayrollParameter.query.join(PayrollParameterCategory).order_by(PayrollParameterCategory.name).all(),
    )


@hr_bp.route("/employees/<int:employee_id>/parameters", methods=["POST"])
@login_required
def set_employee_parameter(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    parameter_id = request.form.get("payroll_parameter_id")
    amount = Decimal(request.form.get("amount", "0") or "0")

    existing = EmployeePayrollParameter.query.filter_by(employee_id=employee.employee_id, payroll_parameter_id=parameter_id).first()
    if existing:
        existing.amount = amount
    else:
        db.session.add(EmployeePayrollParameter(employee_id=employee.employee_id, payroll_parameter_id=parameter_id, amount=amount))

    db.session.commit()
    flash("Payroll parameter updated.", "success")
    return redirect(url_for("hr.view_employee", employee_id=employee.employee_id))


# ── Departments & Employment Types (simple admin) ────────────────────────

@hr_bp.route("/departments", methods=["GET", "POST"])
@login_required
def list_departments():
    if request.method == "POST":
        db.session.add(Department(name=request.form["name"].strip()))
        db.session.commit()
        flash("Department added.", "success")
        return redirect(url_for("hr.list_departments"))
    return render_template("hr/departments.html", departments=Department.query.order_by(Department.name).all())


@hr_bp.route("/employment-types", methods=["GET", "POST"])
@login_required
def list_employment_types():
    # Viewing is open to any logged-in user (the Employee form needs it),
    # but only admins can add or edit — see edit_employment_type below.
    if request.method == "POST":
        if not current_user.is_admin:
            flash("Only admins can add employment types.", "error")
            return redirect(url_for("hr.list_employment_types"))
        name = request.form["name"].strip()
        if EmploymentType.query.filter_by(name=name).first():
            flash(f"'{name}' already exists.", "error")
        else:
            db.session.add(EmploymentType(name=name))
            db.session.commit()
            flash("Employment type added.", "success")
        return redirect(url_for("hr.list_employment_types"))
    return render_template("hr/employment_types.html", employment_types=EmploymentType.query.order_by(EmploymentType.name).all())


@hr_bp.route("/employment-types/<int:employment_type_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_employment_type(employment_type_id):
    employment_type = EmploymentType.query.get_or_404(employment_type_id)

    if request.method == "POST":
        name = request.form["name"].strip()
        existing = EmploymentType.query.filter_by(name=name).first()
        if existing and existing.employment_type_id != employment_type.employment_type_id:
            flash(f"'{name}' already exists.", "error")
            return redirect(url_for("hr.edit_employment_type", employment_type_id=employment_type.employment_type_id))
        employment_type.name = name
        db.session.commit()
        flash("Employment type updated.", "success")
        return redirect(url_for("hr.list_employment_types"))

    return render_template("hr/employment_type_form.html", employment_type=employment_type)


# ── Payroll Parameters (Earnings/Deductions catalog) ─────────────────────

@hr_bp.route("/parameters")
@login_required
def list_parameters():
    categories = PayrollParameterCategory.query.order_by(PayrollParameterCategory.name).all()
    return render_template("hr/parameters.html", categories=categories)


@hr_bp.route("/parameters/categories/new", methods=["GET", "POST"])
@login_required
def new_parameter_category():
    if request.method == "POST":
        db.session.add(PayrollParameterCategory(
            name=request.form["name"].strip(),
            category_type=request.form["category_type"],
        ))
        db.session.commit()
        flash("Category added.", "success")
        return redirect(url_for("hr.list_parameters"))
    return render_template("hr/parameter_category_form.html")


@hr_bp.route("/parameters/new", methods=["GET", "POST"])
@login_required
def new_parameter():
    if request.method == "POST":
        db.session.add(PayrollParameter(
            name=request.form["name"].strip(),
            parameter_category_id=request.form["parameter_category_id"],
        ))
        db.session.commit()
        flash("Payroll parameter added.", "success")
        return redirect(url_for("hr.list_parameters"))
    return render_template(
        "hr/parameter_form.html",
        categories=PayrollParameterCategory.query.order_by(PayrollParameterCategory.name).all(),
    )


# ── Payslip Periods & Generation ──────────────────────────────────────────

@hr_bp.route("/payroll", methods=["GET", "POST"])
@login_required
def list_periods():
    if request.method == "POST":
        month = int(request.form["pay_month"])
        year = int(request.form["pay_year"])
        if PayslipPeriod.query.filter_by(pay_month=month, pay_year=year).first():
            flash("That period already exists.", "error")
            return redirect(url_for("hr.list_periods"))

        import calendar
        last_day = calendar.monthrange(year, month)[1]
        period = PayslipPeriod(
            pay_month=month, pay_year=year,
            beginning_date=f"{year}-{month:02d}-01",
            ending_date=f"{year}-{month:02d}-{last_day:02d}",
        )
        db.session.add(period)
        db.session.commit()
        flash(f"Period {period.label} created.", "success")
        return redirect(url_for("hr.list_periods"))

    periods = PayslipPeriod.query.order_by(PayslipPeriod.pay_year.desc(), PayslipPeriod.pay_month.desc()).all()
    return render_template("hr/periods.html", periods=periods)


@hr_bp.route("/payroll/<int:payslip_period_id>/generate", methods=["POST"])
@login_required
def generate_payslips(payslip_period_id):
    period = PayslipPeriod.query.get_or_404(payslip_period_id)
    employees = Employee.query.filter_by(is_active=True).all()
    created = 0

    for employee in employees:
        if Payslip.query.filter_by(employee_id=employee.employee_id, payslip_period_id=period.payslip_period_id).first():
            continue  # already generated for this employee/period

        standing = EmployeePayrollParameter.query.filter_by(employee_id=employee.employee_id).all()
        if not standing:
            continue  # nothing configured for this employee — skip rather than generate an empty payslip

        gross = Decimal("0")
        deductions = Decimal("0")
        payslip = Payslip(employee_id=employee.employee_id, payslip_period_id=period.payslip_period_id)
        db.session.add(payslip)
        db.session.flush()

        for sp in standing:
            category_type = sp.parameter.category.category_type
            db.session.add(PayslipItem(
                payslip_id=payslip.payslip_id,
                name=sp.parameter.name,
                category_type=category_type,
                amount=sp.amount,
            ))
            if category_type == "Earning":
                gross += sp.amount
            else:
                deductions += sp.amount

        payslip.gross_earning_total = gross
        payslip.deduction_total = deductions
        payslip.net_pay = gross - deductions
        created += 1

    db.session.commit()
    flash(f"Generated {created} payslip(s) for {period.label}.", "success")
    return redirect(url_for("hr.view_period", payslip_period_id=period.payslip_period_id))


@hr_bp.route("/payroll/<int:payslip_period_id>")
@login_required
def view_period(payslip_period_id):
    period = PayslipPeriod.query.get_or_404(payslip_period_id)
    payslips = Payslip.query.filter_by(payslip_period_id=period.payslip_period_id).all()
    return render_template("hr/period_detail.html", period=period, payslips=payslips)


@hr_bp.route("/payslips/<int:payslip_id>")
@login_required
def view_payslip(payslip_id):
    payslip = Payslip.query.get_or_404(payslip_id)
    return render_template("hr/payslip.html", payslip=payslip)


@hr_bp.route("/payslips/<int:payslip_id>/mark-paid", methods=["POST"])
@login_required
def mark_paid(payslip_id):
    payslip = Payslip.query.get_or_404(payslip_id)
    payslip.is_paid = True
    db.session.commit()
    flash(f"{payslip.employee.full_name}'s payslip marked as paid.", "success")
    return redirect(url_for("hr.view_period", payslip_period_id=payslip.payslip_period_id))
