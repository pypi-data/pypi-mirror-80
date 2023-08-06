# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

"""
Overview
++++++++

Provides functions to exchange messages with a JMS broker.

This package exposes the `com.ibm.streamsx.jms <https://ibmstreams.github.io/streamsx.jms/>`_ toolkit as Python methods for use with Streaming Analytics service on
IBM Cloud and IBM Streams including IBM Cloud Pak for Data.

"""

__version__='0.3.3'

__all__ = ['download_toolkit', 'produce', 'consume']
from streamsx.jms._jms import download_toolkit, produce, consume
