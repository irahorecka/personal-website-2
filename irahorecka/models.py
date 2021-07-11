from irahorecka import db


class GitHubRepo(db.Model):
    __tablename__ = "githubrepo"
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
    languages = db.relationship("RepoLanguage", backref="repo")
    url = db.Column(db.String(240))

    def __repr__(self):
        return f"GitHubRepo(name={self.name})"


class RepoLanguage(db.Model):
    __tablename__ = "repolanguage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    color = db.Column(db.String(20))
    repo_id = db.Column(db.Integer, db.ForeignKey("githubrepo.id"))

    def __repr__(self):
        return f"RepoLanguage(name={self.name})"
