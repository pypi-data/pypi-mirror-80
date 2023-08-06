#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import socket
import threading
import uuid

import raisin

def send(s, generator, signature):
    """
    permet d'envoyer des donnees
    """
    def standardize_generator_sizes(generator, buff_size):
        """
        'generator' est un generateur qui cede des paquets de taille tres variable
        les paquets doivent etre de type 'bytes'
        le but est ici, d'uniformiser la taille des packets afin de renvoyer des packets de 
        'buff_size' octets
        cede donc les paquets au fure et a meusure
        """
        pack = b""
        for data in generator:                                          # on va lentement vider le generateur
            pack += data                                                # pour stocker peu a peu les paquets dans cette variable
            while len(pack) >= buff_size:                               # si le packet est suffisement gros
                yield pack[:buff_size]                                  # on le retourne avec la taille reglementaire
                pack = pack[buff_size:]                                 # puis on le racourci et on recomence le test
        if pack:
            yield pack       
    
    def anticipator(generator):
        """
        cede les packets du generateur accompagne d'un boolean
        qui vaut True si l'element itere est le dernier
        et false sinon. Le generateur doit donc etre capable de ceder au moin un paquet
        """
        actuel = next(generator)
        for pack in generator:
            yield False, actuel
            actuel = pack
        yield True, actuel
    
    with raisin.Printer("Envoi des donnees...", signature=signature) as p:
        for is_end, data in anticipator(standardize_generator_sizes(generator, 1024*1024 -1)):
            p.show("Contenu: %s" % (bytes([is_end]) + data))
            s.send(bytes([is_end]) + data)

def receive(s, signature):
    """
    permet de receptionner les donnees,
    meme si elle sont nombreuses
    retourne soit directement les donnes soit le nom du fichier qui les contients
    ce qui permet de distinguer les 2, c'est le premier bit qui vaut 1 si les donnees sont directement recuperee
    ou 0 si ce qui suit est le nom de fichier
    """
    with raisin.Printer("Reception des donnees...", signature=signature) as p:
        data = s.recv(1024*1024)
        is_end = data[0]
        if is_end:
            p.show("Contenu: %s" % (b"\x01" + data[1:]))
            return b"\x01" + data[1:]
        filename = os.path.join(str(raisin.temprep), str(uuid.uuid4()))
        with open(filename, "wb") as f:
            f.write(data[1:])
            while not is_end:
                data = s.recv(1024*1024)
                f.write(data[1:])
                is_end = data[0]
        p.show("Contenu: %s" % (b"\x00" + filename.encode("utf-8")))
        return b"\x00" + filename.encode("utf-8")

def _client(ip_client, port_client, client_socket, parallelization_rate, signature):
    """
    prend en charge un client
    """
    with raisin.Printer("Communication en cours...", signature=signature) as p:
        with raisin.Printer("Reception de la requette...", signature=signature):
            requette = receive(client_socket, signature=signature)
        with raisin.Printer("Traitement de la requette...", signature=signature):
            resultat = raisin.process(
                raisin.communication.answering.answering,
                args=(requette, signature),
                parallelization_rate=parallelization_rate)
        with raisin.Printer("Envoi de la reponse...", signature=signature):
            send(client_socket, resultat, signature=signature)
            # p.show("Contenu: %s" % resultat)
            # client_socket.sendall(resultat)
        client_socket.close()


class ServerIpv4(threading.Thread):
    """
    se met en ecoute sur une ipv4
    """
    def __init__(self, parallelization_rate, signature):
        threading.Thread.__init__(self)
        assert 0 <= parallelization_rate <= 2
        self.parallelization_rate = parallelization_rate
        self.signature = signature
        self.must_die = False

        self.port = raisin.setup.load_settings()["server"]["port"]
        self.listen = raisin.setup.load_settings()["server"]["listen"]
        self.ip = str(raisin.Id().ipv4_lan)

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # on tente de reutiliser le port si possible
        self.tcp_socket.bind((self.ip, self.port))
    
    def run(self):        
        with raisin.Printer("Lancement du serveur ipv4...", signature=self.signature) as p:
            while not self.must_die:
                self.tcp_socket.listen(self.listen)
                p.show("En ecoute sur l'addresse %s port %d." % (self.ip, self.port))
                client_socket, (ip_client, port_client) = self.tcp_socket.accept()
                
                if self.parallelization_rate:
                    threading.Thread(
                        target=_client,
                        args=(ip_client, port_client, client_socket),
                        kwargs={
                            "parallelization_rate": 0 if self.parallelization_rate < 2 else self.parallelization_rate,
                            "signature": uuid.uuid4()
                            },
                        ).start()
                else:
                    _client(
                        ip_client,
                        port_client,
                        client_socket,
                        parallelization_rate=0,
                        signature=self.signature)

    def close(self):
        self.must_die = True
        self.tcp_socket.close()

    def __del__(self):
        self.close()

class ServerIpv6(threading.Thread):
    """
    se met en ecoute sur une ipv6
    """
    def __init__(self, parallelization_rate, signature):
        threading.Thread.__init__(self)
        assert 0 <= parallelization_rate <= 2
        self.parallelization_rate = parallelization_rate
        self.signature = signature
        self.must_die = False

        self.port = raisin.setup.load_settings()["server"]["port"]
        self.listen = raisin.setup.load_settings()["server"]["listen"]
        self.ip = str(raisin.Id().ipv6)

        self.tcp_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)   # creation d'un TCP/IP socket, SOCK_STREAM=>TCP
        self.tcp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        self.tcp_socket.bind((self.ip, self.port))

    def run(self):
        with raisin.Printer("Lancement du serveur ipv6...", signature=self.signature) as p:
            while not self.must_die:
                self.tcp_socket.listen(self.listen)
                p.show("En ecoute sur l'addresse %s port %d." % (self.ip, self.port))
                # print(self.tcp_socket.accept())
                client_socket, (ip_client, port_client, *_) = self.tcp_socket.accept()

                if self.parallelization_rate:
                    threading.Thread(
                        target=_client,
                        args=(ip_client, port_client, client_socket),
                        kwargs={
                            "parallelization_rate": 0 if self.parallelization_rate < 2 else self.parallelization_rate,
                            "signature": uuid.uuid4()
                            },
                        ).start()
                else:
                    _client(
                        ip_client,
                        port_client,
                        client_socket,
                        parallelization_rate=0,
                        signature=self.signature)

    def close(self):
        self.must_die = True
        self.tcp_socket.close()

    def __del__(self):
        self.close()
