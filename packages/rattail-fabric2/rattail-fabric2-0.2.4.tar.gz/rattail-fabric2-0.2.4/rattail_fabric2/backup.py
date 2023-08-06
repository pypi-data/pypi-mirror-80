# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Fabric library for Backup app
"""

import os
import datetime

from rattail_fabric2 import apt, borg, python, exists, make_deploy, mkdir, UNSPECIFIED


deploy_generic = make_deploy(__file__)


def deploy_rattail_backup_script(c, **context):
    """
    Deploy the generic `rattail-backup` script
    """
    context.setdefault('envname', 'backup')
    deploy_generic(c, 'backup/rattail-backup.mako', '/usr/local/bin/rattail-backup',
                   mode='0700', context=context, use_sudo=True)


def deploy_backup_everything(c, **context):
    """
    Deploy the generic `backup-everything` script
    """
    context.setdefault('envname', 'backup')
    context.setdefault('user', 'rattail')
    deploy_generic(c, 'backup/backup-everything.mako', '/usr/local/bin/backup-everything',
                   mode='0700', context=context, use_sudo=True)


def deploy_backup_app(c, deploy, envname, mkvirtualenv=True, user='rattail',
                      install_borg=False,
                      link_borg_to_bin=True,
                      install_luigi=False,
                      luigi_history_db=None,
                      luigi_listen_address='0.0.0.0',
                      install_rattail=True,
                      config=None,
                      rattail_backup_script=None,
                      everything=None,
                      crontab=None,
                      runat=UNSPECIFIED,
                      context={}):
    """
    Make an app which can run backups for the server.
    """
    if install_rattail and not config:
        path = '{}/rattail.conf.mako'.format(envname)
        if deploy.local_exists(path):
            config = path
        else:
            path = '{}/rattail.conf'.format(envname)
            if deploy.local_exists(path):
                config = path
            else:
                raise ValueError("Must provide config path for backup app")

    if install_borg:
        borg.install_dependencies(c)

    if install_luigi:
        c.sudo('supervisorctl stop backup:')

    # virtualenv
    if mkvirtualenv:
        python.mkvirtualenv(c, envname, python='/usr/bin/python3', runas_user=user)
    envpath = '/srv/envs/{}'.format(envname)
    c.sudo('chown -R {}: {}'.format(user, envpath))
    mkdir(c, os.path.join(envpath, 'src'), use_sudo=True, runas_user=user)
    c.sudo("bash -l -c 'workon {} && pip install --upgrade pip'".format(envname), user=user)

    if install_rattail:

        # rattail
        if not exists(c, os.path.join(envpath, 'src/rattail')):
            c.sudo('git clone https://rattailproject.org/git/rattail.git {}/src/rattail'.format(envpath), user=user)
            c.sudo("bash -l -c 'workon {} && cdvirtualenv && bin/pip install --editable src/rattail'".format(envname), user=user)
        deploy_generic(c, 'backup/git-exclude', os.path.join(envpath, 'src/rattail/.git/info/exclude'), use_sudo=True, owner=user)

        # config
        c.sudo("bash -l -c 'workon {} && cdvirtualenv && rattail make-appdir'".format(envname), user=user)
        # note, config is owned by root regardless of `user` - since we always run backups as root
        deploy(c, config, os.path.join(envpath, 'app/rattail.conf'), owner='root:{}'.format(user), mode='0640', use_sudo=True, context=context)
        c.sudo("bash -l -c 'workon {} && cdvirtualenv && bin/rattail -c app/rattail.conf make-config -T quiet -O app/'".format(envname), user=user)
        c.sudo("bash -l -c 'workon {} && cdvirtualenv && bin/rattail -c app/rattail.conf make-config -T silent -O app/'".format(envname), user=user)

        # rattail-backup script
        script_context = dict(context)
        script_context['envname'] = envname
        if rattail_backup_script:
            deploy(c, rattail_backup_script, '/usr/local/bin/rattail-backup', mode='0700', use_sudo=True,
                   context=script_context)
        else:
            deploy_rattail_backup_script(c, **script_context)

    # borg
    if install_borg:
        if install_rattail:
            packages = [
                'rattail[backup]',
            ]
        else:
            # these should be same as rattail[backup]
            packages = [
                'msgpack',
                'borgbackup',
                'llfuse==1.3.4',
            ]
        c.sudo("bash -l -c 'workon {} && cdvirtualenv && bin/pip install {}'".format(envname, ' '.join(packages)), user=user)
        if link_borg_to_bin:
            c.sudo("ln -sf {}/bin/borg /usr/local/bin/borg".format(envpath))

    # luigi
    if install_luigi:
        packages = ['luigi']
        if luigi_history_db:
            packages.append('SQLAlchemy')
            if luigi_history_db.startswith('postgresql://'):
                packages.append('psycopg2')
        c.sudo("bash -l -c 'workon {}; pip install {}'".format(envname, ' '.join(packages)), user=user)

        # basic config
        mkdir(c, ['{}/app/luigitasks'.format(envpath),
                  '{}/app/luigi'.format(envpath),
                  '{}/app/luigi/log'.format(envpath),
                  '{}/app/work'.format(envpath),
        ], owner=user, use_sudo=True)
        c.sudo('touch {}/app/luigitasks/__init__.py'.format(envpath), user=user)
        deploy_generic(c, 'backup/luigi.cfg.mako', '{}/app/luigi/luigi.cfg'.format(envpath),
                       owner=user, mode='0600', use_sudo=True,
                       context={'envpath': envpath, 'history_db': luigi_history_db})
        deploy_generic(c, 'backup/luigi-logging.conf.mako', '{}/app/luigi/luigi-logging.conf'.format(envpath),
                       owner=user, use_sudo=True, context={'envpath': envpath})

        # needed for restarting luigi tasks
        apt.install(c, 'at')

        # app/luigitasks/overnight.py - should define the OvernightBackups wrapper task
        path = '{}/luigi-overnight.py'.format(envname)
        if deploy.local_exists(path):
            deploy(c, path, '{}/app/luigitasks/overnight.py'.format(envpath),
                   owner=user, use_sudo=True)
        else:
            deploy_generic(c, 'backup/luigi-overnight.py', '{}/app/luigitasks/overnight.py'.format(envpath),
                           owner=user, use_sudo=True)

        # app/overnight-backups.sh - generic script to invoke OvernightBackups task
        deploy_generic(c, 'backup/overnight-backups.sh.mako', '{}/app/overnight-backups.sh'.format(envpath),
                       owner=user, mode='0755', use_sudo=True, context={'envpath': envpath})

        # app/restart-overnight-backups.sh - generic script to restart OvernightBackups task
        deploy_generic(c, 'backup/restart-overnight-backups.sh.mako', '{}/app/restart-overnight-backups.sh'.format(envpath),
                       owner=user, mode='0755', use_sudo=True, context={'envpath': envpath})

        # supervisor / luigid
        apt.install(c, 'supervisor')
        deploy_generic(c, 'backup/supervisor.conf.mako', '/etc/supervisor/conf.d/backup.conf',
                       use_sudo=True, context={
                           'envpath': envpath, 'user': user,
                           'listen_address': luigi_listen_address})
        c.sudo('supervisorctl update')
        c.sudo('supervisorctl start backup:')

    # upgrade script
    if install_rattail:
        deploy_generic(c, 'backup/upgrade.sh.mako', '{}/app/upgrade.sh'.format(envpath),
                       owner=user, mode='0755', use_sudo=True, context={'envpath': envpath, 'user': user})

    # backup-everything script
    if install_rattail or everything:
        everything_context = dict(context)
        everything_context['envname'] = envname
        everything_context['user'] = user
        if everything:
            deploy(c, everything, '/usr/local/bin/backup-everything', mode='0700', context=everything_context, use_sudo=True)
        else:
            deploy_backup_everything(c, **everything_context)

    # crontab
    if runat is UNSPECIFIED:
        runat = datetime.time(0) # defaults to midnight
    if runat is not None and (install_rattail or everything):
        crontab_context = dict(context)
        crontab_context['envname'] = envname
        crontab_context['pretty_time'] = runat.strftime('%I:%M %p')
        crontab_context['cron_time'] = runat.strftime('%M %H')
        if crontab:
            deploy(c, crontab, '/etc/cron.d/backup', context=crontab_context, use_sudo=True)
        else:
            deploy_generic(c, 'backup/crontab.mako', '/etc/cron.d/backup', context=crontab_context, use_sudo=True)
