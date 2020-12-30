"Start Xvfb server. Open xmessage window. Thread safe."

from easyprocess import EasyProcess

from pyvirtualdisplay import Display

# manage_global_env=False is thread safe
with Display(manage_global_env=False) as disp:
    # disp.new_display_var should be used for new processes
    print("disp.new_display_var=" + disp.new_display_var)

    # disp.env() copies global os.environ and adds disp.new_display_var
    print("disp.env()['DISPLAY']=" + disp.env()["DISPLAY"])

    # set $DISPLAY for subprocesses
    with EasyProcess(["xmessage", "-timeout", "1", "hello"], env=disp.env()) as proc:
        proc.wait()
