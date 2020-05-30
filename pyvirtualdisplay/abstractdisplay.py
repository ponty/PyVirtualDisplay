import fnmatch
import logging
import os
import select
import signal
import subprocess
import tempfile
import time
from threading import Lock

from easyprocess import EasyProcess, EasyProcessError

from pyvirtualdisplay import xauth
from pyvirtualdisplay.util import get_helptext, py2

# try:
#     import fcntl
# except ImportError:
#     fcntl = None


_mutex = Lock()

log = logging.getLogger(__name__)

_MIN_DISPLAY_NR = 1000
_USED_DISPLAY_NR_LIST = []

_X_START_TIMEOUT = 10
_X_START_TIME_STEP = 0.1
_X_START_WAIT = 0.1


class XStartTimeoutError(Exception):
    pass


class XStartError(Exception):
    pass


def _lock_files():
    tmpdir = "/tmp"
    try:
        ls = os.listdir(tmpdir)
    except FileNotFoundError:
        log.warning("missing /tmp")
        return []
    pattern = ".X*-lock"
    names = fnmatch.filter(ls, pattern)
    ls = [os.path.join(tmpdir, child) for child in names]
    ls = [p for p in ls if os.path.isfile(p)]
    return ls


def _search_for_display(randomizer=None):
    # search for free display
    ls = list(map(lambda x: int(x.split("X")[1].split("-")[0]), _lock_files()))
    if len(ls):
        display = max(_MIN_DISPLAY_NR, max(ls) + 3)
    else:
        display = _MIN_DISPLAY_NR

    if randomizer:
        display = randomizer.generate()

    return display


class AbstractDisplay(object):
    """
    Common parent for X servers (Xvfb,Xephyr,Xvnc)
    """

    def __init__(self, program, use_xauth, randomizer, retries, extra_args):
        self._extra_args = extra_args
        self._retries = retries
        self._program = program
        self._randomizer = randomizer
        self.stdout = None
        self.stderr = None
        self.old_display_var = None
        self._subproc = None
        self.display = None
        self.is_started = False

        helptext = get_helptext(program)
        self._has_displayfd = "-displayfd" in helptext
        if not self._has_displayfd:
            log.debug("-displayfd flag is missing.")
        # if check_startup and not has_displayfd:
        #     check_startup = False
        #     log.warning(
        #         program
        #         + " -displayfd flag is not supported, 'check_startup' parameter has been disabled"
        #     )
        self._check_flags(helptext)

        if use_xauth and not xauth.is_installed():
            raise xauth.NotFoundError()

        self._use_xauth = use_xauth
        self._old_xauth = None
        self._xauth_filename = None
        # self.check_startup = check_startup
        # if check_startup and not fcntl:
        #     self.check_startup = False
        #     log.warning(
        #         "fcntl module can't be imported, 'check_startup' parameter has been disabled"
        #     )
        #     log.warning("fnctl module does not exist on Windows")
        # if self.check_startup:
        #     rp, wp = os.pipe()
        #     fcntl.fcntl(rp, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        #     # TODO: to properly allow to inherit fds to subprocess on
        #     # python 3.2+ the easyprocess needs small fix..
        #     fcntl.fcntl(wp, fcntl.F_SETFD, 0)
        #     self.check_startup_fd = wp
        #     self._check_startup_fd = rp
        # self.proc = EasyProcess(self._cmd())

    def _check_flags(self, helptext):
        pass

    def _cmd(self):
        raise NotImplementedError()

    def _redirect_display(self, on):
        """
        on:
         * True -> set $DISPLAY to virtual screen
         * False -> set $DISPLAY to original screen

        :param on: bool
        """
        d = self.new_display_var if on else self.old_display_var
        if d is None:
            log.debug("unset $DISPLAY")
            try:
                del os.environ["DISPLAY"]
            except KeyError:
                log.warning("$DISPLAY was already unset.")
        else:
            log.debug("$DISPLAY=%s", d)
            os.environ["DISPLAY"] = d

    def start(self):
        """
        start display

        :rtype: self
        """
        if self.is_started:
            raise XStartError(self, "Display was started twice.")
        self.is_started = True

        if self._has_displayfd:
            self._start1()
        else:
            i = 0
            while True:
                try:
                    self._start1()
                    break
                except XStartError:
                    log.warning("start failed %s", i + 1)
                    time.sleep(0.05)
                    i += 1
                    if i >= self._retries:
                        raise XStartError(
                            "No success after %s retries. Last stderr: %s"
                            % (self._retries, self.stderr)
                        )
                finally:
                    self._redirect_display(False)
        self._redirect_display(True)

    def _start1(self):
        if self._has_displayfd:
            # stdout doesn't work on osx -> create own pipe
            rfd, self._pipe_wfd = os.pipe()
        else:
            with _mutex:
                self.display = _search_for_display(randomizer=self._randomizer)
                while self.display in _USED_DISPLAY_NR_LIST:
                    self.display += 1
                self.new_display_var = ":%s" % int(self.display)

                _USED_DISPLAY_NR_LIST.append(self.display)

        self._command = self._cmd() + self._extra_args
        log.debug("command: %s", self._command)

        self._stdout_file = tempfile.TemporaryFile(prefix="stdout_")
        self._stderr_file = tempfile.TemporaryFile(prefix="stderr_")

        if py2() or not self._has_displayfd:
            self._subproc = subprocess.Popen(
                self._command,
                stdout=self._stdout_file,
                stderr=self._stderr_file,
                shell=False,
            )
        else:
            if self._has_displayfd:
                self._subproc = subprocess.Popen(
                    self._command,
                    pass_fds=[self._pipe_wfd],
                    stdout=self._stdout_file,
                    stderr=self._stderr_file,
                    shell=False,
                )
        if self._has_displayfd:
            # rfd = self.subproc.stdout.fileno()
            self.display = int(self._wait_for_pipe_text(rfd))
            os.close(rfd)
            os.close(self._pipe_wfd)
        self.new_display_var = ":%s" % int(self.display)

        if self._use_xauth:
            self._setup_xauth()

        # https://github.com/ponty/PyVirtualDisplay/issues/2
        # https://github.com/ponty/PyVirtualDisplay/issues/14
        self.old_display_var = os.environ.get("DISPLAY", None)

        # wait until X server is active
        start_time = time.time()
        # if self.check_startup:
        #     rp = self._check_startup_fd
        #     display_check = None
        #     rlist, wlist, xlist = select.select((rp,), (), (), _X_START_TIMEOUT)
        #     if rlist:
        #         display_check = os.read(rp, 10).rstrip()
        #     else:
        #         msg = "No display number returned by X server"
        #         raise XStartTimeoutError(msg)
        #     dnbs = str(self.display)
        #     if bytes != str:
        #         dnbs = bytes(dnbs, "ascii")
        #     if display_check != dnbs:
        #         msg = 'Display number "%s" not returned by X server' + str(
        #             display_check
        #         )
        #         raise XStartTimeoutError(msg % self.display)

        if not self._has_displayfd:
            self._redirect_display(True)  # for xdpyinfo
            d = self.new_display_var
            ok = False
            time.sleep(0.05)  # give time for early exit
            while True:
                if not self.is_alive():
                    break

                try:
                    xdpyinfo = EasyProcess(["xdpyinfo"])
                    xdpyinfo.enable_stdout_log = False
                    xdpyinfo.enable_stderr_log = False
                    exit_code = xdpyinfo.call().return_code
                except EasyProcessError:
                    log.warning(
                        "xdpyinfo was not found, X start can not be checked! Please install xdpyinfo!"
                    )
                    time.sleep(_X_START_WAIT)  # old method
                    ok = True
                    break

                if exit_code != 0:
                    pass
                else:
                    log.info('Successfully started X with display "%s".', d)
                    ok = True
                    break

                if time.time() - start_time >= _X_START_TIMEOUT:
                    break
                time.sleep(_X_START_TIME_STEP)
            if not self.is_alive():
                log.warning("process exited early. stderr:%s", self.stderr)
                msg = "Failed to start process: %s"
                raise XStartError(msg % self)
            if not ok:
                msg = 'Failed to start X on display "%s" (xdpyinfo check failed, stderr:[%s]).'
                raise XStartTimeoutError(msg % (d, xdpyinfo.stderr))

        return self

    def _wait_for_pipe_text(self, rfd):
        s = ""
        start_time = time.time()
        while True:
            (rfd_changed_ls, _, _) = select.select([rfd], [], [], 0.1)
            if not self.is_alive():
                raise XStartError(
                    "%s program closed. command: %s stderr: %s"
                    % (self._program, self._command, self.stderr)
                )
            if rfd in rfd_changed_ls:
                c = os.read(rfd, 1)
                if c == b"\n":
                    break
                s += c.decode("ascii")
            if time.time() - start_time >= _X_START_TIMEOUT:
                raise XStartTimeoutError(
                    "No reply from program %s. command:%s"
                    % (self._program, self._command,)
                )
        return s

    def stop(self):
        """
        stop display

        :rtype: self
        """
        if not self.is_started:
            raise XStartError("stop() is called before start().")

        self._redirect_display(False)

        if self.is_alive():
            try:
                try:
                    self._subproc.terminate()
                except AttributeError:
                    os.kill(self._subproc.pid, signal.SIGKILL)
            except OSError as oserror:
                log.debug("exception in terminate:%s", oserror)

            self._subproc.wait()
            self._read_stdout_stderr()
        if self._use_xauth:
            self._clear_xauth()
        return self

    def _read_stdout_stderr(self):
        if self.stdout is None:
            self._stdout_file.seek(0)
            self._stderr_file.seek(0)
            self.stdout = self._stdout_file.read()
            self.stderr = self._stderr_file.read()

            self._stdout_file.close()
            self._stderr_file.close()

            log.debug("stdout=%s", self.stdout)
            log.debug("stderr=%s", self.stderr)

    def _setup_xauth(self):
        """
        Set up the Xauthority file and the XAUTHORITY environment variable.
        """
        handle, filename = tempfile.mkstemp(
            prefix="PyVirtualDisplay.", suffix=".Xauthority"
        )
        self._xauth_filename = filename
        os.close(handle)
        # Save old environment
        self._old_xauth = {}
        self._old_xauth["AUTHFILE"] = os.getenv("AUTHFILE")
        self._old_xauth["XAUTHORITY"] = os.getenv("XAUTHORITY")

        os.environ["AUTHFILE"] = os.environ["XAUTHORITY"] = filename
        cookie = xauth.generate_mcookie()
        xauth.call("add", self.new_display_var, ".", cookie)

    def _clear_xauth(self):
        """
        Clear the Xauthority file and restore the environment variables.
        """
        os.remove(self._xauth_filename)
        for varname in ["AUTHFILE", "XAUTHORITY"]:
            if self._old_xauth[varname] is None:
                del os.environ[varname]
            else:
                os.environ[varname] = self._old_xauth[varname]
        self._old_xauth = None

    def __enter__(self):
        """used by the :keyword:`with` statement"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """used by the :keyword:`with` statement"""
        self.stop()

    def is_alive(self):
        return self.return_code is None

    @property
    def return_code(self):
        rc = self._subproc.poll()
        if rc is not None:
            # proc exited
            self._read_stdout_stderr()
        return rc

    @property
    def pid(self):
        """
        PID (:attr:`subprocess.Popen.pid`)

        :rtype: int
        """
        if self._subproc:
            return self._subproc.pid
