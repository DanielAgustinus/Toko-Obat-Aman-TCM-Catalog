"""
database.py — Layer penyimpanan data menggunakan JSON file
Untuk production, bisa diganti dengan SQLite/PostgreSQL
"""
import json
from pathlib import Path
from models import Herb, HerbCreate, HerbUpdate, SearchQuery

DATA_DIR = Path(__file__).parent / "data"
HERBS_FILE = DATA_DIR / "herbs.json"


def _load_herbs() -> list[dict]:
    """Baca semua data herb dari file JSON"""
    if not HERBS_FILE.exists():
        return []
    with open(HERBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_herbs(herbs: list[dict]) -> None:
    """Simpan data herb ke file JSON"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HERBS_FILE, "w", encoding="utf-8") as f:
        json.dump(herbs, f, ensure_ascii=False, indent=2)


def get_all_herbs() -> list[Herb]:
    """Ambil semua herb"""
    raw = _load_herbs()
    return [Herb(**h) for h in raw]


def get_herb_by_id(herb_id: int) -> Herb | None:
    """Ambil satu herb berdasarkan ID"""
    for h in _load_herbs():
        if h["id"] == herb_id:
            return Herb(**h)
    return None


def search_herbs(query: SearchQuery) -> list[Herb]:
    """Cari herb berdasarkan berbagai filter"""
    results = get_all_herbs()

    if query.keyword:
        kw = query.keyword.lower()
        results = [
            h for h in results
            if kw in h.nama_indonesia.lower()
            or kw in h.nama_chinese
            or kw in h.nama_pinyin.lower()
            or kw in (h.nama_latin or "").lower()
            or kw in h.khasiat.lower()
            or kw in h.deskripsi.lower()
        ]

    if query.kategori:
        results = [h for h in results if h.kategori == query.kategori]

    if query.sifat:
        results = [h for h in results if h.sifat == query.sifat]

    if query.rasa:
        results = [h for h in results if query.rasa in h.rasa]

    if query.min_harga is not None:
        results = [h for h in results if h.harga >= query.min_harga]

    if query.max_harga is not None:
        results = [h for h in results if h.harga <= query.max_harga]

    if query.hanya_stok:
        results = [h for h in results if h.stok > 0]

    if query.hanya_populer:
        results = [h for h in results if h.populer]

    return results


def create_herb(data: HerbCreate) -> Herb:
    """Tambah herb baru"""
    herbs_raw = _load_herbs()
    new_id = max((h["id"] for h in herbs_raw), default=0) + 1
    new_herb = Herb(id=new_id, **data.model_dump())
    herbs_raw.append(new_herb.model_dump())
    _save_herbs(herbs_raw)
    return new_herb


def update_herb(herb_id: int, data: HerbUpdate) -> Herb | None:
    """Update herb yang sudah ada"""
    herbs_raw = _load_herbs()
    for i, h in enumerate(herbs_raw):
        if h["id"] == herb_id:
            update_data = data.model_dump(exclude_none=True)
            herbs_raw[i].update(update_data)
            _save_herbs(herbs_raw)
            return Herb(**herbs_raw[i])
    return None


def delete_herb(herb_id: int) -> bool:
    """Hapus herb berdasarkan ID"""
    herbs_raw = _load_herbs()
    original_len = len(herbs_raw)
    herbs_raw = [h for h in herbs_raw if h["id"] != herb_id]
    if len(herbs_raw) < original_len:
        _save_herbs(herbs_raw)
        return True
    return False


def get_categories_summary() -> dict:
    """Ringkasan jumlah herb per kategori"""
    herbs = get_all_herbs()
    summary = {}
    for h in herbs:
        cat = h.kategori.value
        summary[cat] = summary.get(cat, 0) + 1
    return summary
