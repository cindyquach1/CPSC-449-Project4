#!/bin/sh

http --verbose POST localhost:5000/users/ @"$1"
http --verbose POST localhost:5000/timelines/ @"$1"