from .. import models as md
from sqlalchemy import or_, func


def create_project(user_id, title, logo, description, project_start_date, project_end_date, objective, pas):
    new_project = md.Project(user_id, title, logo, description, project_start_date, project_end_date
                             , objective, pas)
    md.db.session.add(new_project)
    md.db.session.flush()
    md.db.session.refresh(new_project)
    md.db.session.commit()
    return new_project.id
