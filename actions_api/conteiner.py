from logging import getLogger
from dependency_injector import containers, providers

from extensions import session
from modules.updater import UserUpdater


class ApplicationContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            'actions.confirm',
            'actions.unsubscribe'
        ]
    )

    logger = providers.Singleton(getLogger)

    session = providers.Singleton(session)

    user_updater = providers.Factory(
        UserUpdater,
        session=session,
        logger=logger
    )
