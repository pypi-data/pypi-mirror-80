remind-me-some
==============

.. image:: https://github.com/audrow/remind-me-some/workflows/Continuous%20Integration/badge.svg
   :target: https://github.com/audrow/remind-me-some/actions?query=branch%3Amaster

.. image:: https://codecov.io/gh/audrow/remind-me-some/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/audrow/remind-me-some

Schedules some number of items that are due today.

Tasks that you don't get to are weighted to be more heavily in the future.

Features
--------
- Repeatedly schedules tasks at a specified frequency
- Schedule a set number or less tasks each day
- Tasks that don't get done or scheduled will increase in priority
- Tested on Python 3.6, 3.7, and 3.8


Usage
-----

.. code-block:: bash

    $ git clone https://github.com/audrow/remind-me-some
    $ pip install remind-me-some

.. code-block:: python

    from datetime import date, timedelta
    from remind_me_some.goal import Goal
    from remind_me_some.schedule_manager import ScheduleManager

    goals = (
        ("Call Mom", timedelta(weeks=1)),
        ("Call Dad", timedelta(weeks=1)),
        ("Call Grandma", timedelta(weeks=2)),
        ("Call Grandpa", timedelta(weeks=2)),
        ("Call Cousin", timedelta(weeks=4)),
        ("Call Uncle", timedelta(weeks=4)),
    )
    goals_ = []
    for goal in goals:
        goals_.append(Goal(name=goal[0], frequency=goal[1]))

    sm.add_goals(*goals_)
    sm.update_schedule()
    print(sm)
    sm.run()  # run the callback for the scheduled action
    sm.run()  # clear the action if it's completed
    print(sm)


Documentation
-------------

Remind-Me-Some's documentation lives at `remind-me-some.readthedocs.io <https://remind-me-some.readthedocs.io/>`_.


About Remind-Me-Some
--------------------

Remind-Me-Some was created by `Audrow Nash <https://audrow.github.io/>`_ - `audrow@hey.com <audrow@hey.com>`_

Distributed under the MIT license. See ``LICENSE.txt`` for more information.
