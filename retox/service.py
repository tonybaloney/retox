# -*- coding: utf-8 -*-

from __future__ import absolute_import

from eventlet.green.subprocess import Popen
import eventlet
import eventlet.debug
from eventlet import GreenPool

import tox.session

from retox.reporter import RetoxReporter
from retox.log import retox_log


class RetoxService(object):
    def __init__(self, toxconfig, screen, env_frames):
        self._toxconfig = toxconfig
        self._logger = retox_log
        self._logger.debug('Instantiated service')
        self._resources = Resources(self)
        self._sdistpath = None

        RetoxReporter.screen = screen
        RetoxReporter.set_env_frames(env_frames)

        self.screen = screen

        # Disabled eventlet dumping exceptions in threads
        eventlet.debug.hub_exceptions(False)
        eventlet.debug.tpool_exceptions(False)

    def start(self):
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
        self._logger.info(' ')
        self._logger.info(' ')
        self._logger.info(' ')
        self._logger.info(' ---- Starting new test run ----')

        self._toxsession.report.reset()

        pool = GreenPool(size=self._toxconfig.option.numproc)

        for env in envlist:
            pool.spawn_n(self.runtests, env)

        pool.waitall()
        self.screen.refresh()

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
            self._logger.debug('Getting sdist resources')
            self._sdistpath = self.getresources("sdist")

            return
        if self.toxsession.config.skipsdist:
            self._logger.debug('Skipping sdist')
            venv_resources = self.getresources("venv:%s" % venvname)
            if venv_resources and len(venv_resources) > 0:
                self.toxsession.runtestenv(venv_resources[0], redirect=True)

        else:
            venv_resources = self.getresources("venv:%s" % venvname, "sdist")
            self._sdistpath = venv_resources[1]
            self._logger.debug('Running tests')

            if len(venv_resources) > 1:
                venv = venv_resources[0]
                sdist = venv_resources[1]
                venv.status = 0
                if self.toxsession.installpkg(venv, sdist):
                    self.toxsession.runtestenv(venv, redirect=True)
                else:
                    self._logger.debug('Failed installing package')
            else:
                self._logger.debug('VirtualEnv doesnt exist')

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
        lst = []
        for spec in specs:
            if spec not in self._resources:
                self._spec2thread[spec].wait()
            lst.append(self._resources[spec])
        return lst
