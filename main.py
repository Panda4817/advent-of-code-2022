import click

import runner


@click.command()
@click.option("--day", "-d", type=str, required=True, help="Day number")
@click.option("--year", "-y", type=str, required=True, help="Year number")
def run(day: str, year: str):
    runner.run(day=day, year=year)


if __name__ == "__main__":
    run()
