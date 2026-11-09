"""
Monitorea Downloads y mueve modelos automáticamente a ComfyUI en E:
Ejecutar antes de descargar modelos: python mover_modelos.py
"""
import time, shutil, os
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
BASE = Path(r"E:\Github\ComfyUI\models")

RULES = {
    "checkpoints":        ["checkpoint"],
    "loras":              ["lora", "adapter"],
    "text_encoders":      ["t5", "clip", "encoder", "gemma", "llava", "bert"],
    "vae":                ["vae"],
    "diffusion_models":   ["unet", "diffusion", "transformer", "multiview", "convrot", "pixal3d", "ltx"],
    "controlnet":         ["controlnet", "control_"],
    "upscale_models":     ["upscale", "esrgan", "realesr"],
    "background_removal": ["birefnet", "rembg", "isnet"],
    "clip_vision":        ["dino", "clip_vision", "siglip"],
}
EXTS = {".safetensors", ".gguf", ".pt", ".bin", ".ckpt"}

def dest_for(name):
    low = name.lower()
    for folder, keywords in RULES.items():
        if any(k in low for k in keywords):
            return BASE / folder
    return BASE / "checkpoints"  # fallback

moved = set()
print(f"Monitoreando {DOWNLOADS} ...")
print("Ctrl+C para detener\n")

while True:
    for f in DOWNLOADS.iterdir():
        if (f.suffix in EXTS
                and f.stat().st_size > 50_000_000
                and not f.name.endswith(".crdownload")
                and f.name not in moved):
            dest = dest_for(f.name)
            dest.mkdir(exist_ok=True)
            print(f"Moviendo {f.name} -> {dest.name}/")
            shutil.move(str(f), dest / f.name)
            moved.add(f.name)
            print(f"  OK: {f.name}")
    time.sleep(10)
