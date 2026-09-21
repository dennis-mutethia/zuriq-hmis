from datetime import datetime, timezone
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


class SystemUser(db.Model):
    __tablename__ = "system_users"
    system_user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


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
