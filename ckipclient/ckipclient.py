#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import string
import time
from xml.etree import ElementTree
from xml.sax import saxutils
from unicodedata import category


class CKIPClient:
    """
    A Python client for the Chinese Word Segmentation System (see ckipsvr.iis.sinica.edu.tw)
    provided by Academia Sinica Chinese Knowledge and Information Processing (CKIP) Group.
    """

    def __init__(self, ip: str, port: int, usr: str, pwd: str, wait: int = 0):
        """
        Initialize the client.

        :param ip: CKIP server IP.
        :type ip: str
        :param port: CKIP server port.
        :type port: int
        :param usr: CKIP server username.
        :type usr: str
        :param pwd: CKIP server password.
        :type pwd: str
        :param wait: Number of seconds to wait before segmenting.
                     Used to prevent overwhelming requests.
        :type wait: int
        """

        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd
        self.wait = wait

    def safe_segment(self, text: str, pos: bool = True, retry: int = 5) -> list:
        """
        Segment the text into words, retry if an error occurred.

        :param text: Text to be segmented.
                     Characters that cannot be encoded in big5 will be replaced by '?'.
        :type text: str
        :param pos: Return part of speech or not.
        :type pos: bool
        :param retry: Maximum number of retries.
        :type retry: int
        :return: List of sentences, each sentence is a list of words.
                 Each word is a tuple of (word, part of speech) if pos is true.
                 Otherwise, it contains just the word.
        :rtype: list
        """

        counter = 0
        while counter <= retry:
            try:
                counter += 1
                results = self.segment(text, pos)
            except ElementTree.ParseError as err:
                print('ElementTree.ParseError:', err, flush=True)
                print('wait 10 seconds...', flush=True)
                time.sleep(10)
            except ConnectionError as err:
                print('ConnectionError:', err, flush=True)
                print('wait 10 seconds...', flush=True)
                time.sleep(10)
            except OSError as err:
                print('OSError:', err, flush=True)
                print('wait 10 seconds...', flush=True)
                time.sleep(10)
            else:
                return results
        print('failed after', retry, 'retries', flush=True)
        return []

    def segment(self, text: str, pos: bool = True) -> list:
        """
        Segment the text into words.

        :param text: Text to be segmented.
                     Characters that cannot be encoded in big5 will be replaced by '?'.
        :type text: str
        :param pos: Return part of speech or not.
        :type pos: bool
        :return: List of sentences, each sentence is a list of words.
                 Each word is a tuple of (word, part of speech) if pos is true.
                 Otherwise, it contains just the word.
        :rtype: list
        """

        if not text:
            return []

        if self.wait > 0:
            time.sleep(self.wait)

        request_xml = (
            '<?xml version="1.0" ?>'
            '<wordsegmentation version="0.1">'
            '<option showcategory="$pos" />'
            '<authentication username="$usr" password="$pwd" />'
            '<text>$text</text>'
            '</wordsegmentation>'
        )

        request_xml = string.Template(request_xml).substitute(
            pos=int(pos),
            usr=self.usr,
            pwd=self.pwd,
            text=saxutils.escape(text)
        )

        response_xml = b''
        proto = socket.getprotobyname('tcp')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto) as sock:
            sock.settimeout(600)
            sock.connect((self.ip, self.port))
            sock.sendall(request_xml.encode(encoding='big5', errors='replace'))
            ending_bytes = '</wordsegmentation>'.encode(encoding='big5')
            while ending_bytes not in response_xml:
                response_xml += sock.recv(4096)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        response_xml = response_xml.decode(encoding='big5', errors='replace')

        response_xml_sanitized = ''
        for char in response_xml.partition('</wordsegmentation>')[0]:
            response_xml_sanitized += '\ufffd' if category(char).startswith('C') else char
        response_xml = response_xml_sanitized + '</wordsegmentation>'

        try:
            root = ElementTree.fromstring(response_xml)
        except ElementTree.ParseError:
            raise ElementTree.ParseError(response_xml)

        status_code = root.find('processstatus').get('code')
        status_msg = root.find('processstatus').text
        if status_code != '0':
            raise ConnectionError((status_code, status_msg))

        results = []
        sentences = root.find('result').iterfind('sentence')
        for sentence in sentences:
            words = saxutils.unescape(sentence.text).split('\u3000')
            if any(word for word in words):
                results.append([])
                for word in words:
                    if word and word[-1] == ')':
                        idx = word.rfind('(')
                        word = (word[:idx], word[idx+1:-1]) if pos else word[:idx]
                        results[-1].append(word)
                    elif word:
                        word = (word, '') if pos else word
                        results[-1].append(word)

        return results
