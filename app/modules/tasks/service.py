
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.tasks.models import Task
from app.modules.tasks.schemas import TaskCreate, TaskUpdate, TaskStatus
from app.modules.users.models import User


def create_task(
    db: Session,
    task_data: TaskCreate,
    current_user: User,
) -> Task:
    task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    current_user: User,
    status: TaskStatus | None = None,
) -> list[Task]:
    query = select(Task).where(Task.owner_id == current_user.id)

    if status is not None:
        query = query.where(Task.status == status.value)

    return list(db.scalars(query.order_by(Task.id.desc())).all())


def get_task(
    db: Session,
    task_id: int,
    current_user: User,
) -> Task | None:
    query = select(Task).where(
        Task.id == task_id,
        Task.owner_id == current_user.id,
    )

    return db.scalars(query).first()


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
) -> Task:
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if isinstance(value, TaskStatus):
            value = value.value

        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
