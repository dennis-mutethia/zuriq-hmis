import click
from app import db


def register_cli(app):
    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(username, password):
        """Create a system user (there's no self-registration — this is
        how you bootstrap the first login, and how you'd add staff
        accounts from the terminal if you don't want to use the in-app
        Users page)."""
        from app.models import SystemUser, Role

        if SystemUser.query.filter_by(username=username).first():
            click.echo(f"A user named '{username}' already exists.")
            return

        admin_role = Role.query.filter_by(is_admin_role=True).first()
        if not admin_role:
            click.echo("No admin role found — run the roles migration/schema first.")
            return

        # This command is specifically for bootstrapping the first login,
        # so it always creates an admin — there'd be no admin at all
        # otherwise. Additional staff accounts should go through /users
        # (or this same command, then change their role via SQL if needed).
        user = SystemUser(username=username, role_id=admin_role.role_id)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created admin user '{username}'.")
