#!/usr/bin/env python
# coding=utf-8

import pytest

from ResearchManagement import create_app, db


# pytest supports execution of fixture specific finalization code when the fixture goes out of scope.
# By using a yield statement instead of return, all the code after the yield statement serves as the teardown code

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    app.config['ENVIRONMENT'] = 'testing'
    with app.app_context():
        db.create_all()
        print('\n' + '============= SETUP DB ==============')
        yield app
        print('\n' + '============ TEARDOWN DB ============')
        db.session.remove()
        db.drop_all()
