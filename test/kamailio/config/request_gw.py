#!/usr/bin/env python3

import sys
import Router.Logger as Logger
import KSR as KSR
import httplib2
import json
import configparser
import os
import sqlite3
import datetime
from contextlib import closing

dbPath = '/usr/local/etc/kamailio/kamailio.sqlite'

class RequestGw:
    def __init__(self):
        Logger.LM_ERR('RequestGw.__init__\n')
        sipSecret=os.environ.get('SIP_SECRET').replace('"',"").replace("'", "")
        self.sipDomain=os.environ.get('SIP_DOMAIN').replace('"',"").replace("'", "")
        self.publicIP=os.environ.get('PUBLIC_IP').replace('"',"").replace("'", "")
        self.gwNamePart = os.environ.get('GW_NAME_PREFIX').replace('"',"").replace("'", "")
        KSR.pv.sets("$var(secret)", sipSecret)

    def child_init(self, y):
        Logger.LM_ERR('RequestGwchild_init(%d)\n' % y)
        return 0

    def lockGw (self):
        res=''
        with closing(sqlite3.connect(dbPath)) as con:
            with closing(con.cursor()) as cursor:
                cursor.execute('''SELECT contact, username, socket FROM location
                                  WHERE
                                      locked = 0 AND
                                      username LIKE '%'||?||'%' AND
                                      NOT EXISTS (
                                         SELECT callee_contact
                                         FROM dialog
                                         WHERE callee_contact LIKE '%'||location.username||'%'
                                      );''',(self.gwNamePart,))
                contactList = cursor.fetchall()
                if len(contactList) == 0:
                    return
                for contact in contactList:
                    cursor.execute('''UPDATE location SET locked = 1
                                      WHERE
                                          location.contact = ? AND
                                          locked = 0 AND
                                          NOT EXISTS (
                                             SELECT callee_contact
                                             FROM dialog
                                             WHERE callee_contact LIKE '%'||?||'%'
                                          );''',(contact[0], contact[1],))
                    res = con.commit()
                    if cursor.rowcount > 0:
                        return contact
        return

    def handler(self, msg, args):
        Logger.LM_ERR("Loggers.py:      LM_ERR: msg: %s" % str(args))
        Logger.LM_ERR('RequestGw.handler(%s, %s)\n' % (msg.Type, str(args)))
        if (msg.Type == 'SIP_REQUEST' and
            ((msg.RURI).find(self.sipDomain) != -1 or
             (msg.RURI).find(self.publicIP) != -1)):
            if msg.Method == 'INVITE' and (msg.RURI).find(self.gwNamePart) == -1:
                Logger.LM_ERR('SIP request, method = %s, RURI = %s, From = %s\n' % (msg.Method, msg.RURI, msg.getHeader('from')))
                uri = msg.RURI
                room = (uri.split(":", 1)[1]).split('@')[0]
                displayName = ""
                if "<" in msg.getHeader('from'):
                    displayName = (msg.getHeader('from').split('<')[0])
                Logger.LM_ERR('Room Name %s\n' % room )
                gwRes = self.lockGw()
                if gwRes:
                    gwUri = gwRes[1]
                    gwSocket = gwRes[2].split(':')[1]
                    Logger.LM_ERR('Returned Gateway: %s\n' % gwUri)
                    msg.rewrite_ruri("sip:%s@%s" % (gwUri, gwSocket))
                    displayNameWRoom = '"%s-%s%s"' % (str(len(room)), room, displayName.replace('"',''))
                    KSR.uac.uac_replace_from(displayNameWRoom, "")
                    Logger.LM_ERR('########## SIP request, method = %s, RURI = %s, From = %s\n' % (msg.Method, msg.RURI, msg.getHeader('from')))

        return 1

def mod_init():
    return RequestGw()
