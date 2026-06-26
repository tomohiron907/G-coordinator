#!/usr/bin/env python3
"""
Runner sidecar: receives {"code": "...", "settings": {...}} JSON on stdin,
executes user code, and returns preview data + pickle on stdout.
"""
import sys
import json
import os
import base64
import io
import traceback
import tempfile

import msgpack
import gcoordinator as gc


def main():
    payload  = json.loads(sys.stdin.read())
    code     = payload["code"]
    settings = payload["settings"]

    nozzle_size = (settings.get("Print", {})
                          .get("nozzle", {})
                          .get("nozzle_diameter", 0.4))

    work_dir     = tempfile.mkdtemp(prefix="gcoord_")
    msgpack_file = os.path.join(work_dir, "export.msgpack")
    pickle_file  = os.path.join(work_dir, "export.pkl")
    old_dir      = os.getcwd()
    os.chdir(work_dir)

    try:
        tmp_cfg = os.path.join(work_dir, "settings.json")
        with open(tmp_cfg, "w") as f:
            json.dump(settings, f)
        try:
            gc.load_settings(tmp_cfg)
        except Exception:
            pass

        os.environ["GCOORDINATOR_EXPORT_FILE"] = msgpack_file
        os.environ["GCOORDINATOR_PICKLE_FILE"]  = pickle_file

        buf        = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        error_msg  = None

        try:
            exec(compile(code, "<user_code>", "exec"), {"__name__": "__main__"})
        except SystemExit:
            pass
        except Exception:
            error_msg = traceback.format_exc()
        finally:
            sys.stdout = old_stdout
            os.environ.pop("GCOORDINATOR_EXPORT_FILE", None)
            os.environ.pop("GCOORDINATOR_PICKLE_FILE",  None)

        captured_stdout = buf.getvalue()

        if error_msg:
            result = {"success": False, "stdout": captured_stdout, "error": error_msg}
        elif not os.path.exists(msgpack_file):
            result = {
                "success": False,
                "stdout":  captured_stdout,
                "error":   "No gc.gui_export() or gc.preview() call detected.",
            }
        else:
            with open(msgpack_file, "rb") as f:
                data = msgpack.unpackb(f.read(), raw=False)
            with open(pickle_file, "rb") as f:
                pickle_b64 = base64.b64encode(f.read()).decode()

            result = {
                "success":             True,
                "stdout":              captured_stdout,
                "path_lengths":        data["path_lengths"],
                "coords_b64":          base64.b64encode(data["coords"]).decode(),
                "travel_path_lengths": data["travel_path_lengths"],
                "travel_coords_b64":   base64.b64encode(data["travel_coords"]).decode(),
                "nozzleSize":          nozzle_size,
                "pickle_b64":          pickle_b64,
            }

    finally:
        os.chdir(old_dir)
        import shutil
        shutil.rmtree(work_dir, ignore_errors=True)

    sys.stdout.write(json.dumps(result) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
