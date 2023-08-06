from clients_core.service_clients import E360ServiceClient
from typing import Any, Dict
from .models import PatientCard


class CardServicePatientCardClient(E360ServiceClient):
    service_endpoint: str = ""
    extra_headers: Dict = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    def post_card(self, card: PatientCard, **kwargs: Any) -> PatientCard:
        """
        Create a new patient card with the provided list of patients Ids

        Returns:
            The newly created card

        Raises:
            clients_core.exceptions.HttpResponseError: on server response errors.
        """
        params = {"userId": self.user_id}
        schema = PatientCard.Schema()
        response = self.client.post('', json=schema.dump(card), params=params, headers=self.service_headers, raises=True, **kwargs).json()
        card.id = response["cardId"]
        card.asset_id = response["assetId"]
        return card
