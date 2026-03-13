import requests
from typing import Dict, Any, Optional


class PayStation:
    def __init__(self, merchant_id: str, password: str, sandbox: bool = False):
        """
        Initialize the PayStation Payment Gateway Client.

        :param merchant_id: Merchant ID provided by PayStation
        :param password: Password provided by PayStation
        :param sandbox: Set to True to use the sandbox environment
        """
        self.merchant_id = merchant_id
        self.password = password
        self.sandbox = sandbox

        if self.sandbox:
            self.base_url = "https://sandbox.paystation.com.bd"
        else:
            self.base_url = "https://api.paystation.com.bd"

    def initiate_payment(
        self,
        invoice_number: str,
        payment_amount: float,
        cust_name: str,
        cust_phone: str,
        cust_email: str,
        callback_url: str,
        currency: str = "BDT",
        reference: Optional[str] = None,
        cust_address: Optional[str] = None,
        checkout_items: Optional[str | Dict[Any, Any]] = None,
        pay_with_charge: Optional[bool] = False,
        emi: Optional[int] = None,
        opt_a: Optional[str | Dict[Any, Any]] = None,
        opt_b: Optional[str | Dict[Any, Any]] = None,
        opt_c: Optional[str | Dict[Any, Any]] = None,
    ) -> Dict[str, Any]:
        """_summary_

        Args:
            invoice_number (str): Unique invoice number for the transaction.
            payment_amount (float): Transaction amount.
            cust_name (str): Customer's full name.
            cust_phone (str): Customer's phone number.
            cust_email (str): Customer's email address.
            callback_url (str): URL to which PayStation will send the transaction result.
            currency (str, optional): Currency code for the transaction. Defaults to "BDT".
            reference (Optional[str], optional): Reference number for the transaction. Defaults to None.
            cust_address (Optional[str], optional): Customer's address. Defaults to None.
            checkout_items (Optional[str  |  Dict[Any, Any]], optional): Items in the checkout. Defaults to None.
            pay_with_charge (Optional[bool], optional): Whether to include a charge. Defaults to False.
            emi (Optional[int], optional): EMI installment count. Defaults to None.
            opt_a (Optional[str  |  Dict[Any, Any]], optional): Optional field A. Defaults to None.
            opt_b (Optional[str  |  Dict[Any, Any]], optional): Optional field B. Defaults to None.
            opt_c (Optional[str  |  Dict[Any, Any]], optional): Optional field C. Defaults to None.

        Returns:
            Dict[str, Any]: Response from PayStation API with transaction details and status.
        """

        endpoint = f"{self.base_url}/initiate-payment"

        payload = {
            "merchantId": self.merchant_id,
            "password": self.password,
            "invoice_number": invoice_number,
            "currency": currency,
            "payment_amount": payment_amount,
            "cust_name": cust_name,
            "cust_phone": cust_phone,
            "cust_email": cust_email,
            "callback_url": callback_url,
        }

        if reference:
            payload["reference"] = reference
        if cust_address:
            payload["cust_address"] = cust_address
        if checkout_items:
            payload["checkout_items"] = checkout_items
        if pay_with_charge is not None:
            payload["pay_with_charge"] = int(pay_with_charge)
        if emi is not None:
            payload["emi"] = emi
        if opt_a:
            payload["opt_a"] = opt_a
        if opt_b:
            payload["opt_b"] = opt_b
        if opt_c:
            payload["opt_c"] = opt_c

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        response = requests.post(endpoint, data=payload, headers=headers)
        return response.json()

    def get_transaction_status_by_invoice(self, invoice_number: str) -> Dict[str, Any]:
        """
        Check the status of a transaction using the Invoice Number.
        """
        endpoint = f"{self.base_url}/transaction-status"

        headers = {
            "merchantId": self.merchant_id,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        payload = {"invoice_number": invoice_number}

        response = requests.post(endpoint, data=payload, headers=headers)
        return response.json()

    def get_transaction_status_by_trx_id(self, trx_id: str) -> Dict[str, Any]:
        """
        Check the status of a transaction using the Transaction ID (v2 API).
        """
        endpoint = f"{self.base_url}/v2/transaction-status"

        headers = {
            "merchantId": self.merchant_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {"trxId": trx_id}

        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
