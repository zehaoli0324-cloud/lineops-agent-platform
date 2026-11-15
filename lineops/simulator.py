"""World state produces observations; no fault labels cross the tool boundary."""
import time
from dataclasses import dataclass
from io import BytesIO
from uuid import uuid4
import numpy as np
from PIL import Image, ImageDraw

SCENES = {
    "glue": {"metric": "bead_coverage", "threshold": .90,
             "manual": "Low bead coverage with supply pressure >= .8: inspect outlet; low pressure: inspect supply. Invalid image: restore camera before diagnosis."},
    "filling": {"metric": "fill_fraction", "threshold": .90,
                "manual": "Low fill with supply pressure >= .8: inspect outlet; low pressure: inspect supply. Invalid image: restore camera before diagnosis."},
}
FAULTS = ("normal", "clog", "supply", "camera", "persistent")
ACTIONS = ("pause", "resume", "clean_outlet", "refill_supply", "clean_camera")

@dataclass
class World:
    scene: str = "glue"
    _fault: str = "normal"
    version: int = 0
    running: bool = True

    def __post_init__(self):
        if self.scene not in SCENES or self._fault not in FAULTS:
            raise ValueError("unknown scenario or injection")

    def capture(self):
        fraction = .42 if self._fault in ("clog", "supply", "persistent") else .98
        pressure = .35 if self._fault == "supply" else 1.0
        image = Image.new("RGB", (320, 180), (18, 28, 42))
        draw = ImageDraw.Draw(image)
        if self.scene == "glue":
            draw.rectangle((30, 60, 289, 119), fill=(45, 55, 66))
            draw.rectangle((30, 70, 30+int(260*fraction)-1, 109), fill=(40, 200, 120))
        else:
            draw.rectangle((90, 20, 229, 159), fill=(45, 55, 66))
            draw.rectangle((100, 150-int(120*fraction), 219, 149), fill=(40, 200, 120))
        if self._fault == "camera":
            image = Image.new("RGB", image.size, (100, 100, 100))
        buf = BytesIO(); image.save(buf, format="PNG")
        fid = uuid4().hex
        return {"id": fid, "scene": self.scene, "version": self.version,
                "frame": "/api/frames/"+fid, "captured_at_epoch": time.time(),
                "telemetry": {"supply_pressure": pressure, "running": self.running}}, buf.getvalue()

    def mutate(self, action):
        if action == "pause": self.running = False
        elif action == "resume": self.running = True
        elif action == "clean_outlet" and self._fault == "clog": self._fault = "normal"
        elif action == "refill_supply" and self._fault == "supply": self._fault = "normal"
        elif action == "clean_camera" and self._fault == "camera": self._fault = "normal"
        self.version += 1


def measure(scene, png):
    """Independent pixel segmentation; never consult World or fault labels."""
    a = np.array(Image.open(BytesIO(png)).convert("RGB"))
    # Uniform grey frame fails quality instead of being interpreted as a defect.
    valid = float(a.std()) > 12
    mask = (a[:,:,1] > 150) & (a[:,:,0] < 90) & (a[:,:,2] < 160)
    value = float(mask[70:110,30:290].mean()) if scene == "glue" else float(mask[30:150,100:220].mean())
    return {"metric": SCENES[scene]["metric"], "value": value if valid else None,
            "quality": "valid" if valid else "invalid", "method": "rgb_threshold_v1"}
