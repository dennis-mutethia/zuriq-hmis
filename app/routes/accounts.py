from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import (
    AccountType, Account, SubAccount, AccountSubAccount,
    FiscalPeriod, JournalVoucher, SubaccountEntry,
    Bank, BankBranch, BankDeposit, BankReconciliation, BankRecItem,
)

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")


# ── Journal Vouchers ─────────────────────────────────────────────────────

@accounts_bp.route("/")
@login_required
def list_vouchers():
    vouchers = JournalVoucher.query.order_by(JournalVoucher.transaction_datetime.desc()).limit(200).all()
    return render_template("accounts/list.html", vouchers=vouchers)


@accounts_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_voucher():
    if request.method == "POST":
        acc_sub_acc_ids = request.form.getlist("acc_sub_acc_id")
        entry_types = request.form.getlist("entry_type")
        amounts = request.form.getlist("amount")

        lines = []
        for asa_id, etype, amt_raw in zip(acc_sub_acc_ids, entry_types, amounts):
            if not asa_id or not amt_raw:
                continue
            try:
                amt = Decimal(amt_raw)
            except InvalidOperation:
                continue
            if amt <= 0:
                continue
            lines.append((int(asa_id), etype, amt))

        if len(lines) < 2:
            flash("A journal voucher needs at least two lines (one debit, one credit).", "error")
            return redirect(url_for("accounts.new_voucher"))

        total_debit = sum((amt for _, t, amt in lines if t == "Debit"), Decimal("0"))
        total_credit = sum((amt for _, t, amt in lines if t == "Credit"), Decimal("0"))
        if total_debit != total_credit:
            flash(f"Debits (KES {total_debit:,.2f}) must equal credits (KES {total_credit:,.2f}) — not saved.", "error")
            return redirect(url_for("accounts.new_voucher"))

        period = FiscalPeriod.get_or_create_current()
        voucher = JournalVoucher(
            description=request.form["description"].strip(),
            source_reference=request.form.get("source_reference") or None,
            fiscal_period_id=period.fiscal_period_id,
            created_by=current_user.system_user_id,
        )
        db.session.add(voucher)
        db.session.flush()

        for asa_id, etype, amt in lines:
            db.session.add(SubaccountEntry(
                journal_voucher_id=voucher.journal_voucher_id,
                acc_sub_acc_id=asa_id,
                entry_type=etype,
                amount=amt,
                fiscal_period_id=period.fiscal_period_id,
            ))

        db.session.commit()
        flash(f"Journal voucher posted — {len(lines)} lines, KES {total_debit:,.2f} balanced.", "success")
        return redirect(url_for("accounts.list_vouchers"))

    return render_template(
        "accounts/new_voucher.html",
        acc_sub_accs=AccountSubAccount.query.join(Account).order_by(Account.account_no).all(),
    )


@accounts_bp.route("/<int:journal_voucher_id>")
@login_required
def view_voucher(journal_voucher_id):
    voucher = JournalVoucher.query.get_or_404(journal_voucher_id)
    return render_template("accounts/view_voucher.html", voucher=voucher)


# ── Chart of Accounts ────────────────────────────────────────────────────

@accounts_bp.route("/chart")
@login_required
def chart_of_accounts():
    accounts = Account.query.order_by(Account.account_no).all()
    return render_template("accounts/chart.html", accounts=accounts)


@accounts_bp.route("/chart/new", methods=["GET", "POST"])
@login_required
def new_account():
    if request.method == "POST":
        account = Account(
            account_no=request.form["account_no"].strip(),
            name=request.form["name"].strip(),
            account_type_id=request.form["account_type_id"],
        )
        db.session.add(account)
        db.session.commit()
        flash(f"Account '{account.account_no} — {account.name}' created.", "success")
        return redirect(url_for("accounts.chart_of_accounts"))
    return render_template("accounts/account_form.html", account=None, account_types=AccountType.query.order_by(AccountType.account_type_id).all())


@accounts_bp.route("/chart/<int:account_id>/edit", methods=["GET", "POST"])
@login_required
def edit_account(account_id):
    account = Account.query.get_or_404(account_id)
    if request.method == "POST":
        account.account_no = request.form["account_no"].strip()
        account.name = request.form["name"].strip()
        account.account_type_id = request.form["account_type_id"]
        db.session.commit()
        flash(f"Account '{account.account_no} — {account.name}' updated.", "success")
        return redirect(url_for("accounts.chart_of_accounts"))
    return render_template("accounts/account_form.html", account=account, account_types=AccountType.query.order_by(AccountType.account_type_id).all())


# ── Account Types ────────────────────────────────────────────────────────

@accounts_bp.route("/account-types")
@login_required
def list_account_types():
    account_types = AccountType.query.order_by(AccountType.account_type_id).all()
    return render_template("accounts/account_types.html", account_types=account_types)


@accounts_bp.route("/account-types/<int:account_type_id>/edit", methods=["GET", "POST"])
@login_required
def edit_account_type(account_type_id):
    account_type = AccountType.query.get_or_404(account_type_id)
    if request.method == "POST":
        account_type.name = request.form["name"].strip()
        db.session.commit()
        flash("Account type updated.", "success")
        return redirect(url_for("accounts.list_account_types"))
    return render_template("accounts/account_type_form.html", account_type=account_type)


# ── Sub-Accounts ─────────────────────────────────────────────────────────

@accounts_bp.route("/sub-accounts")
@login_required
def list_sub_accounts():
    sub_accounts = SubAccount.query.order_by(SubAccount.name).all()
    return render_template("accounts/sub_accounts.html", sub_accounts=sub_accounts)


@accounts_bp.route("/sub-accounts/new", methods=["GET", "POST"])
@login_required
def new_sub_account():
    if request.method == "POST":
        sub_account = SubAccount(name=request.form["name"].strip())
        db.session.add(sub_account)
        db.session.commit()
        flash(f"Sub-account '{sub_account.name}' created.", "success")
        return redirect(url_for("accounts.list_sub_accounts"))
    return render_template("accounts/sub_account_form.html", sub_account=None)


@accounts_bp.route("/sub-accounts/<int:sub_account_id>/edit", methods=["GET", "POST"])
@login_required
def edit_sub_account(sub_account_id):
    sub_account = SubAccount.query.get_or_404(sub_account_id)
    if request.method == "POST":
        sub_account.name = request.form["name"].strip()
        db.session.commit()
        flash(f"Sub-account '{sub_account.name}' updated.", "success")
        return redirect(url_for("accounts.list_sub_accounts"))
    return render_template("accounts/sub_account_form.html", sub_account=sub_account)


@accounts_bp.route("/sub-accounts/<int:sub_account_id>/link", methods=["GET", "POST"])
@login_required
def link_sub_account(sub_account_id):
    sub_account = SubAccount.query.get_or_404(sub_account_id)

    if request.method == "POST":
        account_id = request.form.get("account_id")
        if AccountSubAccount.query.filter_by(account_id=account_id, sub_account_id=sub_account.sub_account_id).first():
            flash("Already linked to that account.", "error")
        else:
            db.session.add(AccountSubAccount(account_id=account_id, sub_account_id=sub_account.sub_account_id))
            db.session.commit()
            flash(f"Linked '{sub_account.name}' to the selected account.", "success")
        return redirect(url_for("accounts.list_sub_accounts"))

    linked_account_ids = {l.account_id for l in AccountSubAccount.query.filter_by(sub_account_id=sub_account.sub_account_id).all()}
    available = [a for a in Account.query.order_by(Account.account_no).all() if a.account_id not in linked_account_ids]
    return render_template("accounts/link_sub_account.html", sub_account=sub_account, available=available)


# ── Ledger view (per sub-account, across all vouchers) ──────────────────

@accounts_bp.route("/ledger/<int:acc_sub_acc_id>")
@login_required
def ledger(acc_sub_acc_id):
    asa = AccountSubAccount.query.get_or_404(acc_sub_acc_id)
    entries = (
        SubaccountEntry.query
        .filter_by(acc_sub_acc_id=acc_sub_acc_id)
        .order_by(SubaccountEntry.transaction_datetime)
        .all()
    )
    running = Decimal("0")
    rows = []
    for e in entries:
        running += e.amount if e.entry_type == "Debit" else -e.amount
        rows.append((e, running))
    return render_template("accounts/ledger.html", asa=asa, rows=rows, balance=running)


# ── Fiscal Periods (read/admin) ──────────────────────────────────────────

@accounts_bp.route("/periods")
@login_required
def list_periods():
    periods = FiscalPeriod.query.order_by(FiscalPeriod.start_date.desc()).all()
    return render_template("accounts/periods.html", periods=periods)


# ── Banking: banks/branches (simple admin) ───────────────────────────────

@accounts_bp.route("/banks")
@login_required
def list_banks():
    banks = Bank.query.order_by(Bank.name).all()
    return render_template("accounts/banks.html", banks=banks)


@accounts_bp.route("/banks/new", methods=["GET", "POST"])
@login_required
def new_bank():
    if request.method == "POST":
        db.session.add(Bank(name=request.form["name"].strip(), bank_code=request.form.get("bank_code") or None))
        db.session.commit()
        flash("Bank added.", "success")
        return redirect(url_for("accounts.list_banks"))
    return render_template("accounts/bank_form.html", bank=None)


@accounts_bp.route("/banks/<int:bank_id>/edit", methods=["GET", "POST"])
@login_required
def edit_bank(bank_id):
    bank = Bank.query.get_or_404(bank_id)
    if request.method == "POST":
        bank.name = request.form["name"].strip()
        bank.bank_code = request.form.get("bank_code") or None
        db.session.commit()
        flash(f"Bank '{bank.name}' updated.", "success")
        return redirect(url_for("accounts.list_banks"))
    return render_template("accounts/bank_form.html", bank=bank)


@accounts_bp.route("/banks/<int:bank_id>/branches/new", methods=["GET", "POST"])
@login_required
def new_bank_branch(bank_id):
    bank = Bank.query.get_or_404(bank_id)
    if request.method == "POST":
        db.session.add(BankBranch(
            bank_id=bank.bank_id,
            name=request.form["name"].strip(),
            branch_code=request.form.get("branch_code") or None,
        ))
        db.session.commit()
        flash(f"Branch added to {bank.name}.", "success")
        return redirect(url_for("accounts.list_banks"))
    return render_template("accounts/bank_branch_form.html", bank=bank, branch=None)


@accounts_bp.route("/banks/branches/<int:bank_branch_id>/edit", methods=["GET", "POST"])
@login_required
def edit_bank_branch(bank_branch_id):
    branch = BankBranch.query.get_or_404(bank_branch_id)
    if request.method == "POST":
        branch.name = request.form["name"].strip()
        branch.branch_code = request.form.get("branch_code") or None
        db.session.commit()
        flash(f"Branch '{branch.name}' updated.", "success")
        return redirect(url_for("accounts.list_banks"))
    return render_template("accounts/bank_branch_form.html", bank=branch.bank, branch=branch)


# ── Bank Deposits ─────────────────────────────────────────────────────────

@accounts_bp.route("/deposits")
@login_required
def list_deposits():
    deposits = BankDeposit.query.order_by(BankDeposit.date_time_deposited.desc()).limit(200).all()
    return render_template("accounts/deposits.html", deposits=deposits)


@accounts_bp.route("/deposits/new", methods=["GET", "POST"])
@login_required
def new_deposit():
    bank_sub_accs = AccountSubAccount.query.join(Account).order_by(Account.account_no).all()

    if request.method == "POST":
        amount = Decimal(request.form.get("amount", "0") or "0")
        if amount <= 0:
            flash("Enter an amount greater than zero.", "error")
            return redirect(url_for("accounts.new_deposit"))

        deposit = BankDeposit(
            dest_acc_sub_acc_id=request.form["dest_acc_sub_acc_id"],
            source_acc_sub_acc_id=request.form.get("source_acc_sub_acc_id") or None,
            amount=amount,
            bank_transaction_ref_no=request.form.get("bank_transaction_ref_no") or None,
            cheque_nos=request.form.get("cheque_nos") or None,
            deposited_by=current_user.system_user_id,
        )

        # Post a balanced GL entry if a source sub-account was given: Debit
        # the destination (the deposit increases the bank account), Credit
        # the source (usually Cash — the till decreases by the same amount).
        if deposit.source_acc_sub_acc_id:
            period = FiscalPeriod.get_or_create_current()
            voucher = JournalVoucher(
                description=f"Bank deposit — {request.form.get('bank_transaction_ref_no') or 'no reference'}",
                fiscal_period_id=period.fiscal_period_id,
                created_by=current_user.system_user_id,
            )
            db.session.add(voucher)
            db.session.flush()
            db.session.add(SubaccountEntry(
                journal_voucher_id=voucher.journal_voucher_id, acc_sub_acc_id=deposit.dest_acc_sub_acc_id,
                entry_type="Debit", amount=amount, fiscal_period_id=period.fiscal_period_id,
            ))
            db.session.add(SubaccountEntry(
                journal_voucher_id=voucher.journal_voucher_id, acc_sub_acc_id=deposit.source_acc_sub_acc_id,
                entry_type="Credit", amount=amount, fiscal_period_id=period.fiscal_period_id,
            ))
            deposit.journal_voucher_id = voucher.journal_voucher_id

        db.session.add(deposit)
        db.session.commit()
        flash(f"Deposit of KES {amount:,.2f} recorded.", "success")
        return redirect(url_for("accounts.list_deposits"))

    return render_template("accounts/new_deposit.html", acc_sub_accs=bank_sub_accs)


# ── Bank Reconciliation ───────────────────────────────────────────────────

@accounts_bp.route("/reconciliation")
@login_required
def list_reconciliations():
    recs = BankReconciliation.query.order_by(BankReconciliation.to_date.desc()).all()
    return render_template("accounts/reconciliations.html", recs=recs)


@accounts_bp.route("/reconciliation/new", methods=["GET", "POST"])
@login_required
def new_reconciliation():
    if request.method == "POST":
        rec = BankReconciliation(
            acc_sub_acc_id=request.form["acc_sub_acc_id"],
            from_date=request.form["from_date"],
            to_date=request.form["to_date"],
            book_balance=Decimal(request.form.get("book_balance", "0") or "0"),
            statement_balance=Decimal(request.form.get("statement_balance", "0") or "0"),
        )
        db.session.add(rec)
        db.session.commit()
        flash("Reconciliation started.", "success")
        return redirect(url_for("accounts.view_reconciliation", bank_rec_id=rec.bank_rec_id))

    return render_template(
        "accounts/new_reconciliation.html",
        acc_sub_accs=AccountSubAccount.query.join(Account).order_by(Account.account_no).all(),
    )


@accounts_bp.route("/reconciliation/<int:bank_rec_id>", methods=["GET", "POST"])
@login_required
def view_reconciliation(bank_rec_id):
    rec = BankReconciliation.query.get_or_404(bank_rec_id)

    if request.method == "POST":
        db.session.add(BankRecItem(
            bank_rec_id=rec.bank_rec_id,
            description=request.form["description"].strip(),
            amount=Decimal(request.form.get("amount", "0") or "0"),
            side=request.form["side"],
            is_increment=(request.form.get("direction") == "increase"),
        ))
        db.session.commit()
        flash("Reconciling item added.", "success")
        return redirect(url_for("accounts.view_reconciliation", bank_rec_id=rec.bank_rec_id))

    return render_template("accounts/view_reconciliation.html", rec=rec)


@accounts_bp.route("/reconciliation/<int:bank_rec_id>/complete", methods=["POST"])
@login_required
def complete_reconciliation(bank_rec_id):
    rec = BankReconciliation.query.get_or_404(bank_rec_id)
    if not rec.is_balanced:
        flash(f"Can't mark complete — adjusted balances differ by KES {rec.difference:,.2f}.", "error")
        return redirect(url_for("accounts.view_reconciliation", bank_rec_id=rec.bank_rec_id))

    rec.has_been_reconciled = True
    rec.reconciled_by = current_user.system_user_id
    rec.reconciled_at = datetime.now(timezone.utc)
    db.session.commit()
    flash("Reconciliation completed.", "success")
    return redirect(url_for("accounts.list_reconciliations"))
