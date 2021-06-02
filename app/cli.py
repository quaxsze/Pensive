import click
from flask.cli import with_appcontext
from app.models.user import User
from app.models.post import Post


@click.command("create-user")
@click.argument("username")
@click.argument("password")
@with_appcontext
def create_user(username, password):
    click.echo(f"Creating user {username}.")
    user = User(username=username)
    user.set_password(password)
    user.save()
    click.echo("Done.")


@click.command("create-post")
@click.argument("title")
@click.argument("content")
@click.argument("remote-url")
@with_appcontext
def create_post(title, content, remote_url):
    click.echo(f"Creating post {title}.")
    post = Post(title=title, content=content, remote_url=remote_url)
    post.save()
    click.echo("Done.")


def init_app(app):
    app.cli.add_command(create_user)
    app.cli.add_command(create_post)
