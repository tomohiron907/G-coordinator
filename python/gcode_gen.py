#!/usr/bin/env python3
"""
G-code generator sidecar: receives {pickle_b64, settings, start_gcode?, end_gcode?}
JSON on stdin, generates G-code, returns {"success": true, "gcode": "..."} on stdout.
"""
import sys
import json
import base64
import pickle
import tempfile
import os
import shutil
import traceback

import gcoordinator as gc
from gcoordinator.gcode_generator import GCode


def main():
    payload    = json.loads(sys.stdin.read())
    pickle_b64 = payload["pickle_b64"]
    settings   = payload["settings"]
    start_txt  = payload.get("start_gcode", "")
    end_txt    = payload.get("end_gcode", "")

    work_dir = tempfile.mkdtemp(prefix="gcoord_gcode_")
    old_dir  = os.getcwd()
    os.chdir(work_dir)

    try:
        # Write settings so GCode class can read .temp_config.json
        tmp_cfg = os.path.join(work_dir, "settings.json")
        with open(tmp_cfg, "w") as f:
            json.dump(settings, f)
        try:
            gc.load_settings(tmp_cfg)
        except Exception:
            pass

        full_object = pickle.loads(base64.b64decode(pickle_b64))
        gcode_obj   = GCode(full_object)

        start_path = os.path.join(work_dir, "start_gcode.txt")
        end_path   = os.path.join(work_dir, "end_gcode.txt")
        with open(start_path, "w") as f:
            f.write(start_txt)
        with open(end_path, "w") as f:
            f.write(end_txt)

        gcode_obj.start_gcode(start_path)
        gcode_obj.end_gcode(end_path)

        out_path = os.path.join(work_dir, "output.gcode")
        gcode_obj.save(out_path)

        with open(out_path, "r") as f:
            gcode_str = f.read()

        result = {"success": True, "gcode": gcode_str}

    except Exception:
        result = {"success": False, "error": traceback.format_exc()}
    finally:
        os.chdir(old_dir)
        shutil.rmtree(work_dir, ignore_errors=True)

    sys.stdout.write(json.dumps(result) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
