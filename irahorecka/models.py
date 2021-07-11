from irahorecka import db


class GitHubRepos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    full_name = db.Column(db.String(120))
    description = db.Column(db.String(240))
    license = db.Column(db.String(80))
    private = db.Column(db.String(20))
    stars = db.Column(db.Integer)
    forks = db.Column(db.Integer)
    commits = db.Column(db.Integer)
    open_issues = db.Column(db.Integer)
    languages = db.relationship("RepoLanguages", uselist=False)


class RepoLanguages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey("GitHubRepos.id"))
    name = db.Column(db.String(80))
    color = db.Column(db.String(20))
