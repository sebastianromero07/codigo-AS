## Project Structure

```txt
factoring-platform-api/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── auth_routes.py
│   │           ├── invoice_routes.py
│   │           ├── invoice_validation_routes.py
│   │           ├── marketplace_routes.py
│   │           ├── investment_routes.py
│   │           ├── payout_routes.py
│   │           ├── risk_routes.py
│   │           └── notification_routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── constants.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── users/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── companies/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── invoices/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   ├── states.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── invoice_validation/
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── validators.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── risk/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   └── score_calculator.py
│   │   │
│   │   ├── pricing/
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── price_calculator.py
│   │   │
│   │   ├── marketplace/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   └── service.py
│   │   │
│   │   ├── investments/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   └── states.py
│   │   │
│   │   ├── payouts/
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── repository.py
│   │   │   ├── service.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── payments/
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── payment_provider.py
│   │   │
│   │   └── notifications/
│   │       ├── schemas.py
│   │       ├── service.py
│   │       └── templates.py
│   │
│   ├── integrations/
│   │   ├── sunat/
│   │   │   ├── client.py
│   │   │   ├── schemas.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── bank/
│   │   │   ├── client.py
│   │   │   ├── schemas.py
│   │   │   └── exceptions.py
│   │   │
│   │   └── email/
│   │       ├── client.py
│   │       └── schemas.py
│   │
│   ├── infrastructure/
│   │   ├── cache/
│   │   │   ├── redis.py
│   │   │   └── keys.py
│   │   │
│   │   ├── storage/
│   │   │   ├── local_storage.py
│   │   │   └── s3_storage.py
│   │   │
│   │   └── queue/
│   │       ├── publisher.py
│   │       └── consumer.py
│   │
│   ├── jobs/
│   │   ├── invoice_expiration_job.py
│   │   ├── payout_reconciliation_job.py
│   │   └── notification_job.py
│   │
│   └── shared/
│       ├── enums.py
│       ├── pagination.py
│       ├── responses.py
│       ├── utils.py
│       └── date_utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_invoices.py
│   ├── test_invoice_validation.py
│   ├── test_marketplace.py
│   ├── test_investments.py
│   ├── test_payouts.py
│   └── test_risk.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── scripts/
│   ├── create_superuser.py
│   ├── seed_data.py
│   └── run_dev.py
│
├── docs/
│   ├── architecture.md
│   ├── api_flows.md
│   └── business_rules.md
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Main Modules

| Module | Responsibility |
|---|---|
| `auth` | User login, authentication, JWT tokens and permissions. |
| `users` | User management for companies, investors and admins. |
| `companies` | Company/entity information and fiscal data. |
| `invoices` | Invoice upload, invoice data and invoice lifecycle states. |
| `invoice_validation` | Invoice validation, duplicate checks and SUNAT validation. |
| `risk` | Entity risk scoring and risk evaluation. |
| `pricing` | Price, profit and liquid amount calculation. |
| `marketplace` | Invoice publication and marketplace listing. |
| `investments` | Investor purchase flow and investment lifecycle. |
| `payouts` | Seller and investor payout management. |
| `payments` | Payment processing with external bank provider. |
| `notifications` | Email, push or system notifications. |

## Architecture Style

This project follows a modular monolith architecture using FastAPI.

Each business module is organized using the following structure:

```txt
module_name/
├── models.py
├── schemas.py
├── repository.py
├── service.py
└── exceptions.py
```

### File Responsibility

| File | Purpose |
|---|---|
| `models.py` | SQLAlchemy database models. |
| `schemas.py` | Pydantic request and response schemas. |
| `repository.py` | Database access logic. |
| `service.py` | Business rules and use cases. |
| `exceptions.py` | Module-specific exceptions. |
| `states.py` | State definitions for invoices or investments. |

## Main Business Flow

```txt
Company uploads invoice
        ↓
Invoice is validated
        ↓
SUNAT validation is executed
        ↓
Risk score is calculated
        ↓
Price and profit are calculated
        ↓
Invoice is published in marketplace
        ↓
Investor buys invoice
        ↓
Seller receives payout
        ↓
Investor receives payout after collection
```

## Suggested Tech Stack

```txt
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Redis
JWT
Pytest
Docker
```

## Observaciones de Arquitectura

En el diagrama actual, el `Invoice Upload Service` recibe la factura enviada por la empresa. Sin embargo, no se especifica dónde se almacena el archivo de la factura.

El componente `Invoice state cache` no debe interpretarse como almacenamiento principal de la factura, ya que solo representa el estado de la factura, por ejemplo: subida, validada, publicada o pendiente de pago.

Para completar el diseño, se debería definir un componente de almacenamiento para el archivo de la factura y otro para la metadata,por ejemplo un almacenamiento de objetos separado de la base de datos relacional. 

- **Falta un servicio de validación de la Empresa A (cedente).** Antes de aceptar cualquier factura, debe existir un paso que valide la identidad y legitimidad de la empresa que la sube (RUC activo, no estar en listas restrictivas).
- **Falta el `Invoice Validation Service` antes del `Invoice Upload`.** La factura se publica antes de validarse. El orden correcto es: subir → validar (SUNAT, formato, no anulada) → recién entonces publicar.
- **El `Invoice state cache` está de más.** No es una cache real, es simplemente el estado actual de la factura (columna `status` en la tabla `invoices`). Agregarlo como bloque en el flujo confunde y sugiere infraestructura innecesaria.
- **El flujo de `Invoice Pay` está invertido.** Se reparte a inversionistas antes de confirmar el cobro. El orden correcto es:
  1. La Entidad B(pagador) realiza el pago.
  2. El sistema confirma que el dinero ingresó al banco.
  3. Recién entonces se ejecuta el payout al inversor (capital + ganancia) y al cedente si corresponde.
- En este punto, se observa que no se está representando claramente el ingreso de dinero desde la Entidad B, lo cual es crítico dentro del flujo, ya que ese pago es el que permite cerrar el ciclo del factoring. 

- **Faltan estados de pago pendiente, impago y mora.** El flujo actual asume el camino feliz. Se debe contemplar:
  - `PENDING_PAYMENT`: la factura está fondeada y se espera el pago en la fecha de vencimiento.
  - `OVERDUE / IN_MORA`: pasó la fecha estimada y el pagador no ha pagado.
  - `DEFAULTED`: impago confirmado, se dispara el proceso de protesto/cobranza.

- Además, sería importante considerar un componente o proceso de cobranzas que gestione estos escenarios y haga seguimiento a los pagos de la Entidad B. 

### No se especifica claramente a quién se está pagando

El diagrama muestra servicios de pago, pero no indica claramente quién recibe el dinero.

Según el caso de uso:

```txt
Seller Payout Service   → Entity C paga a Company A
Investor Payout Service → Entity C paga a Investor D
Invoice Pay             → Company B paga a Entity C
```

### Los pagos parecen ejecutarse al mismo tiempo

El diagrama puede dar la impresión de que el pago al cedente y el pago al inversionista ocurren en paralelo.

Sin embargo, en el caso de uso factoring, los pagos deben ocurrir en momentos diferentes.

El flujo correcto debería ser:

```txt
1. Investor D compra la factura.
2. Entity C paga a Company A un monto menor para darle liquidez.
3. Company B paga la factura a Entity C.
4. Entity C paga a Investor D el capital invertido más la ganancia.
```

---
- Adicionalmente, se debería considerar que la plataforma informe a la Entidad B sobre la cesión de la factura, ya que este paso es importante dentro del proceso de negocio y no se encuentra representado en el diagrama. 
- Se observa también que no se representa explícitamente el momento en que la Entidad C notifica a la Entidad B sobre la cesión de la factura, lo cual es relevante desde el punto de vista operativo y legal dentro del proceso de factoring. 

### Falta representar qué ocurre si Company B no paga

El diagrama no muestra un flujo alternativo para los casos en los que el pagador no cumple con el pago de la factura.

Se debería contemplar un flujo para:

```txt
- Retraso en el pago
- Mora
- Impago
- Cobranza
- Protesto o recuperación
```

- Adicionalmente, no se evidencia un módulo o servicio encargado específicamente de gestionar la interacción con la Entidad B (deudor), tanto para el cobro como para el seguimiento del pago, lo cual es clave dentro del flujo completo del negocio.
- También se observa una posible inconsistencia entre la complejidad de la arquitectura propuesta (uso de microservicios, eventos, etc.) y la infraestructura estimada, ya que se menciona que sería suficiente un solo servidor, lo cual podría no ser coherente con ese nivel de diseño.
- Finalmente, no queda completamente claro cómo se gestiona el cálculo de la ganancia (porcentaje Y%) dentro del modelo de datos, específicamente cómo se diferencia la comisión de la plataforma respecto a la rentabilidad del inversionista.



