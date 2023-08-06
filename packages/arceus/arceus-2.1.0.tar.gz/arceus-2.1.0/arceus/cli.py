#!/usr/bin/env python
import os
import sys
import traceback
from datetime import datetime, timedelta
import json

import click
from PyInquirer import style_from_dict, Token, prompt

from .account import Account, InvalidAccountError, RatelimitedError
from .snipers import Blocker, Transferrer
from .benchmark import Benchmarker
from .logger import log, log_logo

style = style_from_dict(
    {
        Token.Separator: "#cc5454",
        Token.QuestionMark: "#673ab7 bold",
        Token.Selected: "#cc5454",
        Token.Pointer: "#673ab7 bold",
        Token.Instruction: "",
        Token.Answer: "#f44336 bold",
        Token.Question: "",
    }
)


def exit(message: str = None):
    log(message or "Exiting...", "red")
    sys.exit()


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--target", type=str, help="Name to block")
@click.option("-c", "--config", "config_file", type=str, help="Path to config file")
@click.option("-a", "--attempts", type=int, default=20, help="Number of block attempts")
@click.option("-l", "--later", type=int, default=0, help="Days later to snipe")
def block(target: str, config_file: str, attempts: int, later: int):
    log_logo()

    if not target:
        target = prompt(
            {
                "type": "input",
                "name": "target",
                "message": "Enter the username you want to block:",
            }
        )["target"]

    if not config_file:
        config_file = prompt(
            [
                {
                    "type": "input",
                    "name": "config_file",
                    "message": "Enter path to config file",
                    "default": "config.json",
                }
            ]
        )["config_file"]

    config = json.load(open(config_file))

    accounts = [
        Account(account["email"], account["password"]) for account in config["accounts"]
    ]

    print(f"Accounts: {accounts}")

    if "offset" in config:
        offset = timedelta(milliseconds=config["offset"])
    else:
        offset = timedelta(milliseconds=0)

    log("Verifying accounts...", "yellow")

    auth_fail = False
    for account in accounts:
        try:
            account.authenticate()
            if account.get_challenges():
                auth_fail = True
                log(f'Account "{account.email}" is secured', "magenta")
        except:
            auth_fail = True
            log(f'Failed to authenticate account "{account.email}"', "magenta")

    if auth_fail and not prompt(
        [
            {
                "type": "confirm",
                "message": "One or more accounts failed to authenticate. Continue?",
                "name": "continue",
                "default": False,
            }
        ]
    )["continue"]:
        exit()

    try:
        blocker = Blocker(target, accounts, offset=offset)
        log(f"Setting up blocker...", "yellow")
        blocker.setup(attempts=attempts, later=timedelta(days=later), verbose=True)
    except AttributeError:
        traceback.print_exc()
        exit(message="Getting drop time failed. Name may be unavailable.")

    if account.check_blocked(target):
        log(f'Success! Account "{account.email}" blocked target name.', "green")
    else:
        log(
            f'Failure! Account "{account.email}" failed to block target name. 😢',
            "red",
        )

    exit()


@cli.command()
@click.option("-t", "--target", type=str, help="Name to block")
@click.option("-c", "--config", "config_file", type=str, help="Path to config file")
@click.option(
    "-a", "--attempts", type=int, default=100, help="Number of block attempts"
)
@click.option("-l", "--later", type=int, default=0, help="Days later to snipe")
def transfer(target: str, config_file: str, attempts: int, later: int):
    log_logo()

    if not target:
        target = prompt(
            {
                "type": "input",
                "name": "target",
                "message": "Enter the username you want to snipe:",
            }
        )["target"]

    if not config_file:
        config_file = prompt(
            [
                {
                    "type": "input",
                    "name": "config_file",
                    "message": "Enter path to config file",
                    "default": "config.json",
                }
            ]
        )["config_file"]

    config = json.load(open(config_file))
    accounts = [
        Account(account["email"], account["password"]) for account in config["accounts"]
    ]

    if "offset" in config:
        offset = timedelta(milliseconds=config["offset"])
    else:
        offset = timedelta(milliseconds=0)

    log("Verifying accounts...", "yellow")

    auth_fail = False
    for account in accounts:
        try:
            account.authenticate()
            if account.get_challenges():
                auth_fail = True
                log(f'Account "{account.email}" is secured', "magenta")
        except:
            auth_fail = True
            log(f'Failed to authenticate account "{account.email}"', "magenta")

    if auth_fail and not prompt(
        [
            {
                "type": "confirm",
                "message": "One or more accounts failed to authenticate. Continue?",
                "name": "continue",
                "default": False,
            }
        ]
    )["continue"]:
        exit()

    accounts = [
        Account(account["email"], account["password"]) for account in config["accounts"]
    ]

    print(f"Accounts: {accounts}")

    if "offset" in config:
        offset = timedelta(milliseconds=config["offset"])
    else:
        offset = timedelta(milliseconds=0)

    log("Verifying accounts...", "yellow")

    auth_fail = False
    for account in accounts:
        print("1")
        try:
            account.authenticate()
            if account.get_challenges():
                auth_fail = True
                log(f'Account "{account.email}" is secured', "magenta")
            print("2")
        except:
            print("fail")
            auth_fail = True
            log(f'Failed to authenticate account "{account.email}"', "magenta")

    if auth_fail and not prompt(
        [
            {
                "type": "confirm",
                "message": "One or more accounts failed to authenticate. Continue?",
                "name": "continue",
                "default": False,
            }
        ]
    )["continue"]:
        exit()
    try:
        transferrer = Transferrer(target, account, offset=offset)
        log(f"Setting up sniper...", "yellow")
        transferrer.setup(attempts=attempts, later=timedelta(days=later), verbose=True)
    except AttributeError:
        traceback.print_exc()
        exit(message="Getting drop time failed. Name may be unavailable.")

    if account.check_blocked(target):
        log(f'Success! Account "{account.email}" sniped target name.', "green")
    else:
        log(
            f'Failure! Account "{account.email}" failed to snipe target name. 😢',
            "red",
        )

    exit()


@cli.command()
@click.option(
    "-h",
    "--host",
    type=str,
    default="https://snipe-benchmark.herokuapp.com",
    help="Benchmark API to use",
)
@click.option("-o", "--offset", type=int, default=0, help="Request timing offset")
@click.option("-a", "--attempts", type=int, default=100, help="Number of attempts")
@click.option("-d", "--delay", type=float, default=15)
def benchmark(host: str, offset: int, attempts: int, delay: int):
    log_logo()

    benchmarker = Benchmarker(
        datetime.now() + timedelta(seconds=delay),
        offset=timedelta(milliseconds=offset),
        api_base=host,
    )
    benchmarker.setup(attempts=attempts, verbose=True)

    result = benchmarker.result
    log(f"Results:", "green")
    log(f"Delay: {result['delay']}ms", "magenta")
    requests = result["requests"]
    log(
        f"Requests: {requests['early'] + requests['late']} Total | {requests['early']} Early | {requests['late']} Late",
        "magenta",
    )
    log(f"Requests per second: {requests['rate']}", "magenta")

    exit()


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        exit(message=traceback.format_exc())
