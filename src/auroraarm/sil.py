"""Compara o controlador Python com o C compilado, se gcc/clang estiver disponível."""
import ctypes,shutil,subprocess,tempfile
from pathlib import Path
from .codegen import generate
from .controller import PID
def run_sil():
    cc=shutil.which("gcc") or shutil.which("clang")
    if not cc:return {"status":"SKIPPED","reason":"gcc/clang não encontrado"}
    cfile=generate()
    with tempfile.TemporaryDirectory() as td:
        lib=Path(td)/"controller.so"
        subprocess.run([cc,"-shared","-fPIC",str(cfile),"-o",str(lib)],check=True,capture_output=True)
        dll=ctypes.CDLL(str(lib))
        class State(ctypes.Structure): _fields_=[("integral",ctypes.c_float),("prev_error",ctypes.c_float)]
        dll.aa_pid_step.argtypes=[ctypes.POINTER(State),ctypes.c_float,ctypes.c_float]
        dll.aa_pid_step.restype=ctypes.c_float
        py=PID(); cs=State(0,0); errs=[]
        for r,y in ([(1.,0.)]*20+[(1.,.5)]*20+[(0.,.5)]*20):
            errs.append(abs(py.step(r,y)-float(dll.aa_pid_step(ctypes.byref(cs),r,y))))
        return {"status":"PASS" if max(errs)<1e-4 else "FAIL","samples":len(errs),
                "max_abs_error":max(errs),"tolerance":1e-4}
if __name__=="__main__":print(run_sil())
