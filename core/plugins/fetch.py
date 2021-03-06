#    iCraft is Copyright 2010-2011 both
#
#    The Archives team:
#                   <Adam Guy> adam@adam-guy.com AKA "Adam01"
#                   <Andrew Godwin> andrew@aeracode.org AKA "Aera"
#                   <Dylan Lukes> lukes.dylan@gmail.com AKA "revenant"
#                   <Gareth Coles> colesgareth2@hotmail.com AKA "gdude2002"
#
#    And,
#
#    The iCraft team:
#                   <Andrew Caluzzi> tehcid@gmail.com AKA "tehcid"
#                   <Andrew Dolgov> fox@bah.org.ru AKA "gothfox"
#                   <Andrew Horn> Andrew@GJOCommunity.com AKA "AndrewPH"
#                   <Brad Reardon> brad@bradness.co.cc AKA "PixelEater"
#                   <Clay Sweetser> CDBKJmom@aol.com AKA "Varriount"
#                   <James Kirslis> james@helplarge.com AKA "iKJames"
#                   <Jason Sayre> admin@erronjason.com AKA "erronjason"
#                   <Jonathon Dunford> sk8rjwd@yahoo.com AKA "sk8rjwd"
#                   <Joseph Connor> destroyerx100@gmail.com AKA "destroyerx1"
#                   <Kamyla Silva> supdawgyo@hotmail.com AKA "NotMeh"
#                   <Kristjan Gunnarsson> kristjang@ffsn.is AKA "eugo"
#                   <Nathan Coulombe> NathanCoulombe@hotmail.com AKA "Saanix"
#                   <Nick Tolrud> ntolrud@yahoo.com AKA "ntfwc"
#                   <Noel Benzinger> ronnygmod@gmail.com AKA "Dwarfy"
#                   <Randy Lyne> qcksilverdragon@gmail.com AKA "goober"
#                   <Willem van der Ploeg> willempieeploeg@live.nl AKA "willempiee"
#
#    Disclaimer: Parts of this code may have been contributed by the end-users.
#
#    iCraft is licensed under the Creative Commons
#    Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#    Or, send a letter to Creative Commons, 171 2nd Street,
#    Suite 300, San Francisco, California, 94105, USA.

from core.plugins import ProtocolPlugin
from core.decorators import *

class FetchPlugin(ProtocolPlugin):
    
    commands = {
        "fetch": "commandFetch",
        "bring": "commandFetch",
        "forcefetch": "commandForceFetch",
        "forcebring": "commandForceFetch",
        "ffetch": "commandForceFetch",
        "fbring": "commandForceFetch",
        "invite": "commandInvite",
        "finvite": "commandFetch",
        "forceinvite": "commandFetch",
    }

    hooks = {
        "chatmsg": "message"
    }

    def gotClient(self):
        self.client.var_fetchrequest = False
        self.client.var_fetchdata = ()

    def message(self, message):
        if self.client.var_fetchrequest:
            self.client.var_fetchrequest = False
            if message in ["y"]:
                sender,world,rx,ry,rz = self.client.var_fetchdata
                if self.client.world == world:
                    self.client.teleportTo(rx, ry, rz)
                else:
                    self.client.changeToWorld(world.id, position=(rx, ry, rz))
                self.client.sendServerMessage("You have accepted the fetch request.")
                sender.sendServerMessage("%s has accepted your fetch request." % self.client.username)
            elif message in ["n"]:
                sender = self.client.var_fetchdata[0]
                self.client.sendServerMessage("You did not accept the fetch request.")
                sender.sendServerMessage("%s did not accept your request." % self.client.username)
            else:
                sender = self.client.var_fetchdata[0]
                self.client.sendServerMessage("You have ignored the fetch request.")
                sender.sendServerMessage("%s has ignored your request." % self.client.username)
                return
            self.client.var_fetchdata
            return True
    
    @player_list
    @op_only
    @username_command
    def commandFetch(self, user, byuser, overriderank):
        "/fetch username - Op\nAliases: bring, forceinvite\nTeleports a user to be where you are"
        # Shift the locations right to make them into block coords
        rx = self.client.x >> 5
        ry = self.client.y >> 5
        rz = self.client.z >> 5
        user.var_prefetchdata = (self.client,self.client.world)
        if self.client.world.id == user.world.id:
            user.sendServerMessage("%s would like to fetch you." % self.client.username)
        else:
            user.sendServerMessage("%s would like to fetch you to %s." % (self.client.username, self.client.world.id))
        user.sendServerMessage("Do you wish to accept? [y]es [n]o")
        user.var_fetchrequest = True
        user.var_fetchdata = (self.client,self.client.world,rx,ry,rz)
        self.client.sendServerMessage("The fetch request has been sent.")

    @player_list
    @admin_only
    @username_command
    def commandForceFetch(self, user, byuser, overriderank):
        "/forcefetch username - Admin\nAliases: fbring, forcebring, ffetch\nTeleports a user to be where you are"
        # Shift the locations right to make them into block coords
        rx = self.client.x >> 5
        ry = self.client.y >> 5
        rz = self.client.z >> 5
        if user.world == self.client.world:
            user.teleportTo(rx, ry, rz)
        else:
            if self.client.isAdmin():
                user.changeToWorld(self.client.world.id, position=(rx, ry, rz))
            elif self.client.isMod():
                user.changeToWorld(self.client.world.id, position=(rx, ry, rz))
            else:
                self.client.sendServerMessage("%s cannot be forcefetched from '%s'" % (self.client.username, user.world.id))
                return
        user.sendServerMessage("You have been forcefetched by %s" % self.client.username)

    @player_list
    @username_command
    def commandInvite(self, user, byuser, overriderank):
        "/invite username - Guest\nAliases: finvite\nInvites a user to come to you."
        if user.world == self.client.world:
            self.client.sendServerMessage("%s has been invited." % user.username)
            user.sendServerMessage("%s has invited you." % self.client.username)
        else:
            self.client.sendServerMessage("%s has been invited to %s." % (user.username, self.client.world.id))
            user.sendServerMessage("%s has invited you to %s." % (self.client.username, self.client.world.id))
