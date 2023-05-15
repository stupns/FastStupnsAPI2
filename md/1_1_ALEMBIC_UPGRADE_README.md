# Alembic commands

Create revision:

```commandline
alembic revision -m "create posts table"

alembic current

```

After executing the command 'alembic current', Alembic checks the database and compares its current state with the state
of migrations that were previously executed. As a result, you will receive information about the latest executed migration
and the current status of the database.

U need add functional to py file 86d42f033b57_create_posts_table.py:

```python
def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
    pass
```
And pushing:

```commandline
alembic upgrade 86d42f033b57
```
will be result: 

```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 86d42f033b57, create posts table

```

## Add content column

Create revision:

```commandline
alembic revision -m "add content column to posts table"
```

in 8a33c1201619_add_content_column_to_posts_table.py add:

```python
def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
```

and update:

```commandline
alembic current
```

Show latest revision u can next:

```commandline 
alembic heads
```

```text
8a33c1201619 (head)
```

next u need upgrade actually revision:
```commandline
alembic upgrade head
```

## Return to the previous revision

```commandline
alembic downgrade 86d42f033b57
```

## Add user table

```commandline
alembic revision -m "add user table"
```

 In 73d00a5fcf7b_add_user_table.py add next line:
 
```python
def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
```

Check current revision and upgrade:

```commandline
alembic current
alembic upgrade head
```

Result will be:

```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 86d42f033b57 -> 8a33c1201619, add content column to posts table
INFO  [alembic.runtime.migration] Running upgrade 8a33c1201619 -> 73d00a5fcf7b, add user table
```

## Alembic add foreign-key to Posts table

```commandline
alembic revision -m "add foreign-key to posts table"
```

Add next code in 00e241a4645a_add_foreign_key_to_posts_table.py:

```python
def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
```
Check current revision and upgrade:

```commandline
alembic current
alembic upgrade head
```

## Add last few columns to posts table
```commandline
alembic revision -m "add last few columns to posts table"
```

add code b09e5d38b78b_add_last_few_columns_to_posts_table.py

```python
def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
```
and upgrade: 

```commandline
alembic upgrade +1
```
## Autogenerate reversion

```commandline
alembic revision --autogenerate -m "auto-vote"
```

## Add new fields in models and upgrade

In models add field :

```python
class User(Base):
   ...
    phone_number = Column(String)
```

and create revision autogenerate:

```commandline
alembic revision --autogenerate -m "add phone number"
alembic upgrade head
```
