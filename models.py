import sqlalchemy as sa

__all__ = ['feed']

meta = sa.MetaData()


feed = sa.Table(
        'feed', meta,
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String(300), nullable=False),
        sa.Column('link', sa.String(300), nullable=False),
        sa.Column('pub_date', sa.DateTime, nullable=False),
    )
