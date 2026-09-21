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
