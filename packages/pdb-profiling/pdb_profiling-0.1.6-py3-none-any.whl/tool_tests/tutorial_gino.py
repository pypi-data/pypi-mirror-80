# @Created Date: 2020-05-26 08:02:13 pm
# @Filename: tutorial_gino.py
# @Email:  1730416009@stu.suda.edu.cn
# @Author: ZeFeng Zhu
# @Last Modified: 2020-05-26 08:02:16 pm
# @Copyright (c) 2020 MinghuiGroup, Soochow University
from gino import Gino
import asyncio

'''
Reference
---------

* <https://python-gino.org/docs/zh/master/tutorials/tutorial.html>
* <https://python-gino.org/docs/en/master/tutorials/tutorial.html>
'''

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.Unicode(), default='noname')


async def main():
    await db.set_bind('...')
    await db.gino.create_all()

    # further code goes here

    # CREATE/INSERT
    user = await User.create(nickname='fantix')
    '''
    OR:
    user = User(nickname='fantix')
    user.nickname += ' (founder)'
    await user.create()
    '''
    # This will cause GINO to execute this SQL with parameter 'fantix':
    # INSERT INTO users (nickname) VALUES ($1) RETURNING users.id, users.nickname

    # RETRIEVE
    user = await User.get(1)
    # SQL (parameter: 1):
    # SELECT users.id, users.nickname FROM users WHERE users.id = $1
    all_users = await db.all(User.query)
    # SQL:
    # SELECT users.id, users.nickname FROM users
    all_users = await User.query.gino.all()
    # SQL:
    # SELECT users.id, users.nickname FROM users
    # 'it is even not needed to import the db reference for execution'
    founding_users = await User.query.where(User.id < 10).gino.all()
    # SQL (parameter: 10):
    # SELECT users.id, users.nickname FROM users WHERE users.id < $1
    user = await User.query.where(User.nickname == 'fantix').gino.first()
    # SQL (parameter: 'fantix'):
    # SELECT users.id, users.nickname FROM users WHERE users.nickname = $1
    name = await User.select('nickname').where(User.id == 1).gino.scalar()
    # SQL (parameter: 1):
    # SELECT users.nickname FROM users WHERE users.id = $1
    print(name)
    population = await db.func.count(User.id).gino.scalar()
    # SQL:
    # SELECT count(users.id) AS count_1 FROM users
    print(population)  # 17 for example

    # UPDATE
    # create a new user
    user = await User.create(nickname='fantix')
    # get its name
    name = await User.select('nickname').where(
        User.id == user.id).gino.scalar()
    assert name == user.nickname  # they are both 'fantix' before the update
    # modification here
    await user.update(nickname='daisy').apply()
    # SQL (parameters: 'daisy', 1):
    # UPDATE users SET nickname=$1 WHERE users.id = $2 RETURNING users.nickname
    print(user.nickname)  # daisy
    # get its name again
    name = await User.select('nickname').where(
        User.id == user.id).gino.scalar()
    print(name)  # daisy
    assert name == user.nickname  # they are both 'daisy' after the update
    # ---
    await User.update.values(nickname='Founding Member ' + User.nickname).where(
        User.id < 10).gino.status()
    # SQL (parameter: 'Founding Member ', 10):
    # UPDATE users SET nickname=($1 || users.nickname) WHERE users.id < $2
    name = await User.select('nickname').where(
        User.id == 1).gino.scalar()
    print(name)  # Founding Member fantix

    # DELETE
    user = await User.create(nickname='fantix')
    await user.delete()
    # SQL (parameter: 1):
    # DELETE FROM users WHERE users.id = $1
    print(await User.get(user.id))  # None
    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
