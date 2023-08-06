#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
import os
import pprint
import threading
import time
import sys
import uuid

import raisin

def history(content={}):
    """
    Cette fonction retourne l'ensemble des Ip deja connues et la date
    de la derniere recherche
    """
    def write(path, content):
        """
        ecrase le fichier par un nouveau
        """
        with open(path, "w", encoding="utf-8") as f:
            stdcourant = sys.stdout
            sys.stdout = f
            try:
                pprint.pprint(content)
            except Exception as e:
                raise e from e
            finally:
                sys.stdout = stdcourant

    path = os.path.join(os.path.expanduser("~"), ".raisin/padlock_history.py")
    if not os.path.exists(path):    # si l'historique n'est pas existant
        content = {
                "last_check": 0,    # date de la derniere mise a jour
                "ip": set([None]),  # ensemble de toutes les ip deja identifiees
                }
        write(path, content)
        return content
    IPv4Address = ipaddress.IPv4Address # permet d'interpreter le contenu du fichier
    IPv6Address = ipaddress.IPv6Address
    with open(path, "r", encoding="utf-8") as f:
        try:
            old_content = eval(f.read())
        except SyntaxError:
            old_content = None
    if old_content == None:
        os.remove(path)
        old_content = history(content)
    content["last_check"] = content["last_check"] if "last_check" in content else old_content["last_check"]
    content["ip"] = content["ip"] | old_content["ip"] if "ip" in content else old_content["ip"]
    if content != old_content:
        write(path, content)
    return content

def email(myid, settings):
    """
    envoi un email a la personne concernee
    cette email contient plein d'info sur la situation actuelle
    """
    signature = uuid.uuid4()
    address = settings["account"]["email"]
    subject = "raisin padlock notification"
    message = "A new ip is detected!\n\n" + repr(myid)
    raisin.communication.mail.send(address, subject, message, signature=signature)

def cipher(settings):
    """
    chiffre tous les fichiers
    qui doivent etre chiffree en cas de prise d'otage
    """
    def walk(paths, excluded_paths):
        """
        generateur qui cede les chemins des fichiers a chiffrer et a dechiffrer
        """
        excluded_paths = [os.path.abspath(p) for p in excluded_paths] # on met les chemin a la norme
        for path in (p for p in map(os.path.abspath, paths) if p not in excluded_paths): # on parcours chacun des repertoires parents
            if os.path.isdir(path):
                for f in (os.path.join(path, f1) for f1 in os.listdir(path)): # on commence d'abord par
                    if os.path.isfile(f) and f not in excluded_paths: # retourner les fichiers presents en haut
                        yield f                                     # de l'arborecence
                for d in (os.path.join(path, d1) for d1 in os.listdir(path)): # on passe ensuite
                    if os.path.isdir(d) and d not in excluded_paths: # aux dossiers
                        yield from walk([d], excluded_paths)        # on cede recursivement tous les fichiers qu'il contient
            else:
                yield path

    signature = uuid.uuid4()
    with raisin.Printer("Cipher preparation...", signature=signature) as p:
        if settings["account"]["security"]["hash"] == None:         # Si il n'y a pas de mot de passe:
            p.show("Sans mot de passe, l'on ne peu pas chiffrer!")
            return None
        paths = settings["account"]["padlock"]["paths"]["paths"]
        excluded_paths = settings["account"]["padlock"]["paths"]["excluded_paths"]
        for rep in walk(paths, excluded_paths):
            print(rep)
        raisin.worker.security.request_psw(force=True)

def main():
    content = {}
    while 1:
        with raisin.Printer("Load informations about padlock..."):
            settings = raisin.worker.configuration.load_settings()  # recuperation des informations de configuration
            content = history(content)                              # recuperation de l'hystorique
        sleep = max(settings["account"]["padlock"]["break_time"] - time.time() + content["last_check"], 0)
        with raisin.Printer("Sleep for %d seconds..." % sleep):
            time.sleep(sleep)                                       # on fait une pause de sorte a etre pile dans les clous
        with raisin.Printer("Make annalisis...") as p:
            myid = raisin.Id()                                      # recuperation des informations de contexte
            if myid.ipv4_lan not in content["ip"] or myid.ipv6 not in content["ip"]: # si on a changer d'ip
                p.show("L'ip est nouvelle!")
                if settings["account"]["padlock"]["notify_by_email"]:
                    t1 = threading.Thread(target=email, args=(myid, settings))
                    t1.start()
                if settings["account"]["padlock"]["cipher"]:
                    t2 = threading.Thread(target=cipher, args=(settings,))
                    t2.start()
                if settings["account"]["padlock"]["notify_by_email"]:
                    t1.join()
                if settings["account"]["padlock"]["cipher"]:
                    t2.join()

        content = {"last_check": time.time(), "ip": {myid.ipv4_lan, myid.ipv6}}


if __name__ == '__main__':
    main()
