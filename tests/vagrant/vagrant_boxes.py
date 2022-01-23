#!/usr/bin/env python3
import os
from pathlib import Path
from time import sleep

import fabric
from entrypoint2 import entrypoint

import vagrant

# pip3 install fabric vncdotool python-vagrant entrypoint2

DIR = Path(__file__).parent


class Options:
    halt = True
    recreate = True
    destroy = False


def run_box(options, vagrantfile, cmds):
    env = os.environ
    if vagrantfile == "Vagrantfile":
        env["VAGRANT_VAGRANTFILE"] = str(DIR.parent.parent / vagrantfile)
        env["VAGRANT_DOTFILE_PATH"] = ""
    else:
        env["VAGRANT_VAGRANTFILE"] = str(DIR / vagrantfile)
        env["VAGRANT_DOTFILE_PATH"] = str(DIR / (".vagrant_" + vagrantfile))

    v = vagrant.Vagrant(env=env, quiet_stdout=False, quiet_stderr=False)
    status = v.status()
    state = status[0].state
    print(status)

    if options.destroy:
        v.halt(force=True)
        v.destroy()
        return

    if options.halt:
        v.halt()  # avoid screensaver

    if state == "not_created":
        # install programs in box
        v.up()
        # restart box
        v.halt()

    try:
        v.up()

        with fabric.Connection(
            v.user_hostname_port(),
            connect_kwargs={
                "key_filename": v.keyfile(),
            },
        ) as conn:
            with conn.cd("c:/vagrant" if options.win else "/vagrant"):
                if not options.win:
                    if options.osx:
                        freecmd = "top -l 1 -s 0 | grep PhysMem"
                    else:  # linux
                        freecmd = "free -h"
                    cmds = [freecmd, "env | sort"] + cmds + [freecmd]
                sleep(1)
                for cmd in cmds:
                    if options.recreate:
                        if "tox" in cmd:
                            cmd += " -r"
                    # hangs without pty=True
                    conn.run(cmd, echo=True, pty=True)
    finally:
        if options.halt:
            v.halt()


config = {
    "debian10": (
        "Vagrantfile.debian10.rb",
        ["tox -e py37"],
    ),
    "debian11": (
        "Vagrantfile.debian11.rb",
        ["tox -e py39"],
    ),
    "ubuntu2204": (
        "Vagrantfile.ubuntu2204.rb",
        ["tox -e py39"],
    ),
    "ubuntu2004": (
        "Vagrantfile",
        ["tox", "PYVIRTUALDISPLAY_DISPLAYFD=0 tox"],
    ),
    "ubuntu1804": (
        "Vagrantfile.ubuntu1804.rb",
        ["tox -e py36"],
    ),
    # "osx": (
    #     "Vagrantfile.osx.rb",
    #     [
    #         "bash --login -c 'python3 -m tox -e py3-osx'",
    #         # TODO: "bash --login -c 'PYVIRTUALDISPLAY_DISPLAYFD=0 python3 -m tox -e py3-osx'",
    #     ],
    # ),
}


@entrypoint
def main(boxes="all", fast=False, destroy=False):
    options = Options()
    options.halt = not fast
    options.recreate = not fast
    options.destroy = destroy

    if boxes == "all":
        boxes = list(config.keys())
    else:
        boxes = boxes.split(",")

    for k, v in config.items():
        name = k
        vagrantfile, cmds = v[0], v[1]
        if name in boxes:
            options.win = k.startswith("win")
            options.osx = k.startswith("osx")
            print("----->")
            print("----->")
            print("-----> %s %s %s" % (name, vagrantfile, cmds))
            print("----->")
            print("----->")
            try:
                run_box(options, vagrantfile, cmds)
            finally:
                print("<-----")
                print("<-----")
                print("<----- %s %s %s" % (name, vagrantfile, cmds))
                print("<-----")
                print("<-----")
