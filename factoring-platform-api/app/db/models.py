import enum
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    business_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    ruc_emisor: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    serie: Mapped[str] = mapped_column(String(10), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    moneda: Mapped[str] = mapped_column(String(3), nullable=False, default="PEN")
    fecha_emision: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_vencimiento: Mapped[date] = mapped_column(Date, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="uploaded")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False, default="investor")
    balance: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), nullable=False, default=Decimal("0.00")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="wallet", cascade="all, delete-orphan"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wallet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    invoice_id: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    transaction_type: Mapped[str] = mapped_column(
        String(30), nullable=False, default="purchase"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")
class UserType(str, enum.Enum):
    ENTITY = "entity"
    INVESTOR = "investor"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, default=UserType.INVESTOR) # 'entity' o 'investor'