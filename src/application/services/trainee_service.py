from uuid import UUID, uuid4
from datetime import datetime, timezone

# --- 1. Imports from src.core.domain ---
from src.core.domain import TraineeTechnologyState, LearningSessionLog, LearningState

# --- 2. Imports from src.core.exceptions ---
from src.core.exceptions import (
    TraineeTechnologyStateNotFoundError,
    LearningSessionAlreadyInProgressError,
    InvalidLearningStateTransitionError,
    NoActiveLearningSessionError,
)

# --- 3. Imports from src.application.repositories ---
from src.application.repositories import (
    ITraineeTechnologyStateRepository,
    ILearningSessionLogRepository,
)


class TraineeService:
    """
    Manages business logic related to trainee learning progression,
    such as starting/stopping learning sessions and moving tasks
    between states.
    """

    def __init__(
        self,
        trainee_tech_state_repo: ITraineeTechnologyStateRepository,
        learning_session_log_repo: ILearningSessionLogRepository,
    ):
        """
        Initializes the service with repository dependencies (Dependency Injection).

        :param trainee_tech_state_repo: The repository for trainee
                                        technology states.
        :param learning_session_log_repo: The repository for learning
                                          session logs.
        """
        self._trainee_tech_state_repo = trainee_tech_state_repo
        self._learning_session_log_repo = learning_session_log_repo

    async def start_learning_technology(
        self, trainee_id: UUID, technology_id: UUID
    ) -> TraineeTechnologyState:
        """
        Starts a new learning session for a specific technology.

        Business Rules:
        1. A trainee cannot have more than one active learning session.
        2. A new session can only be started if the technology state is
           'PLANNED' or 'READY_FOR_REVIEW'.

        :param trainee_id: The ID of the trainee.
        :param technology_id: The ID of the technology to learn.
        :raises LearningSessionAlreadyInProgressError: If an active session
                                                      already exists.
        :raises TraineeTechnologyStateNotFoundError: If the TraineeTechnologyState
                                                    is not found.
        :raises InvalidLearningStateTransitionError: If the current state
                                                    is not PLANNED or
                                                    READY_FOR_REVIEW.
        :return: The updated TraineeTechnologyState.
        """
        # 1. Check for any other active session
        active_session = (
            await self._learning_session_log_repo.find_active_session_by_trainee_id(
                trainee_id
            )
        )
        if active_session:
            raise LearningSessionAlreadyInProgressError(
                f"Trainee {trainee_id} already has an active session "
                f"for state {active_session.trainee_technology_state_id}."
            )

        # 2. Get the target technology state
        tech_state = await self._trainee_tech_state_repo.find_by_trainee_and_technology(
            trainee_id, technology_id
        )
        if not tech_state:
            raise TraineeTechnologyStateNotFoundError(
                f"TraineeTechnologyState not found for trainee {trainee_id} "
                f"and technology {technology_id}."
            )

        # 3. Validate state transition
        allowed_states = (LearningState.PLANNED, LearningState.READY_FOR_REVIEW)
        if tech_state.state not in allowed_states:
            raise InvalidLearningStateTransitionError(
                from_state=tech_state.state.value,
                to_state=LearningState.IN_PROGRESS.value,
            )

        # 4. Create new immutable state
        updated_tech_state = tech_state.model_copy(
            update={"state": LearningState.IN_PROGRESS}
        )

        # 5. Create new learning log
        new_log = LearningSessionLog(
            id=uuid4(),
            trainee_technology_state_id=tech_state.id,
            start_time=datetime.now(timezone.utc),
            end_time=None,
        )

        # 6. Persist changes
        await self._learning_session_log_repo.add(new_log)
        await self._trainee_tech_state_repo.update(updated_tech_state)

        return updated_tech_state

    async def stop_learning_technology(
        self, trainee_id: UUID, technology_id: UUID
    ) -> TraineeTechnologyState:
        """
        Stops the active learning session for a technology and marks
        it as 'READY_FOR_REVIEW'.

        :param trainee_id: The ID of the trainee.
        :param technology_id: The ID of the technology.
        :raises NoActiveLearningSessionError: If no active session is found.
        :raises TraineeTechnologyStateNotFoundError: If the TraineeTechnologyState
                                                    is not found.
        :raises InvalidLearningStateTransitionError: If the state is not
                                                    IN_PROGRESS.
        :raises LearningSessionAlreadyInProgressError: If the active session is for a
                                             different technology.
        :return: The updated TraineeTechnologyState.
        """
        # 1. Get the target technology state
        tech_state = await self._trainee_tech_state_repo.find_by_trainee_and_technology(
            trainee_id, technology_id
        )
        if not tech_state:
            raise TraineeTechnologyStateNotFoundError(
                f"TraineeTechnologyState not found for trainee {trainee_id} "
                f"and technology {technology_id}."
            )

        # 2. Validate state transition
        if tech_state.state != LearningState.IN_PROGRESS:
            raise InvalidLearningStateTransitionError(
                from_state=tech_state.state.value,
                to_state=LearningState.READY_FOR_REVIEW.value,
            )

        # 3. Find the active session
        active_session = (
            await self._learning_session_log_repo.find_active_session_by_trainee_id(
                trainee_id
            )
        )
        if not active_session:
            raise NoActiveLearningSessionError(
                f"No active learning session found for trainee {trainee_id}."
            )

        # 4. Check session consistency
        if active_session.trainee_technology_state_id != tech_state.id:
            raise LearningSessionAlreadyInProgressError(
                f"Active session found ({active_session.id}) does not match "
                f"the requested technology state ({tech_state.id})."
            )

        # 5. Update the log (stop the timer)
        updated_log = active_session.model_copy(
            update={"end_time": datetime.now(timezone.utc)}
        )

        # 6. Update the state (ready for review)
        updated_tech_state = tech_state.model_copy(
            update={"state": LearningState.READY_FOR_REVIEW}
        )

        # 7. Persist changes
        await self._learning_session_log_repo.update(updated_log)
        await self._trainee_tech_state_repo.update(updated_tech_state)

        return updated_tech_state

    async def get_trainee_dashboard(
        self, trainee_id: UUID
    ) -> list[TraineeTechnologyState]:
        """
        Retrieves all technology states for a given trainee.

        :param trainee_id: The ID of the trainee.
        :return: A list of TraineeTechnologyState models.
        """
        return await self._trainee_tech_state_repo.list_by_trainee_id(trainee_id)
