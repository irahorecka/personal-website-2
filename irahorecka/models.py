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


class CraigslistHousing(db.Model):
    __tablename__ = "craigslisthousing"
    # `id` is the Craigslist's post ID
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(8))
    region = db.Column(db.String(8))
    site = db.Column(db.String(8))
    area = db.Column(db.String(8))
    post_id = db.Column(db.String(20))
    repost_of = db.Column(db.String(20))
    last_updated = db.Column(db.String(20))
    title = db.Column(db.String(120))
    neighborhood = db.Column(db.String(120))
    address = db.Column(db.String(120))
    lat = db.Column(db.String(20))
    lon = db.Column(db.String(20))
    price = db.Column(db.String(20))
    bedrooms = db.Column(db.String(8))
    housing_type = db.Column(db.String(80))
    area_ft2 = db.Column(db.String(20))
    laundry = db.Column(db.String(80))
    parking = db.Column(db.String(80))
    url = db.Column(db.String(120))
    misc = db.Column(db.String(240))

    def __repr__(self):
        return f"CraigslistHousing(post_id={self.post_id})"
