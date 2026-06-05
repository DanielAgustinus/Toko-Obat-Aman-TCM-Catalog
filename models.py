"""
models.py — Pydantic models untuk katalog obat tradisional Chinese
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class KategoriObat(str, Enum):
    """Kategori utama obat tradisional Chinese"""
    HERBAL = "herbal"
    AKAR = "akar"
    BUNGA = "bunga"
    DAUN = "daun"
    BIJI = "biji"
    KULIT_KAYU = "kulit_kayu"
    JAMUR = "jamur"
    MINERAL = "mineral"
    HEWAN = "hewan"
    CAMPURAN = "campuran"
    BUAH = "buah"


class SifatObat(str, Enum):
    """Sifat (性) dalam TCM"""
    PANAS = "panas"       # 热
    HANGAT = "hangat"     # 温
    NETRAL = "netral"     # 平
    SEJUK = "sejuk"       # 凉
    DINGIN = "dingin"     # 寒


class RasaObat(str, Enum):
    """Lima Rasa (五味) dalam TCM"""
    MANIS = "manis"       # 甘
    PAHIT = "pahit"       # 苦
    PEDAS = "pedas"       # 辛
    ASAM = "asam"         # 酸
    ASIN = "asin"         # 咸


class Herb(BaseModel):
    """Model utama untuk setiap item obat dalam katalog"""
    id: int
    nama_indonesia: str = Field(..., description="Nama dalam Bahasa Indonesia")
    nama_chinese: str = Field(..., description="Nama dalam Bahasa Mandarin (汉字)")
    nama_pinyin: str = Field(..., description="Nama dalam Pinyin")
    nama_latin: Optional[str] = Field(None, description="Nama Latin / ilmiah")
    kategori: KategoriObat
    sifat: SifatObat
    rasa: list[RasaObat] = Field(default_factory=list)
    meridian: list[str] = Field(default_factory=list, description="Meridian yang dipengaruhi")
    khasiat: str = Field(..., description="Khasiat / manfaat utama")
    deskripsi: str = Field(..., description="Deskripsi lengkap")
    cara_pakai: str = Field("", description="Cara penggunaan")
    dosis: str = Field("", description="Dosis yang dianjurkan")
    peringatan: str = Field("", description="Peringatan / kontraindikasi")
    harga: float = Field(..., ge=0, description="Harga per unit (Rp)")
    satuan: str = Field("gram", description="Satuan jual (gram, bungkus, botol)")
    stok: int = Field(0, ge=0, description="Jumlah stok tersedia")
    gambar: str = Field("", description="Path ke file gambar")
    populer: bool = Field(False, description="Tandai sebagai produk populer")


class HerbCreate(BaseModel):
    """Model untuk membuat herb baru (tanpa ID)"""
    nama_indonesia: str
    nama_chinese: str
    nama_pinyin: str
    nama_latin: Optional[str] = None
    kategori: KategoriObat
    sifat: SifatObat
    rasa: list[RasaObat] = []
    meridian: list[str] = []
    khasiat: str
    deskripsi: str
    cara_pakai: str = ""
    dosis: str = ""
    peringatan: str = ""
    harga: float = 0
    satuan: str = "gram"
    stok: int = 0
    gambar: str = ""
    populer: bool = False


class HerbUpdate(BaseModel):
    """Model untuk update parsial"""
    nama_indonesia: Optional[str] = None
    nama_chinese: Optional[str] = None
    nama_pinyin: Optional[str] = None
    nama_latin: Optional[str] = None
    kategori: Optional[KategoriObat] = None
    sifat: Optional[SifatObat] = None
    rasa: Optional[list[RasaObat]] = None
    meridian: Optional[list[str]] = None
    khasiat: Optional[str] = None
    deskripsi: Optional[str] = None
    cara_pakai: Optional[str] = None
    dosis: Optional[str] = None
    peringatan: Optional[str] = None
    harga: Optional[float] = None
    satuan: Optional[str] = None
    stok: Optional[int] = None
    gambar: Optional[str] = None
    populer: Optional[bool] = None


class SearchQuery(BaseModel):
    """Model untuk pencarian"""
    keyword: str = ""
    kategori: Optional[KategoriObat] = None
    sifat: Optional[SifatObat] = None
    rasa: Optional[RasaObat] = None
    min_harga: Optional[float] = None
    max_harga: Optional[float] = None
    hanya_stok: bool = False
    hanya_populer: bool = False
