# paystation

Python client for PayStation payment APIs.

## Features

- Initialize payments through PayStation
- Check transaction status by invoice number
- Supports sandbox and production environments
- Simple request/response flow with JSON responses

## Requirements

- Python 3.10+
- `requests>=2.32.5`

## Installation

From PyPI:

```bash
pip install paystation
```

From source:

```bash
git clone https://github.com/rozari0/paystation.git
cd paystation
pip install .
```

## Quick Start (Sandbox)

Use the following sandbox credentials:

- Merchant ID: `104-1653730183`
- Password: `gamecoderstorepass`

```python
from paystation import PayStation

client = PayStation(
	merchant_id="104-1653730183",
	password="gamecoderstorepass",
	sandbox=True,
)

response = client.initiate_payment(
	invoice_number="INV-1001",
	payment_amount=100.0,
	cust_name="John Doe",
	cust_phone="01700000000",
	cust_email="john@example.com",
	callback_url="https://your-domain.com/paystation/callback",
)

print(response)
```

## Environments

`sandbox=True` uses `https://sandbox.paystation.com.bd`.

`sandbox=False` uses `https://api.paystation.com.bd`.

## API Reference

### `PayStation(merchant_id, password, sandbox=False)`

Create a PayStation client instance.

- `merchant_id` (`str`): PayStation merchant ID
- `password` (`str`): PayStation password
- `sandbox` (`bool`): Set `True` for sandbox

### `initiate_payment(...)`

Initiates a payment.

Required parameters:

- `invoice_number` (`str`): Unique invoice ID
- `payment_amount` (`float`): Amount to be paid
- `cust_name` (`str`): Customer name
- `cust_phone` (`str`): Customer phone
- `cust_email` (`str`): Customer email
- `callback_url` (`str`): URL for payment callback/result

Optional parameters:

- `currency` (`str`, default: `"BDT"`)
- `reference` (`str | None`)
- `cust_address` (`str | None`)
- `checkout_items` (`str | dict | None`)
- `pay_with_charge` (`bool`, default: `False`)
- `emi` (`bool` , default: `False`)
- `opt_a` (`str | dict | None`)
- `opt_b` (`str | dict | None`)
- `opt_c` (`str | dict | None`)

Returns:

- `dict`: Parsed JSON response from PayStation

Example with optional fields:

```python
response = client.initiate_payment(
	invoice_number="INV-1002",
	payment_amount=250.0,
	cust_name="Jane Doe",
	cust_phone="01800000000",
	cust_email="jane@example.com",
	callback_url="https://your-domain.com/paystation/callback",
	currency="BDT",
	reference="ORDER-2026-0001",
	cust_address="Dhaka, Bangladesh",
	checkout_items={"item": "Premium Plan", "qty": 1},
	pay_with_charge=True,
	emi=True,
	opt_a={"source": "web"},
)
```

### `get_transaction_status_by_invoice(invoice_number)`

Checks transaction status for an invoice.

- `invoice_number` (`str`): Invoice used during payment initiation

Returns:

- `dict`: Parsed JSON response from PayStation

```python
status = client.get_transaction_status_by_invoice("INV-1001")
print(status)
```

## Typical Callback Flow

1. You call `initiate_payment` and get a response from PayStation.
2. The customer completes payment on the PayStation page.
3. PayStation sends the result to your `callback_url`.
4. You verify final status by calling `get_transaction_status_by_invoice`.

## Notes

- The client returns `response.json()` directly.
- Add your own handling for timeouts, connection errors, and invalid JSON.
- Keep production credentials private.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
