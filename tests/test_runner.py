"""Run with python3 tests/test_runner.py. Requires Neovim and less."""

import fcntl
import os
from pathlib import Path
import pty
import select
import shlex
import shutil
import struct
import subprocess
import tempfile
import termios
import time


RUNNER = Path(__file__).resolve().parents[1] / "vim-golf"


def check_resume(root, env):
    nvim = shutil.which("nvim")
    assert nvim, "Neovim is required"
    bindir = root / "bin"
    bindir.mkdir()
    wrapper = bindir / "nvim"
    wrapper.write_text(
        "#!/bin/sh\n"
        f"exec {shlex.quote(nvim)} --headless -u NONE -i NONE -n "
        '-s "$TEST_INPUT" "$@"\n'
    )
    wrapper.chmod(0o755)
    env = dict(env, PATH=f"{bindir}:{env['PATH']}", TEST_INPUT=str(root / "input"))
    day = "2026-08-01"
    state = Path(env["VIMGOLF_STATE_DIR"]) / day
    sessions = [b":s/x/A/\r:wq\r", b":s/A/B/\r:wq\r", b":q\r"]
    accumulated = b""
    best = len(sessions[0] + sessions[1])
    for index, keys in enumerate(sessions):
        Path(env["TEST_INPUT"]).write_bytes(keys)
        result = subprocess.run(
            [str(RUNNER), "play", day], env=env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, result.stderr
        accumulated += keys
        assert (state / "keys.log").read_bytes() == accumulated
        if index == 0:
            assert "not correct" in result.stderr
            assert (state / "work" / "file").read_text() == "A\n"
            assert not (state / "best").exists()
        else:
            assert f"raw-input score: {len(accumulated)} bytes (best: {best})" in result.stdout
            assert (state / "best").read_text() == f"{best}\n"
    print("PASS: partial edits, resume, and completed reopen retain cumulative input")


def check_brief(env):
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 100, 0, 0))
    process = subprocess.Popen(
        [str(RUNNER), "brief", "2026-08-01"],
        env=dict(env, TERM="xterm", LESS="-iRFXMx4", LESSOPEN="", LESSCLOSE=""),
        stdin=slave, stdout=slave, stderr=slave, start_new_session=True,
    )
    os.close(slave)
    output = b""
    try:
        deadline = time.monotonic() + 5
        while b"q closes" not in output and time.monotonic() < deadline:
            ready, _, _ = select.select([master], [], [], 0.1)
            if ready:
                try:
                    output += os.read(master, 65536)
                except OSError:
                    break
        assert b"Short challenge" in output, output
        assert b"q closes" in output, output
        assert process.poll() is None, "Short brief exited without q"
        os.write(master, b"q")
        deadline = time.monotonic() + 5
        while process.poll() is None and time.monotonic() < deadline:
            if select.select([master], [], [], 0.1)[0]:
                try:
                    if not os.read(master, 65536):
                        break
                except OSError:
                    break
        assert process.wait(timeout=5) == 0
    finally:
        os.close(master)
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
    print("PASS: short brief ignores LESS=-F, displays controls, and waits for q")


with tempfile.TemporaryDirectory(prefix="vim-golf-test-") as directory:
    root = Path(directory)
    challenge = root / "challenges" / "2026-08-01"
    for tree, text in (("start", "x\n"), ("expected", "B\n")):
        (challenge / tree).mkdir(parents=True)
        (challenge / tree / "file").write_text(text)
    (challenge / "entrypoint").write_text("file\n")
    (challenge / "challenge.md").write_text("# Short challenge\nChange x to B.\n")
    environment = dict(
        os.environ, TMUX="", VIMGOLF_CHALLENGES_DIR=str(root / "challenges"),
        VIMGOLF_STATE_DIR=str(root / "state"),
    )
    check_resume(root, environment)
    check_brief(environment)
