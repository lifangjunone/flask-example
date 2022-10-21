#!/usr/bin/env python
# coding=utf-8

import pytest

import common.consul as consul
from tests.configtest import app


@pytest.fixture
def consul_object(app):
    return consul.Consul(host=app.config['CONSUL_SERVER_HOST'], port=app.config['CONSUL_SERVER_PORT'])


@pytest.fixture
def consul_namespace(app):
    return '{prod_name}/config/{service}/{environment}/'.format(prod_name=app.config['PROD_NAME'],
                                                                service=app.config['SERVICE_NAME'],
                                                                environment=app.config['ENVIRONMENT'])


def test_consul_kv(consul_object, consul_namespace):
    consul_object.kv.put(consul_namespace + 'foo', 'bar')
    index, data = consul_object.kv.get(consul_namespace + 'foo', wait='1s')
    print(data)

    assert data['Value'] == 'bar'
    consul_object.kv.delete(consul_namespace + 'foo')
