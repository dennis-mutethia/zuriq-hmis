from datetime import datetime, timezone
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class IdType(db.Model):
    __tablename__ = "id_types"
    id_type_id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.Text, nullable=False)


class Nationality(db.Model):
    __tablename__ = "nationalities"
    nationality_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class GroupAccount(db.Model):
    __tablename__ = "group_accounts"
    group_account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    physical_address = db.Column(db.Text)
    postal_address = db.Column(db.Text)
    postal_code = db.Column(db.Text)
    town_city = db.Column(db.Text)
    telephone1 = db.Column(db.Text)
    email_address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    has_co_pay = db.Column(db.Boolean, nullable=False, default=False)
    co_pay_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    contract_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    credit_limit = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    has_visit_days_cap = db.Column(db.Boolean, nullable=False, default=False)
    capping_days = db.Column(db.Integer)
    receivable_acc_sub_acc_id = db.Column(db.Integer)


class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    is_admin_role = db.Column(db.Boolean, nullable=False, default=False)


class SystemUser(UserMixin, db.Model):
    __tablename__ = "system_users"
    system_user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)
    is_active_flag = db.Column("is_active", db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    role = db.relationship("Role")

    @property
    def is_admin(self):
        return bool(self.role and self.role.is_admin_role)

    def get_id(self):
        # flask-login needs a string id
        return str(self.system_user_id)

    @property
    def is_active(self):
        # overrides UserMixin's default (always-True) so a deactivated
        # account can't log in even with the correct password
        return self.is_active_flag

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return bool(self.password_hash) and check_password_hash(self.password_hash, raw_password)


class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True)
    out_patient_no = db.Column(db.Text, unique=True)   # system-generated: ZH-OP-{patient_id}
    in_patient_no = db.Column(db.Text, unique=True)    # system-generated: ZH-IP-{patient_id}
    surname = db.Column(db.Text, nullable=False)
    other_names = db.Column(db.Text, nullable=False)
    third_name = db.Column(db.Text)
    sex = db.Column(db.Text, nullable=False)
    date_of_birth = db.Column(db.DateTime(timezone=True))
    occupation = db.Column(db.Text)
    residence = db.Column(db.Text)
    city_town = db.Column(db.Text)
    telephone1 = db.Column(db.Text)
    telephone2 = db.Column(db.Text)
    email_address = db.Column(db.Text)
    postal_address = db.Column(db.Text)
    postal_code = db.Column(db.Text)
    next_of_kin = db.Column(db.Text)
    next_of_kin_relationship = db.Column(db.Text)
    next_of_kin_contact = db.Column(db.Text)
    date_registered = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    id_type_id = db.Column(db.Integer, db.ForeignKey("id_types.id_type_id"))
    id_number = db.Column(db.Text)
    nationality_id = db.Column(db.Integer, db.ForeignKey("nationalities.nationality_id"))
    group_account_id = db.Column(db.Integer, db.ForeignKey("group_accounts.group_account_id"))
    reference_no = db.Column(db.Text)
    principal_member = db.Column(db.Text)
    membership_no = db.Column(db.Text)
    company_name = db.Column(db.Text)
    note = db.Column(db.Text)
    registered_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))

    id_type = db.relationship("IdType")
    nationality = db.relationship("Nationality")
    group_account = db.relationship("GroupAccount")
    registered_by_user = db.relationship("SystemUser")

    @property
    def full_name(self):
        parts = [self.surname, self.other_names, self.third_name]
        return " ".join(p for p in parts if p)


class Clinic(db.Model):
    __tablename__ = "clinics"
    clinic_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Visit(db.Model):
    __tablename__ = "visits"

    visit_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinics.clinic_id"))
    visit_datetime = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    age = db.Column(db.Integer)
    age_months = db.Column(db.Integer)
    age_weeks = db.Column(db.Integer)
    doctor = db.Column(db.Text)
    nurse = db.Column(db.Text)
    hpi = db.Column(db.Text)
    summary = db.Column(db.Text)
    is_processed = db.Column(db.Boolean, nullable=False, default=False)
    is_admitted = db.Column(db.Boolean, nullable=False, default=False)
    is_consultant = db.Column(db.Boolean, nullable=False, default=False)
    registered_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))

    patient = db.relationship("Patient")
    clinic = db.relationship("Clinic")


class AccountType(db.Model):
    __tablename__ = "account_types"
    account_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class Account(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    account_no = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    account_type_id = db.Column(db.Integer, db.ForeignKey("account_types.account_type_id"), nullable=False)

    account_type = db.relationship("AccountType")


class SubAccount(db.Model):
    __tablename__ = "sub_accounts"
    sub_account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    links = db.relationship("AccountSubAccount", backref="sub_account_obj", overlaps="sub_account")


class AccountSubAccount(db.Model):
    __tablename__ = "account_sub_accounts"
    acc_sub_acc_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"), nullable=False)
    sub_account_id = db.Column(db.Integer, db.ForeignKey("sub_accounts.sub_account_id"), nullable=False)

    account = db.relationship("Account")
    sub_account = db.relationship("SubAccount")

    @property
    def display_name(self):
        return f"{self.account.account_no} — {self.account.name} / {self.sub_account.name}"

    @staticmethod
    def find_by_sub_account_name(name):
        """Used by integrations (e.g. Billing) that post to a well-known
        sub-account by name. Returns None if it's been renamed or
        deleted — callers must handle that by skipping the post, not
        crashing, since accounts are user-editable."""
        return (
            AccountSubAccount.query
            .join(SubAccount)
            .filter(SubAccount.name == name)
            .first()
        )


class FiscalPeriod(db.Model):
    __tablename__ = "fiscal_periods"
    fiscal_period_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def get_or_create_current():
        from datetime import date
        import calendar
        today = date.today()
        period = FiscalPeriod.query.filter(
            FiscalPeriod.start_date <= today, FiscalPeriod.end_date >= today
        ).first()
        if period:
            return period
        start = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end = today.replace(day=last_day)
        period = FiscalPeriod(name=start.strftime("%B %Y"), start_date=start, end_date=end)
        db.session.add(period)
        db.session.flush()
        return period


class JournalVoucher(db.Model):
    __tablename__ = "journal_vouchers"

    journal_voucher_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    transaction_datetime = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    source_reference = db.Column(db.Text)
    fiscal_period_id = db.Column(db.Integer, db.ForeignKey("fiscal_periods.fiscal_period_id"))
    created_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))

    fiscal_period = db.relationship("FiscalPeriod")
    created_by_user = db.relationship("SystemUser")
    entries = db.relationship("SubaccountEntry", backref="journal_voucher", cascade="all, delete-orphan")

    @property
    def total_debit(self):
        return sum((e.amount for e in self.entries if e.entry_type == "Debit"), Decimal("0"))

    @property
    def total_credit(self):
        return sum((e.amount for e in self.entries if e.entry_type == "Credit"), Decimal("0"))

    @property
    def is_balanced(self):
        return self.total_debit == self.total_credit


class SubaccountEntry(db.Model):
    __tablename__ = "subaccount_entries"

    subaccount_entry_id = db.Column(db.Integer, primary_key=True)
    journal_voucher_id = db.Column(db.Integer, db.ForeignKey("journal_vouchers.journal_voucher_id"), nullable=False)
    acc_sub_acc_id = db.Column(db.Integer, db.ForeignKey("account_sub_accounts.acc_sub_acc_id"), nullable=False)
    entry_type = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    transaction_datetime = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    fiscal_period_id = db.Column(db.Integer, db.ForeignKey("fiscal_periods.fiscal_period_id"))

    acc_sub_acc = db.relationship("AccountSubAccount")


class Room(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class QueueEntry(db.Model):
    __tablename__ = "queue_entries"

    queue_entry_id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.visit_id"), nullable=False)
    from_room_id = db.Column(db.Integer, db.ForeignKey("rooms.room_id"))
    to_room_id = db.Column(db.Integer, db.ForeignKey("rooms.room_id"), nullable=False)
    queued_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    called_at = db.Column(db.DateTime(timezone=True))
    completed_at = db.Column(db.DateTime(timezone=True))
    created_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))

    visit = db.relationship("Visit", backref="queue_entries")
    from_room = db.relationship("Room", foreign_keys=[from_room_id])
    to_room = db.relationship("Room", foreign_keys=[to_room_id])

    @property
    def status(self):
        if self.completed_at:
            return "done"
        if self.called_at:
            return "in_service"
        return "waiting"

    @property
    def waiting_minutes(self):
        end = self.called_at or datetime.now(timezone.utc)
        return int((end - self.queued_at).total_seconds() // 60)

    @property
    def service_minutes(self):
        if not self.called_at:
            return None
        end = self.completed_at or datetime.now(timezone.utc)
        return int((end - self.called_at).total_seconds() // 60)


class NurseTriage(db.Model):
    __tablename__ = "nurse_triage"

    nurse_triage_id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.visit_id"), nullable=False)
    blood_pressure = db.Column(db.Text)
    blood_pressure_remarks = db.Column(db.Text)
    pulse_rate = db.Column(db.Numeric(5, 1))
    pulse_rate_remarks = db.Column(db.Text)
    respiration_rate = db.Column(db.Numeric(5, 1))
    respiration_rate_remarks = db.Column(db.Text)
    temperature = db.Column(db.Numeric(4, 1))
    temperature_remarks = db.Column(db.Text)
    weight = db.Column(db.Numeric(6, 2))
    weight_remarks = db.Column(db.Text)
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    visit = db.relationship("Visit", backref="triage_records")
    recorded_by_user = db.relationship("SystemUser")


class ObservationChart(db.Model):
    __tablename__ = "observation_charts"

    observation_id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey("admissions.admission_id"), nullable=False)
    systolic = db.Column(db.Numeric(5, 1))
    diastolic = db.Column(db.Numeric(5, 1))
    pulse = db.Column(db.Numeric(5, 1))
    respiratory = db.Column(db.Numeric(5, 1))
    spo2 = db.Column(db.Numeric(5, 1))
    temperature = db.Column(db.Numeric(4, 1))
    comments = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    admission = db.relationship("Admission", backref="observations")
    recorded_by_user = db.relationship("SystemUser")


class Service(db.Model):
    __tablename__ = "services"
    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    department_id = db.Column(db.Integer)
    cash_rate = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    nhif_rate = db.Column(db.Numeric(14, 2))
    aar_rate = db.Column(db.Numeric(14, 2))
    kcb_rate = db.Column(db.Numeric(14, 2))
    eduafya_rate = db.Column(db.Numeric(14, 2))
    liason_rate = db.Column(db.Numeric(14, 2))
    national_scheme_rate = db.Column(db.Numeric(14, 2))
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class MedicalBill(db.Model):
    __tablename__ = "medical_bills"

    medical_bill_id = db.Column(db.Integer, primary_key=True)
    medical_bill_no = db.Column(db.Text, unique=True)   # system-generated: ZH-MB-{medical_bill_id}
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.visit_id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"))
    is_patient = db.Column(db.Boolean, nullable=False, default=True)
    customer_name = db.Column(db.Text)
    telephone_no = db.Column(db.Text)
    id_number = db.Column(db.Text)
    group_account_id = db.Column(db.Integer, db.ForeignKey("group_accounts.group_account_id"))
    total_bill_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    sales_discount_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    write_off_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    cover_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    advance_payment = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    total_amount_paid = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    deposit_balance = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    deposit_offset = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    is_processed = db.Column(db.Boolean, nullable=False, default=False)
    date_time_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    date_time_processed = db.Column(db.DateTime(timezone=True))
    processed_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))

    visit = db.relationship("Visit")
    patient = db.relationship("Patient")
    group_account = db.relationship("GroupAccount")
    items = db.relationship("BillItem", backref="bill", cascade="all, delete-orphan")

    @property
    def balance_due(self):
        return (self.total_bill_amount or 0) - (self.total_amount_paid or 0) - (self.cover_amount or 0)

    @staticmethod
    def get_or_create_for_visit(visit):
        """The one open (unpaid) bill for this visit — created if it
        doesn't exist yet. Services, Pharmacy, and Lab all bill into this
        same running total rather than each starting a separate bill."""
        bill = (
            MedicalBill.query
            .filter_by(visit_id=visit.visit_id, is_processed=False)
            .order_by(MedicalBill.medical_bill_id.desc())
            .first()
        )
        if bill is None:
            patient = visit.patient
            bill = MedicalBill(
                visit_id=visit.visit_id,
                patient_id=patient.patient_id,
                is_patient=True,
                customer_name=patient.full_name,
                telephone_no=patient.telephone1,
                id_number=patient.id_number,
                group_account_id=patient.group_account_id,
            )
            db.session.add(bill)
            db.session.flush()  # need medical_bill_id before adding items
        return bill

    def add_item(self, name, quantity, rate, service_id=None):
        from decimal import Decimal
        rate = Decimal(rate or 0)
        quantity = int(quantity or 1)
        amount = rate * quantity
        item = BillItem(
            medical_bill_id=self.medical_bill_id,
            service_id=service_id,
            name=name,
            quantity=quantity,
            rate=rate,
            amount=amount,
        )
        db.session.add(item)
        self.total_bill_amount = Decimal(self.total_bill_amount or 0) + amount
        return item


class BillItem(db.Model):
    __tablename__ = "bill_items"

    bill_item_id = db.Column(db.Integer, primary_key=True)
    medical_bill_id = db.Column(db.Integer, db.ForeignKey("medical_bills.medical_bill_id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.service_id"))
    name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    rate = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    percentage_discount = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    discounted_amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    amount = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    has_been_paid_for = db.Column(db.Boolean, nullable=False, default=False)

    service = db.relationship("Service")


class Ward(db.Model):
    __tablename__ = "wards"
    ward_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Bed(db.Model):
    __tablename__ = "beds"
    bed_id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.ward_id"), nullable=False)
    bed_no = db.Column(db.Text, nullable=False)
    bed_status = db.Column(db.Text, nullable=False, default="Vacant")

    ward = db.relationship("Ward", backref="beds")


class Admission(db.Model):
    __tablename__ = "admissions"

    admission_id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.visit_id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    admission_datetime = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    discharge_datetime = db.Column(db.DateTime(timezone=True))
    is_in_admission = db.Column(db.Boolean, nullable=False, default=True)
    admitted_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))
    admitting_doctor = db.Column(db.Text)
    discharging_doctor = db.Column(db.Text)
    received_by_nurse = db.Column(db.Text)

    patient = db.relationship("Patient")
    visit = db.relationship("Visit")
    bed_assignments = db.relationship("AdmissionWard", backref="admission", order_by="AdmissionWard.assigned_at")

    @property
    def current_bed_assignment(self):
        for a in reversed(self.bed_assignments):
            if a.is_current_bed:
                return a
        return None


class AdmissionWard(db.Model):
    __tablename__ = "admission_ward"

    admission_ward_id = db.Column(db.Integer, primary_key=True)
    admission_id = db.Column(db.Integer, db.ForeignKey("admissions.admission_id"), nullable=False)
    ward_id = db.Column(db.Integer, db.ForeignKey("wards.ward_id"), nullable=False)
    bed_id = db.Column(db.Integer, db.ForeignKey("beds.bed_id"), nullable=False)
    is_current_bed = db.Column(db.Boolean, nullable=False, default=True)
    assigned_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    ward = db.relationship("Ward")
    bed = db.relationship("Bed")


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    unit_definition = db.Column(db.Text)
    unit_cost = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    unit_price = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    quantity_in_stock = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level


class Supplier(db.Model):
    __tablename__ = "suppliers"
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    contact_person = db.Column(db.Text)
    telephone = db.Column(db.Text)
    email = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    stock_movement_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.supplier_id"))
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    product = db.relationship("Product", backref="stock_movements")
    supplier = db.relationship("Supplier")
    recorded_by_user = db.relationship("SystemUser")


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    prescription_id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.visit_id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    prescribed_by = db.Column(db.Text)
    special_instruction = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    patient = db.relationship("Patient")
    visit = db.relationship("Visit")
    items = db.relationship("PrescriptionItem", backref="prescription", cascade="all, delete-orphan")

    @property
    def is_fully_dispensed(self):
        return bool(self.items) and all(i.has_been_dispensed for i in self.items)


class PrescriptionItem(db.Model):
    __tablename__ = "prescription_items"

    prescription_item_id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescriptions.prescription_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    inscription = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    quantity_per_time = db.Column(db.Text)
    frequency_per_day = db.Column(db.Text)
    dosage_duration = db.Column(db.Text)
    other_instruction = db.Column(db.Text)
    has_been_dispensed = db.Column(db.Boolean, nullable=False, default=False)
    dispensed_at = db.Column(db.DateTime(timezone=True))

    product = db.relationship("Product")


class Test(db.Model):
    __tablename__ = "tests"
    test_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    specimen = db.Column(db.Text)
    cash_rate = db.Column(db.Numeric(14, 2), nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class LabRequest(db.Model):
    __tablename__ = "lab_requests"

    lab_request_id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey("visits.visit_id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey("system_users.system_user_id"))
    technologist = db.Column(db.Text)
    date_time_requested = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    date_time_done = db.Column(db.DateTime(timezone=True))
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    reason_not_done = db.Column(db.Text)

    patient = db.relationship("Patient")
    visit = db.relationship("Visit")
    items = db.relationship("LabRequestItem", backref="lab_request", cascade="all, delete-orphan")


class LabRequestItem(db.Model):
    __tablename__ = "lab_request_items"

    lab_request_item_id = db.Column(db.Integer, primary_key=True)
    lab_request_id = db.Column(db.Integer, db.ForeignKey("lab_requests.lab_request_id"), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.test_id"))
    test_name = db.Column(db.Text, nullable=False)
    conclusion = db.Column(db.Text)

    test = db.relationship("Test")
