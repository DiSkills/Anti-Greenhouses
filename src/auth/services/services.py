import uuid

from src.auth.adapters.repositories.verification import VerificationRepository
from src.auth.domain import model
from src.auth.services import exceptions


# TODO add error when user with this email exists
def registration_request(*, email: str, repository: VerificationRepository) -> None:
    if repository.get(email=email) is not None:
        # TODO send email
        raise exceptions.VerificationExists(
            'Verification with this email already exists, we sent you another email with a code.',
        )

    # TODO send email
    repository.add(verification=model.Verification(email=email, uuid=f'{uuid.uuid4()}'))
    repository.session.commit()
