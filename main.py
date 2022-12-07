import click

import runner


@click.command()
@click.option("--day", "-d", type=str, required=True, help="Day number")
def run(day: str):
    runner.run(day=day)


if __name__ == "__main__":
    run()
