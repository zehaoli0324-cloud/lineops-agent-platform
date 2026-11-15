"""Optional standalone functional smoke check, not a trained perception model."""
from pathlib import Path
import sys
import numpy as np

def check():
    source=Path(__file__).resolve().parents[1]/'third_party/neuroptica'
    if source.exists():sys.path.insert(0,str(source))
    x=np.linspace(.1,1,8).astype(complex).reshape(8,1)
    try:
        from neuroptica.layers import ReckLayer
        state=np.random.get_state()
        try:
            np.random.seed(7); layer=ReckLayer(8)
        finally:
            np.random.set_state(state)
        out=layer.forward_pass(x)
        # Reference full transfer matrix vs layer implementation, same initialized mesh.
        matrix=layer.mesh.get_transfer_matrix()
        reference=matrix@x
        error=float(np.max(np.abs(out-reference)))
        norm_error=float(abs(np.linalg.norm(out)-np.linalg.norm(x)))
        unitary_error=float(np.max(np.abs(matrix.conj().T@matrix-np.eye(8))))
        if not np.isfinite(error+norm_error+unitary_error) or max(error,norm_error,unitary_error)>1e-9:raise ValueError('optical reference error')
        return {'backend':'neuroptica','ports':8,'max_abs_error':error,'norm_error':norm_error,'unitarity_error':unitary_error,'fallback':False,'scope':'untrained functional transform only'}
    except (ImportError,AttributeError,ValueError) as exc:
        # Explicit identity reference; never claim a different transform is equivalent.
        return {'backend':'numpy_identity','ports':8,'fallback':True,'reason':type(exc).__name__,'scope':'optical backend unavailable; no optical claim','output':x.real.ravel().tolist()}
