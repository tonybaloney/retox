# -*- coding: utf-8 -*-
from  __future__ import absolute_import

from eventlet.green.subprocess import Popen, PIPE, STDOUT
import eventlet
import tox.session
from eventlet import GreenPool
from retox.reporter import RetoxReporter


class RetoxService(object):
    def __init__(self, toxconfig, logger):
        self._toxconfig = toxconfig
        self._logger = logger
        self._logger.debug('Instantiated service')
        self._resources = Resources(self)

    def start(self):
        self._logger.debug('Starting threads')
        if self.toxsession.report.tw.hasmarkup:
            self._logger.debug('Spawning process')
            eventlet.spawn_n(self.toxsession.report._loopreport)

    @property
    def toxsession(self):
        try:
            return self._toxsession
        except AttributeError:
            self._logger.debug('Starting new session')
            self._toxsession = tox.session.Session(
                self._toxconfig, Report=RetoxReporter, popen=Popen)
            return self._toxsession

    def run(self, envlist):
        pool = GreenPool(size=self._toxconfig.option.numproc)
        for env in envlist:
            pool.spawn_n(self.runtests, env)
        pool.waitall()
        if not self.toxsession.config.option.sdistonly:
            retcode = self._toxsession._summary()
            return retcode

    def provide_sdist(self):
        sdistpath = self.toxsession.get_installpkg_path()
        if not sdistpath:
            raise SystemExit(1)
        return sdistpath

    def provide_venv(self, venvname):
        venv = self.toxsession.getvenv(venvname)
        if self.toxsession.setupenv(venv):
            return venv

    def provide_installpkg(self, venvname, sdistpath):
        venv = self.toxsession.getvenv(venvname)
        return self.toxsession.installpkg(venv, sdistpath)

    def runtests(self, venvname):
        if self.toxsession.config.option.sdistonly:
            self._sdistpath = self.getresources("sdist")
            return
        if self.toxsession.config.skipsdist:
            venv, = self.getresources("venv:%s" % venvname)
            if venv:
                self.toxsession.runtestenv(venv, redirect=True)
        else:
            venv, sdist = self.getresources("venv:%s" % venvname, "sdist")
            self._sdistpath = sdist
            if venv and sdist:
                if self.toxsession.installpkg(venv, sdist):
                    self.toxsession.runtestenv(venv, redirect=True)

    def getresources(self, *specs):
        return self._resources.getresources(*specs)


class Resources(object):
    def __init__(self, providerbase):
        self._providerbase = providerbase
        self._spec2thread = {}
        self._pool = GreenPool()
        self._resources = {}

    def _dispatchprovider(self, spec):
        parts = spec.split(":")
        name = parts.pop(0)
        provider = getattr(self._providerbase, "provide_" + name)
        self._resources[spec] = res = provider(*parts)
        return res

    def getresources(self, *specs):
        for spec in specs:
            if spec not in self._resources:
                if spec not in self._spec2thread:
                    t = self._pool.spawn(self._dispatchprovider, spec)
                    self._spec2thread[spec] = t
        l = []
        for spec in specs:
            if spec not in self._resources:
                self._spec2thread[spec].wait()
            l.append(self._resources[spec])
        return l
