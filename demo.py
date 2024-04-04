from pprint import pprint
import requests
import readline

context = {
    "TRANSACTIONS_API_URL": "https://staging-transactions.symphonyda.io",
    "QUORUM_API_URL": "https://staging-quorum.symphonyda.io",
    "ORGANISATION_ID": 0,
    "APPROVER_ID": 0,
    "ASSET_ID": "ETH_TEST5",
    "EXTERNAL_WALLET_ADDRESS": "0x6BF801F0b62F9797e656519b6a3721618Be791a3",
    "VAULT_ACCOUNT_ID1": "11",
    "VAULT_ACCOUNT_ID2": "10",
    "AMOUNT": "0.000001",
    "TRANSACTION_ID": -1,
}


def get_commands():
    return [k for k, v in Commands.__dict__.items() if isinstance(v, staticmethod)]


class Commands:
    @staticmethod
    def create_deposit():
        response = requests.post(
            url=f"{context["TRANSACTIONS_API_URL"]}/transactions/deposit",
            json={
                "organisationId": context["ORGANISATION_ID"],
                "sourceType": "EXTERNAL_WALLET",
                "source": context["EXTERNAL_WALLET_ADDRESS"],
                "destinationType": "VAULT_ACCOUNT",
                "destination": context["VAULT_ACCOUNT_ID1"],
                "assetId": context["ASSET_ID"],
                "operation": "DEPOSIT",
                "amount": context["AMOUNT"],
            },
        ).json()
        pprint(response)
        context["TRANSACTION_ID"] = int(response["transaction"]["id"])
        return

    @staticmethod
    def create_transfer():
        response = requests.post(
            url=f"{context["TRANSACTIONS_API_URL"]}/transactions/create",
            json={
                "organisationId": context["ORGANISATION_ID"],
                "sourceType": "VAULT_ACCOUNT",
                "source": context["VAULT_ACCOUNT_ID1"],
                "destinationType": "VAULT_ACCOUNT",
                "destination": context["VAULT_ACCOUNT_ID2"],
                "assetId": context["ASSET_ID"],
                "operation": "TRANSFER",
                "amount": context["AMOUNT"],
            },
        ).json()
        pprint(response)
        context["TRANSACTION_ID"] = int(response["transaction"]["id"])
        return

    @staticmethod
    def create_withdraw():
        response = requests.post(
            url=f"{context["TRANSACTIONS_API_URL"]}/transactions/create",
            json={
                "organisationId": context["ORGANISATION_ID"],
                "sourceType": "VAULT_ACCOUNT",
                "source": context["VAULT_ACCOUNT_ID2"],
                "destinationType": "EXTERNAL_WALLET",
                "destination": context["EXTERNAL_WALLET_ADDRESS"],
                "assetId": context["ASSET_ID"],
                "operation": "WITHDRAW",
                "amount": context["AMOUNT"],
            },
        ).json()
        pprint(response)
        context["TRANSACTION_ID"] = int(response["transaction"]["id"])
        return

    @staticmethod
    def approve_transaction(transactionId=None):
        transactionId = (
            context["TRANSACTION_ID"] if transactionId is None else int(transactionId)
        )
        if transactionId < 0:
            print("no transaction to approve")
            return
        response = requests.patch(
            url=f"{context["QUORUM_API_URL"]}/approval-log",
            json={
                "requestId": transactionId,
                "approverId": context["APPROVER_ID"],
                "status": "APPROVED",
            },
        ).json()
        pprint(response)
        return

    @staticmethod
    def view_transaction(transactionId=None):
        transactionId = (
            context["TRANSACTION_ID"] if transactionId is None else int(transactionId)
        )
        if transactionId < 0:
            print("no transaction to view")
            return
        response = requests.post(
            url=f"{context["TRANSACTIONS_API_URL"]}/transactions/find-one-by-id",
            json={
                "transactionId": transactionId,
            },
        ).json()
        pprint(response)
        return

    @staticmethod
    def view_transactions():
        response = requests.post(
            url=f"{context["TRANSACTIONS_API_URL"]}/transactions/find-many-by-vault-accounts",
            json={
                "vaultAccountIds": [
                    context["VAULT_ACCOUNT_ID1"],
                ],
            },
        ).json()
        pprint(response)
        return

    @staticmethod
    def get_context():
        pprint(context)

    @staticmethod
    def list_commands():
        pprint(get_commands())
        return


def main():
    commands = get_commands()
    print("available commands:")
    pprint(commands)

    while True:
        user_input = input("enter command: ")
        [command, *args] = user_input.split(" ")
        if command in commands:
            command_function = getattr(Commands, command)
            command_function(*args)
        else:
            print("invalid command")


if __name__ == "__main__":
    main()
