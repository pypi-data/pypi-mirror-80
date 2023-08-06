# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Converter

@author: tadahaya
"""

import pandas as pd
import numpy as np
from itertools import chain
from tqdm import trange
import pickle
import collections
from collections import defaultdict

class SynoDict():
    """
    Dict considering synonyms
    time consuming in dict preparation

    Parameters
    ----------
    keys: list
        representative keys for decoder
        
    synonyms: list
        a list of synonym sets [{},{},...]
        !! nan should be replaced with "" before construction !!
        
    values: list
        list of int

    """
    def __init__(self,keys=[],values=[],synonyms=[],processing=True):
        if processing:
            self.keys = keys
            lkeys = list(map(lambda x: str(x).lower(),keys))
            self.values = list(map(lambda x: int(x),values))
            self.decoder = dict(zip(self.values,lkeys))
            synonyms = [set([str(x).lower() for x in v]) for v in synonyms]
            lst = list(chain.from_iterable(synonyms))
            ol = set(k for k,v in collections.Counter(lst).items() if v > 1) | {""}
            synonyms = [v - ol for v in synonyms]
            self.synonyms = [{v} | w for v,w in zip(self.keys,synonyms)]
        else:
            self.keys = keys
            self.values = list(map(lambda x: int(x),values))
            self.decoder = dict(zip(values,keys))
            self.synonyms = synonyms
        self.__zip = list(zip(self.synonyms,self.values))
        self.not_found = set()


    def enc(self,word):
        """ encoder """
        for v,w in self.__zip:
            if word in v:
                return w
        raise KeyError(word)


    def fix(self,obj,substitute=0):
        """
        return fixed dict for converting the indicate list
        
        Parameters
        ----------
        obj: list
            a list of conversion target

        substitute: str
            a word employed for indicating not found keys        

        """
        value = self.enc_list(obj,substitute)
        return dict(zip(obj,value))


    def to_pickle(self,url):
        """ to save Synonym Dict """
        with open(url,"wb") as f:
            pickle.dump([self.keys,self.values,self.synonyms],f)


    def read_pickle(self,url):
        """ to load Synonym Dict """
        with open(url,"rb") as f:
            temp = pickle.load(f)
        self.keys = temp[0]
        self.values = temp[1]
        self.synonyms = temp[2]
        self.decoder = dict(zip(self.values,self.keys))
        self.not_found = set()


    def enc_list(self,target,substitute=0):
        """
        convert a list according to pre-defined dict

        Parameters
        ----------
        target: list

        substitute: str
            a word employed for indicating not found keys        
        
        """
        res = []
        ap = res.append
        nf = []
        ap2 = nf.append
        for v in target:
            try:
                ap(self.enc(v))
            except KeyError:
                ap(substitute)
                ap2(v)
        self.not_found = set(nf)
        return res


    def dec_list(self,target,substitute=0):
        """ decoder for list """
        res = []
        ap = res.append
        nf = []
        ap2 = nf.append
        for v in target:
            try:
                ap(self.decoder[v])
            except KeyError:
                ap(substitute)
                ap2(v)
        self.not_found = set(nf)
        return res


    def enc_set(self,target):
        """
        convert a set according to pre-defined dict

        Parameters
        ----------
        target: set

        substitute: str
            a word employed for indicating not found keys        
        
        """
        res = set()
        ad = res.add
        nf = set()
        ad2 = nf.add
        for v in target:
            try:
                ad(self.enc(v))
            except KeyError:
                ad2(v)
        self.not_found = nf
        return res


    def dec_set(self,target,substitute=0):
        """ decoder for set """
        res = set()
        ad = res.add
        nf = set()
        ad2 = nf.add
        for v in target:
            try:
                ad(self.decoder[v])
            except KeyError:
                ad2(v)
        self.not_found = nf
        return res


class FixedDict(SynoDict):
    """ handling conversion between names and IDs """
    def __init__(self,keys,values,synonyms,processing=False):
        super().__init__(keys,values,synonyms,processing)
        self.enc = dict(zip(self.keys,self.values))


    def enc_list(self,target,substitute=0):
        """
        convert a list according to pre-defined dict

        Parameters
        ----------
        target: list

        substitute: str
            a word employed for indicating not found keys        
        
        """
        res = []
        ap = res.append
        nf = []
        for v in target:
            try:
                ap(self.enc[v])
            except KeyError:
                ap(substitute)
                nf.append(v)
        self.not_found = set(nf)
        return res


    def dec_list(self,target,substitute=0):
        """ decoder for list """
        res = []
        ap = res.append
        nf = []
        for v in target:
            try:
                ap(self.decoder[v])
            except KeyError:
                ap(substitute)
                nf.append(v)
        self.not_found = set(nf)
        return res


    def enc_set(self,target):
        """
        convert a set according to pre-defined dict

        Parameters
        ----------
        target: set

        substitute: str
            a word employed for indicating not found keys        
        
        """
        res = set()
        ad = res.add
        nf = set()
        ad2 = nf.add
        for v in target:
            try:
                ad(self.enc[v])
            except KeyError:
                ad2(v)
        self.not_found = nf
        return res


    def dec_set(self,target,substitute=0):
        """ decoder for set """
        res = set()
        ad = res.add
        nf = set()
        ad2 = nf.add
        for v in target:
            try:
                ad(self.decoder[v])
            except KeyError:
                ad2(v)
        self.not_found = nf
        return res


class Integrator():
    def __init__(self):
        self.member = []
        self.ref = None
        self.ref_fix = dict()
        self.encoder = dict() # integrated dict for encoding
        self.decoders = dict() # dict of dict for each decoding
        self.__sub = 0


    def make_ref(self,keys=[],values=[],synonyms=[]):
        """ prepare SynoDict """
        self.ref = SynoDict(keys,values,synonyms,processing=True)
        return self.ref


    def load_ref(self,ref):
        """
        load a reference

        Parameters
        ----------
        ref: SynoDict

        """
        self.ref = ref
        self.ref_fix = self.ref.fix()


    def register(self,keys=[],name=None,ref=None,drop=False):
        """
        registration of a member

        Parameters
        ----------
        name: str
            indicates the key for the data

        keys: list
            data for dictionary preparation
            !! Should be lower case !!
                    
        """
        if len(keys)==0:
            raise ValueError("!! Give keys as a list !!")
        if ref is not None:
            self.ref = ref
        if self.ref is None:
            raise ValueError("!! Load reference before this process !!")
        if name is None:
            name = len(self.member)
        if drop:
            values = self.ref.enc_list(keys,substitute=np.nan)
            df = pd.DataFrame({"keys":keys,"values":values}).dropna()
            keys = list(df["keys"])
            values = list(df["values"])
        else:
            values = self.ref.enc_list(keys,self.__sub)
        dic = dict(zip(keys,values))
        self.encoder.update(dic)
        dec = dict(zip(values,keys))
        dec.update({self.__sub:"NOTFOUND"})
        self.decoders[name] = dec


    def enc_list(self,target):
        """
        convert a list according to the integrated encoder

        Parameters
        ----------
        target: list
        
        """
        try:
            res = [self.encoder[v] for v in target]
        except KeyError:
            raise KeyError("!! Some inputs are not found: register(drop=False) whole keys to be analyzed !!")
        return res


    def enc_set(self,target):
        """
        convert a list according to the integrated encoder

        Parameters
        ----------
        target: set
        
        """
        try:
            res = {self.encoder[v] for v in target}
        except KeyError:
            raise KeyError("!! Some inputs are not found: register(drop=False) whole keys to be analyzed !!")
        return res


    def dec_list(self,target,key):
        """
        convert a list according to the integrated decoder

        Parameters
        ----------
        target: list
        
        """
        try:
            res = [self.decoders[key][v] for v in target]
        except KeyError:
            raise KeyError("!! Some inputs are not found: register(drop=False) whole keys to be analyzed !!")
        return res


    def dec_set(self,target):
        """
        convert a list according to the integrated decoder

        Parameters
        ----------
        target: set
        
        """
        try:
            res = {self.decoders[key][v] for v in target}
        except KeyError:
            raise KeyError("!! Some inputs are not found: register(drop=False) whole keys to be analyzed !!")
        return res


    def set_sub(self,substitute):
        """ set the word for substitution """
        self.__sub = substitute
