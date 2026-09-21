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
        from app.models import SystemUser

        if SystemUser.query.filter_by(username=username).first():
            click.echo(f"A user named '{username}' already exists.")
            return

        user = SystemUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created user '{username}'.")
