"""
main.py — Aplikasi utama FastAPI untuk Katalog Obat Tradisional Chinese
"""
from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import Optional

from models import (
    Herb, HerbCreate, HerbUpdate, SearchQuery,
    KategoriObat, SifatObat, RasaObat,
)
from database import (
    get_all_herbs, get_herb_by_id, search_herbs,
    create_herb, update_herb, delete_herb, get_categories_summary,
)

# ── Inisialisasi App ──────────────────────────────────────────────
app = FastAPI(
    title="Toko Obat Aman — 天安堂",
    description="Katalog Online Toko Obat Aman",
    version="1.0.0",
)

# ── Static files & Templates ─────────────────────────────────────
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "images").mkdir(exist_ok=True)
(STATIC_DIR / "css").mkdir(exist_ok=True)
(STATIC_DIR / "js").mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# ══════════════════════════════════════════════════════════════════
#  HALAMAN WEB (HTML)
# ══════════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def halaman_utama(request: Request):
    """Halaman utama — tampilkan produk populer & ringkasan"""
    herbs = get_all_herbs()
    populer = [h for h in herbs if h.populer]
    summary = get_categories_summary()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "herbs_populer": populer,
        "total_herbs": len(herbs),
        "summary": summary,
    })


@app.get("/katalog", response_class=HTMLResponse)
async def halaman_katalog(
    request: Request,
    q: str = "",
    kategori: Optional[str] = None,
    sifat: Optional[str] = None,
):
    """Halaman katalog — daftar lengkap dengan filter"""
    query = SearchQuery(
        keyword=q,
        kategori=KategoriObat(kategori) if kategori else None,
        sifat=SifatObat(sifat) if sifat else None,
    )
    herbs = search_herbs(query)
    return templates.TemplateResponse("katalog.html", {
        "request": request,
        "herbs": herbs,
        "query": q,
        "kategori_aktif": kategori,
        "sifat_aktif": sifat,
        "kategori_list": [e.value for e in KategoriObat],
        "sifat_list": [e.value for e in SifatObat],
    })


@app.get("/herb/{herb_id}", response_class=HTMLResponse)
async def halaman_detail(request: Request, herb_id: int):
    """Halaman detail satu produk"""
    herb = get_herb_by_id(herb_id)
    if not herb:
        return templates.TemplateResponse("404.html", {
            "request": request,
        }, status_code=404)
    return templates.TemplateResponse("detail.html", {
        "request": request,
        "herb": herb,
    })


@app.get("/tentang", response_class=HTMLResponse)
async def halaman_tentang(request: Request):
    """Halaman tentang toko"""
    return templates.TemplateResponse("tentang.html", {
        "request": request,
    })


# ══════════════════════════════════════════════════════════════════
#  REST API (JSON) — untuk integrasi & pengembangan lanjut
# ══════════════════════════════════════════════════════════════════

@app.get("/api/herbs", response_model=list[Herb], tags=["API"])
async def api_list_herbs(
    q: str = "",
    kategori: Optional[KategoriObat] = None,
    sifat: Optional[SifatObat] = None,
    rasa: Optional[RasaObat] = None,
    min_harga: Optional[float] = None,
    max_harga: Optional[float] = None,
    hanya_stok: bool = False,
    hanya_populer: bool = False,
):
    """API: Daftar semua herb dengan filter"""
    query = SearchQuery(
        keyword=q,
        kategori=kategori,
        sifat=sifat,
        rasa=rasa,
        min_harga=min_harga,
        max_harga=max_harga,
        hanya_stok=hanya_stok,
        hanya_populer=hanya_populer,
    )
    return search_herbs(query)


@app.get("/api/herbs/{herb_id}", response_model=Herb, tags=["API"])
async def api_get_herb(herb_id: int):
    """API: Detail satu herb"""
    herb = get_herb_by_id(herb_id)
    if not herb:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Herb tidak ditemukan")
    return herb


@app.post("/api/herbs", response_model=Herb, tags=["API"])
async def api_create_herb(data: HerbCreate):
    """API: Tambah herb baru"""
    return create_herb(data)


@app.put("/api/herbs/{herb_id}", response_model=Herb, tags=["API"])
async def api_update_herb(herb_id: int, data: HerbUpdate):
    """API: Update herb"""
    herb = update_herb(herb_id, data)
    if not herb:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Herb tidak ditemukan")
    return herb


@app.delete("/api/herbs/{herb_id}", tags=["API"])
async def api_delete_herb(herb_id: int):
    """API: Hapus herb"""
    if not delete_herb(herb_id):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Herb tidak ditemukan")
    return {"message": f"Herb {herb_id} berhasil dihapus"}


@app.get("/api/summary", tags=["API"])
async def api_summary():
    """API: Ringkasan katalog"""
    herbs = get_all_herbs()
    return {
        "total_produk": len(herbs),
        "total_stok": sum(h.stok for h in herbs),
        "kategori": get_categories_summary(),
        "produk_populer": len([h for h in herbs if h.populer]),
    }


# ── Jalankan Server ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
